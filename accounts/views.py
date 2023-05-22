from django.shortcuts import redirect, render
from .forms import UserForm
from .models import User
from django.contrib import messages
# Create your views here.
def registerUser(request):
    if request.method=='POST':
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