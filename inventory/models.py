from django.db import models
import datetime
# Create your models here.

class adminUser(models.Model):
	id = models.AutoField(primary_key=True)
	adminName = models.CharField(max_length=100)
	adminLastName = models.CharField(max_length=100)
	adminEmail = models.EmailField(unique=True)
	password = models.CharField(max_length=100)
	admin_otp = models.IntegerField(default=567)
	adminPhone = models.CharField(max_length=11,null=True)
	adminProfile_pic = models.FileField(upload_to='admin_profile/',null=True, blank=True,default="admin_profile/1.png")
	gender=models.CharField(max_length=10,null=True)
	status=models.CharField(default='Pending',max_length=10)
	home_country=models.CharField(max_length=10,null=True)
	home_state=models.CharField(max_length=50,null=True)
	home_city=models.CharField(max_length=50,null=True)
	home_pincode=models.IntegerField(blank=True,null=True)
	home_address=models.CharField(max_length=100,null=True)
	view=models.BooleanField(default=False)

	def __str__(self):
		return self.adminName

class shop_detail(models.Model):
	owner_id=models.ForeignKey(adminUser,on_delete=models.CASCADE)
	shop_name=models.CharField(max_length=200)
	shop_type=models.CharField(max_length=200)
	shop_country=models.CharField(max_length=30)
	shop_state=models.CharField(max_length=50)
	shop_city=models.CharField(max_length=50)
	shop_pincode=models.IntegerField(blank=True,null=True)
	shop_address=models.CharField(max_length=100)
	view=models.BooleanField(default=False)
	owner_id_proof=models.FileField(upload_to='images/')
	elc_bill=models.FileField(upload_to='images/')

	def __str__(self):
		return self.shop_name

class Category(models.Model):
	category_id = models.AutoField(primary_key=True)
	category_name = models.CharField(max_length=100,null=True)

	def __str__(self):
		return self.category_name


class Product(models.Model):
	adminUser_id =models.ForeignKey(adminUser,null=True,on_delete= models.CASCADE)
	shop_id=models.ForeignKey(shop_detail,null=True,on_delete=models.CASCADE)
	product_name = models.CharField(max_length=100,null=True)
	price = models.FloatField(null=True)
	qty = models.IntegerField(null=True)
	c_id = models.ForeignKey(Category,null=True,on_delete= models.CASCADE)
	desc = models.CharField(max_length=300,null=True)
	product_pic = models.FileField(upload_to='product/images',null=True, blank=True,default="pizzriea.JPG")
	views_count = models.IntegerField(default=0)
	view=models.BooleanField(default=False)	

	def __str__(self):
		return self.product_name

class ProductImage(models.Model):
	adminUser_id =models.ForeignKey(adminUser,null=True,on_delete= models.CASCADE)
	product_id = models.ForeignKey(Product,null=True,on_delete=models.CASCADE)
	product_image = models.FileField(upload_to='product/images',null=True, blank=True,default="pizzriea.JPG")


	def __str__(self):
		return self.product_id.product_name

class retailer_FeedBack(models.Model):
    retailer_id=models.ForeignKey(adminUser,on_delete=models.CASCADE)
    review=models.CharField(max_length=1000)
    overall_experience=models.CharField(max_length=20)
    timely_response=models.CharField(max_length=30)
    our_support=models.CharField(max_length=30)
    overall_setisfaction=models.CharField(max_length=30)
    suggestion=models.CharField(max_length=1000,blank=True)
    view=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True,blank=False)
    updated_at=models.DateTimeField(auto_now=True,blank=False)
