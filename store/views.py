from django.shortcuts import render
from .models import Product
from .forms import OrderForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem, OrderItem, Order, Product
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import requests
from decouple import config




def home(request):
    query = request.GET.get('search')
    if query:
        products = Product.objects.filter(name__icontains=query, is_available=True)
    else:
        products = Product.objects.filter(is_available=True)
    return render(request, 'store/home.html', {'products': products})

# About page view
def about(request):
    return render(request, 'store/about.html')


def order(request):
    success = False
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        items = request.POST['items']

        # Here you can integrate SMS API like Twilio or just simulate
        print(f"Order from {name} ({phone}): {items}")
        success = True

    return render(request, 'store/order.html', {'success': success})

from .models import Feedback

def feedback(request):
    feedback_list = Feedback.objects.order_by('-date_submitted')


    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        Feedback.objects.create(name=name, email=email, message=message)
        return render(request, 'store/feedback.html', {'success': True, 'feedback_list': feedback_list})

    return render(request, 'store/feedback.html', {'feedback_list': feedback_list})


# Add to cart
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to add to cart.")
        return redirect('login')

    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} added to cart.")
    
    # Redirect back to the page the user came from
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


from decouple import config

# View cart and place order
@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total
            order.save()

            order_items_details = []
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
                order_items_details.append(
                    f"{item.product.name} — {item.quantity} x ₹{item.product.price} = ₹{item.product.price * item.quantity}"
                )

            cart_items.delete()

            # Send Email to Admin
            subject = 'New Order Placed'
            message = (
                f"New Order Placed!\n\n"
                f"Name: {order.name}\n"
                f"Phone: {order.phone}\n"
                f"Address: {order.address}\n"
                f"Total: ₹{order.total_price}\n\n"
                f"Items Ordered:\n" +
                "\n".join(order_items_details)
            )
            send_mail(subject, message, settings.EMAIL_HOST_USER, [settings.ADMIN_EMAIL], fail_silently=False)

            
            messages.success(request, "Order placed successfully!")
            return redirect('home')

    else:
        form = OrderForm()

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'form': form,
    })

# Remove from cart
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('view_cart')

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after register
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'store/order_history.html', {'orders': orders})
