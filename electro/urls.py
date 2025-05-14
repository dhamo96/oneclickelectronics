"""oneClick URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from electro import views

urlpatterns = [
    path('',views.home,name = "home"),
    path('login',views.login,name = "login"),
    path('register',views.register,name = "register"),
    path('logout',views.logout,name = "logout"),
    path('forgot_password',views.forgot_password,name = "forgot_password"),
    path('change_password',views.change_password,name = "change_password"),
    path('otpValidation',views.otpValidation,name = "otpValidation"),
    path('product-view/<int:pk>/',views.product_view,name = "product-view"),
    path('account',views.account,name = "account"),
    path('product-list/<int:pk>/',views.product_list,name = "product-list"),
    path('add_cart/<int:pk>/',views.addToCart,name = "add_cart"),
    path('cart',views.cart,name = "cart"),
    path('wishList/<int:pk>/',views.addToWishlist,name = "wishList"),
    path('wishlist',views.wishlist,name = "wishlist"),
    path('delete-wishList-product/<int:pk>/',views.deleteWishlist,name = "delete-wishList-product"),
    path('delete-cart-product/<int:pk>/',views.deleteCartItem,name = "delete-cart-product"),
    path('clear-shopping-cart',views.clear_shopping_cart,name = "clear-shopping-cart"),
    path('change-password',views.changePassword,name = "change-password"),
    path('checkout',views.checkout,name = "checkout"),
    path('pay/', views.initiate_payment, name='pay'),
    path('callback/', views.callback, name='callback'),
    path('search_product/', views.search_product, name='search_product'),
    path('update_qty/', views.update_qty, name='update_qty'),
]
