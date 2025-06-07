from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import register_view
urlpatterns = [
    path('', views.home, name='home'),  # home page
    path('about/', views.about, name='about'),  # about page
    path('order/', views.order, name='order'),
    path('feedback/', views.feedback, name='feedback'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('my-orders/', views.order_history, name='order_history'),

]
