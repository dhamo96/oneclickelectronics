"""demo_project URL Configuration

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
from inventory import views

urlpatterns = [
    path('',views.index,name = "index"),
    path('login',views.adminlogin,name = "adminlogin"),
    path('register',views.adminRegister,name = "adminRegister"),
    path('logout',views.adminLogout,name = "adminLogout"),
    path('forgot-password',views.adminForgotPassword,name = "adminForgotPassword"),
    path('otp-validation',views.adminOtpValidation,name = "adminOtpValidation"),
    path('change-password',views.adminChangepassword,name = "adminChangepassword"),
    path('retailer-update-password',views.retailerUpdatePassword,name = "retailer-update-password"),
    path('retailer-change-profile-picture',views.retailer_change_profile_picture,name = "retailer-change-profile-picture"),
    path('profile',views.adminProfile,name = "adminProfile"),
    path('shop-detail',views.shopDetail,name = "shop-detail"),
    path('product-upload',views.product_upload,name = "product-upload"),
    path('product_list',views.product_list,name = "product_list"),
    path('customer-list',views.customer_list,name = "customer-list"),
    path('customer-view/<int:pk>/',views.customer_view,name = "customer-view"),
    path('customer_delete/<int:pk>/',views.customer_delete,name = "customer_delete"),
    path('product_view/<int:pk>/',views.adminProduct_view,name = "product_view"),
    path('product_delete/<int:pk>/',views.product_delete,name = "product_delete"),
    path('product_edit/<int:pk>/',views.adminProduct_edit,name = "product_edit"),
    path('product-photo/<int:pk>/',views.photo_upload,name = "product-photo"),

    ## admin views
    path('shopAdmin',views.shopAdmin,name = "shopAdmin"),
    path('adminhome',views.adminHome,name = "adminhome"),
    path('view-all-retailers',views.view_all_retailers,name = "view-all-retailers"),
    path('admin_notification_retailer/',views.admin_notification_retailer,name='admin_notification_retailer'),
    path('admin_notification_shop/',views.admin_notification_shop,name='admin_notification_shop'),
    path('admin_notification_products/',views.admin_notification_products,name='admin_notification_products'),
    path('admin-retailers-pending-request',views.admin_retailers_pending_request,name='admin-retailers-pending-request'),
    path('admin_update_retailer_status/<int:pk>',views.admin_update_retailer_status,name='admin_update_retailer_status'),
    path('admin_notification_retailer_view/<int:pk>',views.admin_notification_retailer_view,name='admin_notification_retailer_view'),
    path('admin_notification_shop_view/<int:pk>',views.admin_notification_shop_view,name='admin_notification_shop_view'),
    path('admin_notification_customer/',views.admin_notification_customer,name='admin_notification_customer'),
    path('admin_view_retailer_profile/<int:pk>',views.admin_view_retailer_profile,name='admin_retailer_view_profile'),
    path('admin_view_customer_profile/<int:pk>',views.admin_view_customer_profile,name='admin_view_customer_profile'),
    path('admin_view_all_customers/',views.admin_view_all_customers,name='admin_view_all_customers'),
    path('admin_view_all_products/',views.admin_view_all_products,name='admin_view_all_products'),
    path('admin_view_all_shops/',views.admin_view_all_shops,name='admin_view_all_shops'),
    path('admin_view_product/<int:pk>',views.admin_view_product,name='admin_view_product'),
    path('admin_delete_product/<int:pk>',views.admin_delete_product,name='admin_delete_product'),
    path('admin_delete_retailer/<int:pk>',views.admin_delete_retailer,name='admin_delete_retailer'),
]