from django.shortcuts import redirect, render
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User , UserProfile
from django.contrib import messages , auth
from .utils import detectUser
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from vendor.models import Vendor
# Create your views here.

#Restrict the vendor from accessing the customer page
# Restrict the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,"شما در حال حاضر در حساب کاربری خود هستید")
        return redirect ("dashboard")
    elif request.method=='POST':
        print(request.POST)
        form=UserForm(request.POST)
        if form.is_valid():
            # create user using the from
            #password=form.cleaned_data['password']
            #user= form.save(commit=False)
            #user.set_password(password)
            #user.role=User.CUSTOMER
            #user.save()
            #form.save()
            # create the user using create_user method
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user= User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role=User.CUSTOMER
            user.save()
            messages.success(request, "اکانت شما با موفقیت ثبت شد ")
            return redirect('registerUser')
        else:
            print(' invalid form')
            print(form.errors)

    else:
        form = UserForm()
    context={
        'form' : form,
    }
    return render(request,"accounts/registerUser.html",context)

def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request,"شما در حال حاضر در حساب کاربری خود هستید")
        return redirect ("dashboard")
    elif request.method == "POST":
        #store the data and create the user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid:
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user= User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role=User.VENDOR
            user.save()
            vendor =  v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, "اکانت داروخانه شما با موفقیت ثبت شد، برای تایید اکانت منتظر بمونید")
            return redirect("registerVendor")
        else:
            print ("invalid form")
            print (form.errors)

    else:
        form = UserForm()
        v_form=VendorForm()
    context = {
        'form' : form,
        'v_form' : v_form,
    }
    return  render(request, "accounts/registerVendor.html" , context)

def login(request):
    if request.user.is_authenticated:
        messages.warning(request,"شما در حال حاضر در حساب کاربری خود هستید")
        return redirect ("myAccount")
    if request.method == "POST":
        email = request.POST['email']
        password= request.POST ['password']
        user = auth.authenticate(email = email,password=password)
        if user is not None :
            auth.login(request,user)
            messages.success(request,"شما وارد شدید!")
            return redirect ("myAccount")
        else:
            messages.error(request,"اطلاعات نادرست است")
            return redirect ("login")
    return render(request,"accounts/login.html")

def logout(request):
    auth.logout(request)
    messages.info(request,"شما از اکانت کاربری خود خارج شدید")
    return redirect ("login")


@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return  render(request, "accounts/custDashboard.html")

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return  render(request, "accounts/vendorDashboard.html")


