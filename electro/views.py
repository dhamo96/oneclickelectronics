from django.core import paginator
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password,check_password
from .models import *
from inventory.models import *
from .utils import *
from django.contrib import messages
import random
from django.db.models import Count
from django.conf import settings
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse, request
from django.core.paginator import Page,Paginator


products = Product.objects.all()
# Create your views here.
def home(request):
	p = Paginator(products,4)
	page=request.GET.get('page')
	all_product=p.get_page(page)

	if 'email' in request.session:
		user = registration.objects.get(email=request.session['email'])
		wishlist_id = Wishlist.objects.filter(customer_id=user)
		cart_id = Cart.objects.filter(customer_id=user,status="pending")
		cart_count = Cart.objects.filter(customer_id=user,status="pending").count()
		return render(request,'home.html',{'cart_id':cart_id,'wishlist_id':wishlist_id,'user':user,'products':all_product,'cart_count':cart_count})
	else:
		return render(request,'home.html',{'products':all_product})

def account(request):
	if 'email' in request.session:
		user = registration.objects.get(email=request.session['email'])
		wishlist_id = Wishlist.objects.filter(customer_id=user)
		cart_count = Cart.objects.filter(customer_id=user,status="pending").count()
		cart_id = Cart.objects.filter(customer_id=user,status="pending")
		order_details = Cart.objects.filter(customer_id = user,status="paid")
		try:
			if request.method=='POST':
				fname = request.POST['fname']
				lname = request.POST['lname']
				email = request.POST['uemail']
				age = request.POST['age']
				phone = request.POST['phone']
				landmark = request.POST['landmark']
				area = request.POST['area']
				city = request.POST['city']
				state = request.POST['state']
				zipcode = request.POST['zipcode']
				country = request.POST['country']
				user.first_name = fname
				user.last_name = lname
				user.email = email
				user.age = age
				user.mobile_number = phone
				user.landmark = landmark
				user.area = area
				user.city = city
				user.state = state
				user.zipcode = zipcode
				user.country = country
				if 'profilepic' in request.FILES:
					profilepic = request.FILES['profilepic']
					user.profile_pic = profilepic
				else:
					pass
				user.save()
				messages.success(request,"Details updated successfully ")
				return render(request,'accounts/account.html',{'order_details':order_details,'cart_id':cart_id,'wishlist_id':wishlist_id,'cart_count':cart_count,'user':user})
			else:
				return render(request,'accounts/account.html',{'order_details':order_details,'cart_id':cart_id,'user':user,'wishlist_id':wishlist_id,'cart_count':cart_count})
		except:
			return render(request,'accounts/account.html',{'order_details':order_details,'cart_id':cart_id,'user':user,'wishlist_id':wishlist_id,'cart_count':cart_count})
	else:
		return render(request,'accounts/login.html')

def login(request):
	if request.method == 'POST':
		username = request.POST['email']
		password = request.POST['password']
		user = registration.objects.filter(email=username)
		if user:
			user = registration.objects.get(email=username)
			pwd = check_password(password, user.password)
			if pwd:
				request.session['email'] = username
				request.session['name']=user.first_name
				return redirect('home')
			else:
				msg = "Incorrect password"
				return render(request,'accounts/login.html',{'msg':msg})
		else:
			msg = "User does not exist"
			return render(request,'accounts/login.html',{'msg':msg})

	return render(request,'accounts/login.html')

def logout(request):
	if 'email' in request.session:
		del request.session['email']
		del request.session['name']
		return redirect('home')
	else:
         return redirect('login')

def register(request):
	if request.method == 'POST':
		uname = request.POST['fname']
		lname = request.POST['lname']
		uemail = request.POST['email']
		phone = request.POST['phone']
		upassword = request.POST['password']
		cpassword = request.POST['cpass']
		user = registration.objects.filter(email=uemail)
		if user:
			error = "Email is already registered"
			return render(request,'accounts/register.html',{'msg':error})
		else:
			user = registration.objects.filter(email=uemail)
			if user:
				error = "Email is already registered with admin"
				return render(request,'accounts/register.html',{'msg':error})
			else:
				if upassword == cpassword:
					pwd = make_password(upassword)
					otp = random.randint(111111,999999)
					data = registration.objects.create(first_name = uname,last_name = lname,email = uemail,password = pwd,otp=otp,mobile_number=phone)
					sendmail( "Thank you for registering our site","accounts/email_template",uemail,{'name':uname,'otp':otp})
					return redirect('login')
				else:
					errmsg = "Password does not match"
					return render(request,'accounts/register.html',{'msg':errmsg})
	else:
		pass
	return render(request,'accounts/register.html')

def forgot_password(request):
	if request.method == 'POST':
		username = request.POST['email']
		user = registration.objects.filter(email=username)
		if user:
			user = registration.objects.get(email=username)
			otp = random.randint(111111,999999)
			user.otp = otp
			user.save()
			messages.success(request,"Email sent successfully")
			sendmail( "Reset Password ","accounts/reset_password",username,{'name':username,'otp':otp})
			return render(request,'accounts/generate_otp.html',{'email':username})
		else:
			msg = "User does not exist"
			return render(request,'accounts/forgot-password.html',{'msg':msg})
	return render(request,'accounts/forgot-password.html')

def otpValidation(request):
	if request.method=='POST':
		email = request.POST['email']
		otp=request.POST['otp']
		uid=registration.objects.get(email=email)
		if uid.otp==int(otp):
			return render(request,'accounts/change-password.html',{'email':email})
		else:
			msg="Invalid OTP "
			return render(request,'accounts/generate_otp.html',{'msg':msg})
	else:
		pass
	return render(request,'accounts/generate_otp.html')
 
def change_password(request):
	if request.method == 'POST':
		email = request.POST['email']
		passwd = request.POST['cpass']
		cpasswd = request.POST['retypepass']
		if passwd == cpasswd:
			pwd = make_password(passwd)
			user = registration.objects.get(email=email)
			user.password = pwd
			user.save()
			messages.success(request,"Password changed successfully, now login!")
			return redirect('login')
		else:
			pass		
	return render(request,'accounts/change-password.html')

def changePassword(request):
	if 'email' in request.session:
		user = registration.objects.get(email=request.session['email'])
		cart_count = Cart.objects.filter(customer_id=user,status="pending").count()
		if request.method == 'POST':
			current_pass = request.POST['oldpass']
			new_pass = request.POST['newpass']
			retype_pass = request.POST['retypepass']
			cpass = check_password(current_pass,user.password)
			if cpass:
				if new_pass == retype_pass:
					pwd = make_password(new_pass)
					user.password = pwd
					user.save()
					messages.success(request,"Password changed successfully ")
					return render(request,'accounts/account.html',{'cart_count':cart_count,'user':user})
				else:
					messages.error(request,"New password and re-type password incorrect")
					return render(request,'accounts/account.html',{'cart_count':cart_count,'user':user})
			else:
				messages.error(request,"Old password incorrect")
				return render(request,'accounts/account.html',{'cart_count':cart_count,'user':user})
		else:
			return render(request,'accounts/account.html',{'cart_count':cart_count,'user':user})
	else:
		return redirect('login')

def product_view(request,pk):
	category = Category.objects.all()
	product=Product.objects.get(id=pk)
	product_images = ProductImage.objects.filter(product_id=product)
	# products = Product.objects.filter(c_id=pk)
	if 'email' in request.session:
		user = registration.objects.get(email=request.session['email'])
		wishlist_id = Wishlist.objects.filter(customer_id=user)
		cart_id = Cart.objects.filter(customer_id=user,status="pending")
		cart_count = Cart.objects.filter(customer_id=user,status="pending").count()
		return render(request,'product_pages/product_view.html',{'cart_id':cart_id,'cart_count':cart_count,'wishlist_id':wishlist_id,'product':product,'category':category,'user':user,'product_images':product_images})
	else:
		return render(request,'product_pages/product_view.html',{'product':product,'category':category,'product_images':product_images})

def product_list(request,pk):
	products_count = Product.objects.all().count()
	categories = Category.objects.annotate(product_count =Count('product'))
	categoryId = Category.objects.get(category_id=pk)
	products_list = Product.objects.filter(c_id=pk)
	productsCount = Product.objects.filter(c_id=pk).count()
	p = Paginator(products_list,6)
	page=request.GET.get('page')
	all_product=p.get_page(page)
	context = {
		'products':all_product,
		'categoryId':categoryId,
		'categories':categories,
		'products_count':products_count,
		'productsCount':productsCount
	}
	if 'email' in request.session:
		user = registration.objects.get(email=request.session['email'])
		wishlist_id = Wishlist.objects.filter(customer_id=user)
		wishlist_count = Wishlist.objects.filter(customer_id=user).count()
		cart_id = Cart.objects.filter(customer_id=user,status="pending")
		cart_count = Cart.objects.filter(customer_id=user,status="pending").count()
		context = {
		'wishlist_id':wishlist_id,
		'wishlist_count':wishlist_count,
		'user':user,
		'products':all_product,
		'categoryId':categoryId,
		'categories':categories,
		'products_count':products_count,
		'productsCount':productsCount,
		'cart_count':cart_count,
		'cart_id':cart_id
		}
		return render(request,'product_pages/product_list.html',context)
	else:
		pass
	return render(request,'product_pages/product_list.html',context)

def addToWishlist(request,pk):
	if 'email' in request.session:
		user = registration.objects.get(email=request.session['email'])
		wishlist_item = Product.objects.get(id=pk)
		wishlist_id = Wishlist.objects.filter(customer_id=user)
		cart_count = Cart.objects.filter(customer_id=user,status="pending").count()
		lst=[]
		if wishlist_id:
			for i in wishlist_id:
				lst.append(i.product_Id)
			if wishlist_item in lst:
				messages.error(request,"Product is already in wishlist")
				return redirect('wishlist')
			else:
				wid = Wishlist.objects.create(customer_id=user,product_Id=wishlist_item)
				wishlist_id = Wishlist.objects.filter(customer_id=user)
				messages.success(request,"Product added successfully in wishlist")
				return redirect('wishlist')
		else:
			wid = Wishlist.objects.create(customer_id=user,product_Id=wishlist_item)
			wishlist_id = Wishlist.objects.filter(customer_id=user)
			messages.success(request,"Product added successfully in wishlist")
			return redirect('wishlist')

	else:
		return redirect('login')

def addToCart(request,pk):
	if 'email' in request.session:
		user = registration.objects.get(email=request.session['email'])
		cart_item = Product.objects.get(id=pk)
		retail_id = cart_item.adminUser_id
		cart_id = Cart.objects.filter(customer_id=user,status="pending")
		cart_count = Cart.objects.filter(customer_id=user,status="pending").count()
		lst=[]
		if cart_id:
			for i in cart_id:
				lst.append(i.product_Id)
			if cart_item in lst:
				messages.error(request,"Product is already in cart")
				return redirect('cart')
			else:
				cid = Cart.objects.create(customer_id=user,product_Id=cart_item,price=cart_item.price,retailer_Id=retail_id)
				cart_id = Cart.objects.filter(customer_id=user)
				messages.success(request,"Product added successfully in cart")
				return redirect('cart')
		else:
			cid = Cart.objects.create(customer_id=user,product_Id=cart_item,price=cart_item.price,retailer_Id=retail_id)
			cart_id = Cart.objects.filter(customer_id=user)
			messages.success(request,"Product added successfully in cart")
			# wishlist_id = Wishlist.objects.get(product_Id=pk)
			# wishlist_id.delete()
			return redirect('cart')
	else:
		return redirect('login')

def cart(request):
	total_price=0
	if 'email' in request.session:
		user = registration.objects.get(email=request.session['email'])
		cart_id = Cart.objects.filter(customer_id=user,status="pending")
		
		cart_count = Cart.objects.filter(customer_id=user,status="pending").count()
		wishlist_id = Wishlist.objects.filter(customer_id=user)
		wishlist_id.delete()
		for i in cart_id:
			total_price=total_price+i.price
		return render(request,'product_pages/cart.html',{'cart_count':cart_count,'cart_id':cart_id,'user':user,'wishlist_id':wishlist_id,'total_price':total_price})
	else:
		return redirect('login')

def wishlist(request):
	if 'email' in request.session:
		user = registration.objects.get(email=request.session['email'])
		wishlist_id = Wishlist.objects.filter(customer_id=user)
		cart_id = Cart.objects.filter(customer_id=user,status="pending")
		cart_count = Cart.objects.filter(customer_id=user,status="pending").count()
		return render(request,'product_pages/wishlist.html',{'cart_id':cart_id,'wishlist_id':wishlist_id,'user':user,'cart_count':cart_count})
	else:
		return redirect('login')

def deleteWishlist(request,pk):
	if 'email' in request.session:
		user = registration.objects.get(email=request.session['email'])
		wishlist_id = Wishlist.objects.get(product_Id=pk)
		wishlist_id.delete()
		return redirect('home')
	else:
		return redirect('login')

def deleteCartItem(request,pk):
	if 'email' in request.session:
		user = registration.objects.get(email=request.session['email'])
		cart_id = Cart.objects.get(id=pk)
		cart_id.delete()
		messages.success(request,"Product removed successfully from cart")
		return redirect('cart')
	else:
		return redirect('login') 

def clear_shopping_cart(request):
	if 'email' in request.session:
		user = registration.objects.get(email=request.session['email'])
		cart_id = Cart.objects.all()
		cart_id.delete()
		return redirect('cart')
	else:
		return redirect('login')

def checkout(request):
	total_price=0
	if 'email' in request.session:
		user = registration.objects.get(email=request.session['email'])
		wishlist_count = Wishlist.objects.filter(customer_id=user).count()
		cart_id = Cart.objects.filter(customer_id=user,status="pending")
		cart_count = Cart.objects.filter(customer_id=user,status="pending").count()
		for p in cart_id:
			total_price=total_price+p.price
			rid = p.retailer_Id
		if request.method == 'POST':
			username = request.POST['userid']
			amount = int(request.POST['amount'])
			return redirect('initiate_payment',{'cart_id':cart_id,'wishlist_count':wishlist_count,'cart_count':cart_count,'user':user,'username':username,'amount':amount,'rid':rid})
		else:
			return render(request,'product_pages/checkout.html',{'total_price':total_price,'cart_id':cart_id,'wishlist_count':wishlist_count,'cart_count':cart_count,'user':user,'rid':rid})
	else:
		return redirect('login')

def initiate_payment(request):
	c_id=request.POST['userid']
	username=registration.objects.get(id=c_id)
	amount=int(request.POST['amount'])
	notes = request.POST['message']
	cartid = Cart.objects.filter(customer_id=c_id,status="pending")
		
	for i in cartid:
		i.status='paid'
		i.save()
		
	transaction = Transaction.objects.create(order_notes=notes,made_by=username, amount=amount)
	transaction.save()
	merchant_key = settings.PAYTM_SECRET_KEY
	params = (
                ('MID', settings.PAYTM_MERCHANT_ID),
                ('ORDER_ID', str(transaction.order_id)),
                ('CUST_ID', str(transaction.made_by.email)),
                ('TXN_AMOUNT', str(transaction.amount)),
                ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
                ('WEBSITE', settings.PAYTM_WEBSITE),
                # ('EMAIL', request.user.email),
                # ('MOBILE_N0', '9911223388'),
                ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
                ('CALLBACK_URL', 'http://127.0.0.1:8000/oneclick/callback/'),
                # ('PAYMENT_MODE_ONLY', 'NO'),
            )

	paytm_params = dict(params)
	checksum = generate_checksum(paytm_params, merchant_key)

	transaction.checksum = checksum
	transaction.save()

	paytm_params['CHECKSUMHASH'] = checksum
	print('SENT: ', checksum)
	return render(request, 'payment/redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
	
	if request.method == 'POST':
		paytm_checksum = ''
		print(request.body)
		print(request.POST)
		received_data = dict(request.POST)
		print(received_data)
		paytm_params = {}
		paytm_checksum = received_data['CHECKSUMHASH'][0]
		for key, value in received_data.items():
			if key == 'CHECKSUMHASH':
				paytm_checksum = value[0]
			else:
				paytm_params[key] = str(value[0])
		# Verify checksum
		is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))		
		orderid = received_data['ORDERID']
		s = str(orderid)
		n= s[2:]
		final = n[:-2]
		tid = Transaction.objects.get(order_id=final)
		tid.status="Paid"
		tid.save()  
		otp=random.randint(111111,999999)
		tid.ord_deliver_otp=otp
		tid.save()
		if is_valid_checksum:
			print("Checksum Matched")
			received_data['message'] = "Checksum Matched"
			if received_data['STATUS'] == ['TXT_SUCCESS']:
				return render(request,"payment/payment_result.html",{'tid':tid,'context':received_data})
			else:
				print("Checksum Mismatched")
				received_data['message'] = "Checksum Mismatched"
		return render(request,"payment/payment_result.html",{'tid':tid,'context':received_data})

def search_product(request):
	products_count = Product.objects.all().count()
	categories = Category.objects.annotate(product_count =Count('product'))
	if request.method == "POST":
		item=request.POST['item_product']
		all_products=Product.objects.all()
		sid=shop_detail.objects.all()
		catid=Category.objects.all()
		all_prod=[]
		for i in all_products:
			if item.lower() in i.product_name.lower():
				all_prod.append(i)
		if 'email' in request.session:
			user = registration.objects.get(email=request.session['email'])
			wishlist_id = Wishlist.objects.filter(customer_id=user)
			wishlist_count = Wishlist.objects.filter(customer_id=user).count()
			cart_id = Cart.objects.filter(customer_id=user,status="pending")
			cart_count = Cart.objects.filter(customer_id=user,status="pending").count()
			context = {
			'wishlist_id':wishlist_id,
			'wishlist_count':wishlist_count,
			'user':user,
			'products':products,
			'categories':categories,
			'products_count':products_count,
			'cart_count':cart_count,
			'cart_id':cart_id,
			"all_prod":all_prod,
			"catid":catid,
			"sid":sid,
			}
			return render(request,'product_pages/search_product.html',context)
		else:	
			return render(request,'product_pages/search_product.html',{"categories":categories,"products_count":products_count,'catid':catid,'sid':sid,'all_prod':all_prod})
	else:
		return render(request,'home.html',{'products':products})

def update_qty(request):
	total_price=0
	if request.method=="POST":
		product_id = int(request.POST.get('product_id'))
		cid=registration.objects.get(email=request.session['email'])
		if(Cart.objects.filter(customer_id=cid,product_Id=product_id)):
			qty=int(request.POST.get('product_qty'))
			# print(qty)
			cart=Cart.objects.get(product_Id=product_id,customer_id=cid)
			cart.quantity=qty
			pid=Product.objects.get(id=product_id)
			total=qty*pid.price
			cart.price=total
			cart.save()
			cart_id = Cart.objects.filter(customer_id=cid,status="pending")
			for p in cart_id:
				total_price=total_price+p.price
			data={
                'status':'updated successfully',
                'total':total,
				'total_price':total_price,
            }
			return JsonResponse(data)
	return redirect('/')