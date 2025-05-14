from django.db import models
from inventory.models import *
# Create your models here.

class registration(models.Model):
	first_name = models.CharField(max_length=100,null=True,blank=True)
	last_name = models.CharField(max_length=100,null=True,blank=True)
	email = models.CharField(max_length=100,null=True,blank=True)
	landmark = models.CharField(max_length=100,null=True,blank=True)
	area = models.CharField(max_length=100,null=True,blank=True)
	city = models.CharField(max_length=100,null=True,blank=True)
	state = models.CharField(max_length=100,null=True,blank=True)
	zipcode = models.CharField(max_length=100,null=True,blank=True)
	country = models.CharField(max_length=100,null=True,blank=True)
	mobile_number = models.CharField(max_length=11,null=True,blank=True)
	age = models.CharField(max_length=3,null=True,blank=True)
	profile_pic = models.FileField(upload_to='profiles/',null=True, blank=True,default="pizzriea.JPG")
	password = models.CharField(max_length=100,null=True,blank=True)
	otp = models.IntegerField(default=567)
	view=models.BooleanField(default=False)
	

	def __str__(self):
		return self.first_name

class Wishlist(models.Model):
	customer_id = models.ForeignKey(registration, on_delete=models.CASCADE)
	product_Id = models.ForeignKey(Product, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.product_Id.product_name

class Cart(models.Model):
	customer_id = models.ForeignKey(registration, on_delete=models.CASCADE)
	retailer_Id =models.ForeignKey(adminUser, on_delete=models.CASCADE,blank=True,null=True)
	product_Id = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity=models.CharField(max_length=100,default="1")
	price=models.IntegerField(null=True)
	status=models.CharField(max_length=100,default="pending")
	date=models.DateField(auto_now=True)
	

	def __str__(self):
		return self.product_Id.product_name

class Transaction(models.Model):
	made_by = models.ForeignKey(registration, related_name='transactions',on_delete=models.CASCADE)
	made_on = models.DateTimeField(auto_now_add=True)
	amount = models.IntegerField()
	order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
	checksum = models.CharField(max_length=100, null=True, blank=True)
	date_of_order=models.DateTimeField(auto_now_add=True,blank=False)
	status=models.CharField(max_length=50,default='Pending')
	ord_deliver_otp=models.IntegerField(default=7878)
	order_notes=models.CharField(max_length=300,null=True)

	def save(self, *args, **kwargs):
		if self.order_id is None and self.made_on and self.id:
			self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
		return super().save(*args, **kwargs)
	
	def __str__(self):
		return self.made_by.first_name
