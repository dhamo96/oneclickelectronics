from django.shortcuts import render,redirect
from inventory.models import *
from electro.models import *
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from .utils import *
import random
from datetime import datetime
# Create your views here.
categories = Category.objects.all()
def index(request):
    if 'adminEmail' in request.session:
        user = adminUser.objects.get(adminEmail=request.session['adminEmail'])
        user_count = registration.objects.all().count()
        products = Product.objects.filter(adminUser_id=user)
        return render(request,'main.html',{'user':user,'user_count':user_count,'products':products,'categories':categories})
    else:
        return render(request,'adminAccounts/auth-sign-in.html')

def adminHome(request):
    if 'adminEmail' in request.session:
        if request.session['adminEmail']=='admin123@gmail.com':
            rid=adminUser.objects.filter(status='pending').count()
            customer_count = registration.objects.all().count()
            retailer_count = adminUser.objects.all().count()
            shops_count = shop_detail.objects.all().count()

            customer_view=registration.objects.filter(view=False).count()
            product_view=Product.objects.filter(view=False).count()
            retailer_view=adminUser.objects.filter(view=False).count()
            shop_view=shop_detail.objects.filter(view=False).count()
            total=customer_view+product_view+retailer_view+shop_view
            context={
                        'rid':rid,
                        'customer_count':customer_count,
                        'retailer_count':retailer_count,
                        'shops_count':shops_count,
                        'customer':customer_view,
                        'product':product_view,
                        'retailer':retailer_view,
                        'shop':shop_view,
                        'total':total,
                    }
            return render(request,'adminPanel/adminHome.html',{'ct':context})
        else:
            return render(request,'adminPanel/adminHome.html')
    else:
        return redirect('shopAdmin')
        
def admin_retailers_pending_request(request):
    if 'adminEmail' in request.session:
        if request.session['adminEmail']=='admin123@gmail.com':
            rid=adminUser.objects.filter(status='pending')   
            customer_view=registration.objects.filter(view=False).count()
            product_view=Product.objects.filter(view=False).count()
            retailer_view=adminUser.objects.filter(view=False).count()
            shop_view=shop_detail.objects.filter(view=False).count()
            total=customer_view+product_view+retailer_view+shop_view
            context={
                    'customer':customer_view,
                    'product':product_view,
                    'retailer':retailer_view,
                    'shop':shop_view,
                    'total':total,
                }
            return render(request,'adminPanel/retailers-pending-request.html',{'rid':rid,'ct':context})
        else:
            return render(request,'adminPanel/adminHome.html')
    else:
        return redirect('shopAdmin')

def admin_update_retailer_status(request,pk):
    if 'adminEmail' in request.session:
        if request.session['adminEmail']=='admin123@gmail.com':
            rid=adminUser.objects.get(id=pk)
            if request.method =='POST':
                status=request.POST['status']
                rid.status=status
                rid.save()
                customer_view=registration.objects.filter(view=False).count()
                product_view=Product.objects.filter(view=False).count()
                retailer_view=adminUser.objects.filter(view=False).count()
                shop_view=shop_detail.objects.filter(view=False).count()
                total=customer_view+product_view+retailer_view+shop_view
                context={
                            'customer':customer_view,
                            'product':product_view,
                            'retailer':retailer_view,
                            'shop':shop_view,
                            'total':total,
                        }
                rid=adminUser.objects.filter(status='pending')
                return render(request,'adminPanel/retailers-pending-request.html',{'rid':rid,'ct':context})
            else:
                return render(request,'adminPanel/retailers-pending-request.html',{'rid':rid})
        else:
            return render(request,'adminPanel/retailers-pending-request.html')
    else:
        return redirect('shopAdmin')

def admin_notification_retailer(request):
    if 'adminEmail' in request.session:
        if request.session['adminEmail']=='admin123@gmail.com':
            rid = adminUser.objects.filter(view=False)
            customer_view=registration.objects.filter(view=False).count()
            product_view=Product.objects.filter(view=False).count()
            retailer_view=adminUser.objects.filter(view=False).count()
            shop_view=shop_detail.objects.filter(view=False).count()
            total=customer_view+product_view+retailer_view+shop_view
            context={
                    'customer':customer_view,
                    'product':product_view,
                    'retailer':retailer_view,
                    'shop':shop_view,
                    'total':total,
                }
            return render(request,'adminPanel/notification-retailer.html',{'rid':rid,'ct':context})
        else:
            return render(request,'adminPanel/notification-retailer.html')
    else:
        return redirect('shopAdmin')

def shopAdmin(request):
    if request.method == 'POST':
        shopAdminEmail = request.POST['email']
        password = request.POST['pass']
        if shopAdminEmail == 'admin123@gmail.com' and password == 'admin123':
            request.session['adminEmail'] = 'admin123@gmail.com'
            return redirect('adminhome')
        else:
            return render(request,'adminPanel/shopAdmin.html')
    else:
        return render(request,'adminPanel/shopAdmin.html')

def adminlogin(request):
    if request.method == 'POST':
        user_email = request.POST['uemail']
        password = request.POST['upass']
        user = adminUser.objects.filter(adminEmail=user_email)
        if user:
            user = adminUser.objects.get(adminEmail=user_email)
            pwd = check_password(password, user.password)
            if pwd:
                request.session['adminEmail'] = user_email
                request.session['adminName']=user.adminName
                return redirect('index') 
            else:
                msg = "Incorrect password"
                return render(request,'adminAccounts/auth-sign-in.html',{'msg':msg})
        else:
            msg = "User does not exist"
            return render(request,'adminAccounts/auth-sign-in.html',{'msg':msg})
    return render(request,'adminAccounts/auth-sign-in.html')

def adminLogout(request):
    if 'adminName' in request.session:
        del request.session['adminEmail']
        del request.session['adminName']
        return render(request,'adminAccounts/auth-sign-in.html')
    else:
         return render(request,'adminAccounts/auth-sign-in.html')

def adminForgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = adminUser.objects.filter(adminEmail=email)
        if user:
            user = adminUser.objects.get(adminEmail=email)
            otp = random.randint(111111,999999)
            user.admin_otp = otp
            user.save()
            messages.success(request,"Email sent successfully")
            sendmail( "Reset Password ","adminAccounts/auth_reset_password",email,{'name':email,'otp':otp})
            return render(request,'adminAccounts/auth_generate_otp.html',{'email':email})
        else:
            msg = "User does not exist"
            return render(request,'adminAccounts/auth-recoverpass.html',{'msg':msg})
    return render(request,'adminAccounts/auth-recoverpass.html')

def adminOtpValidation(request):
	if request.method=='POST':
		email = request.POST['email']
		otp=request.POST['adminOtp']
		uid=adminUser.objects.get(adminEmail=email)
		if uid.admin_otp==int(otp):
			return render(request,'adminAccounts/AdminChange-password.html',{'email':email})
		else:
			msg="Invalid OTP "
			return render(request,'adminAccounts/auth-recoverpass.html',{'msg':msg})
	else:
		pass
	return render(request,'adminAccounts/auth_generate_otp.html')

def adminChangepassword(request):
    if request.method=='POST':
        email = request.POST['email']
        cpassword=request.POST['cpassword']
        repass = request.POST['repassword']
        if cpassword == repass:
            changePass = make_password(cpassword)
            user = adminUser.objects.get(adminEmail=email)
            user.password = changePass
            user.save()
            messages.success(request,"Password changed successfully..")
            return redirect('adminlogin')
        else:
            pass
    return render(request,'adminAccounts/AdminChange-password.html')

def adminRegister(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpass']
        user = adminUser.objects.filter(adminEmail=email)
        if user:
            errmsg = "Email is already exist"
            return render(request,'adminAccounts/auth-sign-up.html',{'msg':errmsg})
        else:
            if password == cpassword:
                pwd = make_password(password)
                otp = random.randint(111111,999999)
                data = adminUser.objects.create(adminName=name,adminEmail=email,password=pwd,admin_otp=otp)
                success = "Account created successfully"
                return render(request,'adminAccounts/auth-sign-up.html',{'success':success})
            else:
                errmsg = "Password does not match"
                return render(request,'adminAccounts/auth-sign-up.html',{'msg':errmsg})
    else:
        pass
    return render(request,'adminAccounts/auth-sign-up.html')

def adminProfile(request):
    if 'adminEmail' in request.session:
        user = adminUser.objects.get(adminEmail=request.session['adminEmail'])
        order_rid=Cart.objects.filter(status="paid",retailer_Id=user)
        print(type(order_rid))
        if request.method == 'POST':
            adminName = request.POST['firstname']
            adminLastName = request.POST['lastname']
            admin_Email = request.POST['email']
            adminPhone = request.POST['phonenumber']
            gender=request.POST['gender']
            rlandmark=request.POST['rlandmark']
            rcity=request.POST['rcity']
            rstate=request.POST['rstate']
            rcountry=request.POST['rcountry']
            rpincode=request.POST['rpincode']
            user.adminEmail = admin_Email
            user.adminName = adminName
            user.adminLastName = adminLastName
            user.adminPhone = adminPhone
            user.gender=gender
            user.home_address=rlandmark
            user.home_city=rcity
            user.home_state=rstate
            user.home_country=rcountry
            user.home_pincode=rpincode
            user.save()
            
            msg = "Details updated successfully"
            return render(request,'adminAccounts/adminProfile.html',{'msg':msg,'user':user,'order_rid':order_rid})
        else:
            return render(request,'adminAccounts/adminProfile.html',{'user':user,'order_rid':order_rid})
    else:
        return redirect('adminlogin')

def shopDetail(request):
    if 'adminEmail' in request.session:
        user = adminUser.objects.get(adminEmail=request.session['adminEmail'])
        order_rid=Cart.objects.filter(status="paid",retailer_Id=user)
        if request.method == 'POST':
            shop_name = request.POST['shopname']
            shop_type = request.POST['shoptype']
            owner_id_proof = request.FILES['idproof']
            elc_bill = request.FILES['ebill']
            shop_address = request.POST['slandmark']
            shop_country = request.POST['scountry']
            shop_state = request.POST['sstate']
            shop_city = request.POST['scity']
            shop_pincode = request.POST['spincode']
            shop_register = shop_detail.objects.create(owner_id=user,shop_name=shop_name,shop_type=shop_type,owner_id_proof=owner_id_proof,
            elc_bill=elc_bill,shop_address=shop_address,shop_country=shop_country,shop_state=shop_state,shop_city=shop_city,
            shop_pincode=shop_pincode)
            msg = "Details updated successfully"
            return render(request,'adminAccounts/adminProfile.html',{'msg':msg,'user':user,'order_rid':order_rid})
        else:
            return render(request,'adminAccounts/adminProfile.html',{'user':user,'order_rid':order_rid})
    else:
        return redirect('adminLogin')

def retailerUpdatePassword(request):
    if 'adminEmail' in request.session:
        user = adminUser.objects.get(adminEmail=request.session['adminEmail'])
        order_rid=Cart.objects.filter(status="paid",retailer_Id=user)
        if request.method == 'POST':
            current_pass = request.POST['currentpassword']
            new_pass = request.POST['newpassword']
            retype_pass = request.POST['retypenewpassword']
            cpass = check_password(current_pass,user.password)
            if cpass:
                if new_pass == retype_pass:
                    pwd = make_password(new_pass)
                    user.password = pwd
                    user.save()
                    msg = "Password Changed successfully"
                    return render(request,'adminAccounts/adminProfile.html',{'user':user,'msg':msg,'order_rid':order_rid})
                else:
                    errmsg = "New password and Re-type password incorrect"
                    return render(request,'adminAccounts/adminProfile.html',{'user':user,'errmsg':errmsg,'order_rid':order_rid})
            else:
                errmsg = "Incorrect Old password"
                return render(request,'adminAccounts/adminProfile.html',{'user':user,'errmsg':errmsg,'order_rid':order_rid})
        else:
            return render(request,'adminAccounts/adminProfile.html',{'user':user,'order_rid':order_rid})
    else:
        return redirect('adminLogin')

def retailer_change_profile_picture(request):
    if 'adminEmail' in request.session:
        user = adminUser.objects.get(adminEmail=request.session['adminEmail'])
        order_rid=Cart.objects.filter(status="paid",retailer_Id=user)
        if request.method == 'POST':
            if 'picture' in request.FILES:
                adminProfile_pics = request.FILES['picture']
                user.adminProfile_pic = adminProfile_pics
            else:
                pass
            user.save()
            msg = "Profile Picture updated successfully"
            return render(request,'adminAccounts/adminProfile.html',{'user':user,'msg':msg,'order_rid':order_rid})
        else:
            return render(request,'adminAccounts/adminProfile.html',{'user':user,'order_rid':order_rid})
    else:
        return redirect('adminlogin')

def product_upload(request):
    if 'adminEmail' in request.session:
        user = adminUser.objects.get(adminEmail=request.session['adminEmail'])
        sid = shop_detail.objects.get(owner_id=user)
        if user.status=='Approve':
            if request.method == 'POST':
                product_name = request.POST['product_name']
                product_category = request.POST['product_cat']
                product_price = request.POST['price']
                product_qty = request.POST['qty']
                product_pic = request.FILES['product_pic']
                product_desc = request.POST['desc']
                cat_id = Category.objects.get(category_name = product_category)
                data = Product.objects.create(adminUser_id=user,shop_id=sid,product_name=product_name,price=product_price,qty=product_qty,c_id=cat_id,desc=product_desc,product_pic=product_pic)
                messages.success(request,"Product added successfully")
                return redirect('product_list')
            else:
                categories = Category.objects.all()
                return render(request,'product/add-product.html',{'categories':categories,'user':user})
        else:
            categories = Category.objects.all()
            return render(request,'product/add-product.html',{'categories':categories,'user':user})
    else:
        return redirect('adminlogin')

def product_list(request):
    if 'adminEmail' in request.session:
        user = adminUser.objects.get(adminEmail=request.session['adminEmail'])
        products = Product.objects.filter(adminUser_id=user)
        if products:
            return render(request,'product/product_list.html',{'products':products,'user':user})
        else:
            return redirect('product-upload')
    else:
        # return redirect(request,'product/product_list.html')
        return redirect('adminlogin')

def adminProduct_view(request,pk):
    if 'adminEmail' in request.session:
        user = adminUser.objects.get(adminEmail=request.session['adminEmail'])
        product=Product.objects.get(id=pk)
        if product:
            return render(request,'product/productview.html',{'product':product,'user':user})
        else:
            pass
    else:
       return redirect('adminLogin')

def product_delete(request,pk):
    if 'adminEmail' in request.session:
        user = adminUser.objects.get(adminEmail=request.session['adminEmail'])
        product=Product.objects.get(id=pk)
        product.delete()
        messages.success(request,"Product Deleted successfully")
        return redirect('product_list')
    else:
       return redirect('adminLogin')

def customer_delete(request,pk):
    if 'adminEmail' in request.session:
        user = adminUser.objects.get(adminEmail=request.session['adminEmail'])
        customer=registration.objects.get(id=pk)
        customer.delete()
        messages.success(request,"Customer Deleted successfully")
        return redirect('customer-list')
    else:
       return redirect('adminLogin')

def adminProduct_edit(request,pk):
    if 'adminEmail' in request.session:
        user = adminUser.objects.get(adminEmail=request.session['adminEmail'])
        product=Product.objects.get(id=pk)
        if request.method == 'POST':
            productName = request.POST['product_name']
            productCat = request.POST['product_cat']
            productPrice = request.POST['price']
            productQty = request.POST['qty']
            productDesc = request.POST['desc']
            cat_id = Category.objects.get(category_name = productCat)
            product.product_name = productName
            product.price = productPrice
            product.c_id = cat_id
            product.desc = productDesc
            product.qty = productQty
            if 'product_pic' in request.FILES:
                productPic = request.FILES['product_pic']
                product.product_pic = productPic
            else:
                pass
            product.save()
            messages.success(request,"Product Updated successfully")
            return render(request,'product/product_edit.html',{'categories':categories,'product':product,'user':user})
        else:
            return render(request,'product/product_edit.html',{'product':product,'user':user})
    else:
        return redirect('adminLogin')

def customer_list(request):
    if 'adminEmail' in request.session:
        user = adminUser.objects.get(adminEmail=request.session['adminEmail'])
        customers = registration.objects.all()
        return render(request,'customers/customer-list.html',{'customers':customers,'user':user})
    else:
        # return redirect(request,'product/product_list.html')
        return redirect('adminlogin')

def customer_view(request,pk):
    if 'adminEmail' in request.session:
        user = adminUser.objects.get(adminEmail=request.session['adminEmail'])
        customers = registration.objects.get(id=pk)
        return render(request,'customers/customer_view.html',{'customers':customers,'user':user})
    else:
       return redirect('adminLogin')

def photo_upload(request,pk):
    if 'adminEmail' in request.session:
        user = adminUser.objects.get(adminEmail=request.session['adminEmail'])
        product=Product.objects.get(id=pk)
        if request.method == 'POST':
            product_images = request.FILES.getlist('product_image')
            for image in product_images:
                product_photos = ProductImage.objects.create(adminUser_id=user,product_id=product,product_image=image)
            messages.success(request,"Photos Added successfully")
            return render(request,'product/product_photo.html',{'user':user,'product':product})
        else:
            return render(request,'product/product_photo.html',{'user':user,'product':product})
    else:
        return redirect('adminLogin')

def view_all_retailers(request):
    if 'adminEmail' in request.session:
        if request.session['adminEmail']=='admin123@gmail.com':
            retailers = adminUser.objects.all()
            customer_view=registration.objects.filter(view=False).count()
            product_view=Product.objects.filter(view=False).count()
            retailer_view=adminUser.objects.filter(view=False).count()
            shop_view=shop_detail.objects.filter(view=False).count()
            total=customer_view+product_view+retailer_view+shop_view
            context = {
                     'retailers':retailers,
                     'customer':customer_view,
                     'product':product_view,
                     'retailer':retailer_view,
                     'shop':shop_view,
                     'total':total,
                }
            return render(request,'adminPanel/view-all-retailers.html',{'ct':context})
    else:
        return redirect('shopAdmin')

def admin_notification_retailer_view(request,pk):
    if 'adminEmail' in request.session:
        if request.session['adminEmail']=='admin123@gmail.com':
            rid=adminUser.objects.get(id=pk)
            rid.view=True
            rid.save()
            customer_view=registration.objects.filter(view=False).count()
            product_view=Product.objects.filter(view=False).count()
            retailer_view=adminUser.objects.filter(view=False).count()
            shop_view=shop_detail.objects.filter(view=False).count()
            total=customer_view+product_view+retailer_view+shop_view
            context = {
                     'customer':customer_view,
                     'product':product_view,
                     'retailer':retailer_view,
                     'shop':shop_view,
                     'total':total,
                }
            return render(request,'adminPanel/view-retailer-profile.html',{'rid':rid,'ct':context})
        else:
            return render(request,'adminPanel/view-retailer-profile.html')
    else:
        return redirect('shopAdmin')

def admin_notification_customer(request):
    if 'adminEmail' in request.session:
        if request.session['adminEmail']=='admin123@gmail.com':
            rid = adminUser.objects.filter(view=False)
            cid = registration.objects.filter(view=False)
            customer_view=registration.objects.filter(view=False).count()
            product_view=Product.objects.filter(view=False).count()
            retailer_view=adminUser.objects.filter(view=False).count()
            shop_view=shop_detail.objects.filter(view=False).count()
            total=customer_view+product_view+retailer_view+shop_view
            context={
                    'customer':customer_view,
                    'product':product_view,
                    'retailer':retailer_view,
                    'shop':shop_view,
                    'total':total,
                }
            return render(request,'adminPanel/notification-customer.html',{'cid':cid,'rid':rid,'ct':context})
        else:
            return render(request,'adminPanel/notification-customer.html')
    else:
        return redirect('shopAdmin')

def admin_view_retailer_profile(request,pk):
    if 'adminEmail' in request.session:
        if request.session['adminEmail']=='admin123@gmail.com':
            rid=adminUser.objects.get(id=pk)
            rid.view=True
            rid.save()
            order_rid=Cart.objects.filter(retailer_Id=rid,status='paid')
            order_count=Cart.objects.filter(retailer_Id=rid,status='paid').count()
            customer_view=registration.objects.filter(view=False).count()
            product_view=Product.objects.filter(view=False).count()
            retailer_view=adminUser.objects.filter(view=False).count()
            shop_view=shop_detail.objects.filter(view=False).count()
            total=customer_view+product_view+retailer_view+shop_view
            context = {
                     'customer':customer_view,
                     'product':product_view,
                     'retailer':retailer_view,
                     'shop':shop_view,
                     'total':total,
                     'order_rid':order_rid,
                     'order_count':order_count,
                }
            if rid:
                rsid=shop_detail.objects.filter(owner_id=pk)
                if rsid:
                    sid=shop_detail.objects.get(owner_id=pk)
                    
                    pid=Product.objects.filter(adminUser_id=pk)
                    if pid:
                        total_product=Product.objects.filter(adminUser_id=pk).count()
                        return render(request,'adminPanel/view-retailer-profile.html',{'order_rid':order_rid,'order_count':order_count,'rid':rid,'sid':sid,'pid':pid,'total_product':total_product,'ct':context})
                    else:
                        return render(request,'adminPanel/view-retailer-profile.html',{'order_rid':order_rid,'order_count':order_count,'rid':rid,'sid':sid,'ct':context})
                else:
                    return render(request,'adminPanel/view-retailer-profile.html',{'order_rid':order_rid,'order_count':order_count,'rid':rid,'ct':context})
        else:
            return render(request,'adminPanel/view-retailer-profile.html')
    else:
        return redirect('shopAdmin')   

def admin_view_customer_profile(request,pk):
    if 'adminEmail' in request.session:
        if request.session['adminEmail']=='admin123@gmail.com':
            cid=registration.objects.get(id=pk)
            cid.view=True
            cid.save()
            customer_view=registration.objects.filter(view=False).count()
            product_view=Product.objects.filter(view=False).count()
            retailer_view=adminUser.objects.filter(view=False).count()
            shop_view=shop_detail.objects.filter(view=False).count()
            total=customer_view+product_view+retailer_view+shop_view
            context={
                    'customer':customer_view,
                    'product':product_view,
                    'retailer':retailer_view,
                    'shop':shop_view,
                    'total':total,
                }
            return render(request,'adminPanel/view-customer-profile.html',{'cid':cid,'ct':context})
        else:
            return render(request,'adminPanel/view-customer-profile.html')
    else:
        return redirect('shopAdmin')

def admin_view_all_customers(request):
    if 'adminEmail' in request.session:
        if request.session['adminEmail']=='admin123@gmail.com':
            cid = registration.objects.all()
            customer_view=registration.objects.filter(view=False).count()
            product_view=Product.objects.filter(view=False).count()
            retailer_view=adminUser.objects.filter(view=False).count()
            shop_view=shop_detail.objects.filter(view=False).count()
            total=customer_view+product_view+retailer_view+shop_view
            context={
                    'customer':customer_view,
                    'product':product_view,
                    'retailer':retailer_view,
                    'shop':shop_view,
                    'total':total,
                }
            return render(request,'adminPanel/admin-view-all-customers.html',{'cid':cid,'ct':context})
        else:
            return render(request,'adminPanel/admin-view-all-customers.html')
    else:
        return redirect('shopAdmin')

def admin_notification_shop(request):
    if 'adminEmail' in request.session:
        if request.session['adminEmail']=='admin123@gmail.com':
            sid = shop_detail.objects.filter(view=False)
            customer_view=registration.objects.filter(view=False).count()
            product_view=Product.objects.filter(view=False).count()
            retailer_view=adminUser.objects.filter(view=False).count()
            shop_view=shop_detail.objects.filter(view=False).count()
            total=customer_view+product_view+retailer_view+shop_view
            context={
                    'customer':customer_view,
                    'product':product_view,
                    'retailer':retailer_view,
                    'shop':shop_view,
                    'total':total,
                }
            return render(request,'adminPanel/notification-shop.html',{'sid':sid,'ct':context})
        else:
            return render(request,'adminPanel/notification-shop.html')
    else:
        return redirect('shopAdmin')

def admin_notification_shop_view(request,pk):
    if 'adminEmail' in request.session:
        if request.session['adminEmail']=='admin123@gmail.com':
            sid=shop_detail.objects.get(id=pk)
            sid.view=True
            sid.save()
            pid=Product.objects.filter(adminUser_id=sid.owner_id)
            total_product=Product.objects.filter(adminUser_id=sid.owner_id).count()
            rid=adminUser.objects.get(id=sid.owner_id.id)
            customer_view=registration.objects.filter(view=False).count()
            product_view=Product.objects.filter(view=False).count()
            retailer_view=adminUser.objects.filter(view=False).count()
            shop_view=shop_detail.objects.filter(view=False).count()
            total=customer_view+product_view+retailer_view+shop_view
            context={
            'customer':customer_view,
            'product':product_view,
            'retailer':retailer_view,
            'shop':shop_view,
            'total':total,
            }
            return render(request,'adminPanel/view-retailer-profile.html',{'pid':pid,'ct':context,'rid':rid,'sid':sid,'total_product':total_product})
        else:
            return render(request,'adminPanel/view-retailer-profile.html')
    else:
        return redirect('shopAdmin')

def admin_view_all_products(request):
    if 'adminEmail' in request.session:
        if request.session['adminEmail']=='admin123@gmail.com':
            pid = Product.objects.all()
            customer_view=registration.objects.filter(view=False).count()
            product_view=Product.objects.filter(view=False).count()
            retailer_view=adminUser.objects.filter(view=False).count()
            shop_view=shop_detail.objects.filter(view=False).count()
            total=customer_view+product_view+retailer_view+shop_view
            context={
                    'customer':customer_view,
                    'product':product_view,
                    'retailer':retailer_view,
                    'shop':shop_view,
                    'total':total,
                }
            return render(request,'adminPanel/admin-view-all-products.html',{'pid':pid,'ct':context})
        else:
            return render(request,'adminPanel/admin-view-all-products.html')
    else:
        return redirect('shopAdmin')

def admin_view_all_shops(request):
    if 'adminEmail' in request.session:
        if request.session['adminEmail']=='admin123@gmail.com':
            shops = shop_detail.objects.all().prefetch_related('owner_id')
            customer_view=registration.objects.filter(view=False).count()
            product_view=Product.objects.filter(view=False).count()
            retailer_view=adminUser.objects.filter(view=False).count()
            shop_view=shop_detail.objects.filter(view=False).count()
            total=customer_view+product_view+retailer_view+shop_view
            context={
                    'customer':customer_view,
                    'product':product_view,
                    'retailer':retailer_view,
                    'shop':shop_view,
                    'total':total,
                }
            return render(request,'adminPanel/admin-view-all-shops.html',{'sid':shops,'ct':context})
        else:
            return render(request,'adminPanel/admin-view-all-shops.html')
    else:
        return redirect('shopAdmin')

def admin_view_product(request,pk):
    if 'adminEmail' in request.session:
        if request.session['adminEmail']=='admin123@gmail.com':
            pid = Product.objects.get(id=pk)
            pid.view=True
            pid.save()
            customer_view=registration.objects.filter(view=False).count()
            product_view=Product.objects.filter(view=False).count()
            retailer_view=adminUser.objects.filter(view=False).count()
            shop_view=shop_detail.objects.filter(view=False).count()
            total=customer_view+product_view+retailer_view+shop_view
            context={
                    'customer':customer_view,
                    'product':product_view,
                    'retailer':retailer_view,
                    'shop':shop_view,
                    'total':total,
                }
            return render(request,'adminPanel/admin-view-product.html',{'pid':pid,'ct':context})
        else:
            return render(request,'adminPanel/admin-view-product.html')
    else:
        return redirect('shopAdmin')

def admin_delete_product(request,pk):
    if 'adminEmail' in request.session:
        if request.session['adminEmail']=='admin123@gmail.com':
            pid = Product.objects.get(id=pk)
            pid.delete()
            messages.success(request,"Product Deleted successfully")
            return redirect('admin_view_all_products')
        else:
            return render(request,'adminPanel/admin-view-product.html')
    else:
        return redirect('shopAdmin')

def admin_notification_products(request):
    if 'adminEmail' in request.session:
        if request.session['adminEmail']=='admin123@gmail.com':
            pid = Product.objects.filter(view=False)
            customer_view=registration.objects.filter(view=False).count()
            product_view=Product.objects.filter(view=False).count()
            retailer_view=adminUser.objects.filter(view=False).count()
            shop_view=shop_detail.objects.filter(view=False).count()
            total=customer_view+product_view+retailer_view+shop_view
            context={
                    'customer':customer_view,
                    'product':product_view,
                    'retailer':retailer_view,
                    'shop':shop_view,
                    'total':total,
                }
            return render(request,'adminPanel/notification-product.html',{'pid':pid,'ct':context})
        else:
            return render(request,'adminPanel/notification-product.html')
    else:
        return redirect('shopAdmin')

def admin_delete_retailer(request,pk):
    if 'adminEmail' in request.session:
        if request.session['adminEmail']=='admin123@gmail.com':
            rid = adminUser.objects.get(id=pk)
            rid.delete()
            messages.success(request,"Retailer Deleted successfully")
            return redirect('view-all-retailers')
        else:
            return render(request,'adminPanel/view-all-retailers.html')
    else:
        return redirect('shopAdmin')