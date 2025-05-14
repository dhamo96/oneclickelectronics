from django.contrib import admin
from .models import *
# # Register your models here.
admin.site.register(adminUser)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(shop_detail)
admin.site.register(retailer_FeedBack)