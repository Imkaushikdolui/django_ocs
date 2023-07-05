from django.shortcuts import render,redirect
from online_course.forms import UserForm
from django.contrib.auth import authenticate,login,logout

from django.core.mail import send_mail
from online_course.settings import EMAIL_HOST_USER
from accounts.models import Account

import random

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from base.models import Student,Teacher


#  user registration -->
@csrf_exempt
def Otpverify(request):
    if request.method == 'POST':
        userotp = request.POST.get('otp')
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        role = request.POST.get('role')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print("OTP:",userotp)
        if password1 == password2:
            form  = Account.objects.create_user(
                name = name,
                email = email,
                username = username,
                role = role,
                password = password1
            )
            if role == 'teacher':
                teacher = Teacher.objects.create(
                    teacher_id=form,
                    name = name
                )
                teacher.save()
            elif role == 'student':
                student = Student.objects.create(
                    student_id=form,
                    name = name
                )
                student.save()
            form.save()
    return JsonResponse({'otp' : 'otp'}, status=200 )

def Signup(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        role = request.POST.get('role')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if form.is_valid():
            # form.save()
            otp = random.randint(1000,9999)
            print("form is saved successfully")
            send_mail("TWO FACTOR AUTHENTICATION: ",f"VERIFY YOUR MAIL USING THIS OTP: {otp}",EMAIL_HOST_USER,[email],fail_silently=True)
            print("email sended successfully")
            context = {
                'name' : name,
                'email' : email,
                'username' : username,
                'role': role,
                'password1' : password1,
                'password2' : password2,
                'otp' : otp
            }
            return render(request, 'template/OTPverify.html' ,context)
        else:
            print("some error has occured")
    context= {
            'form': form
    }
    return render(request, 'signup.html', context)


# user login -->
@csrf_exempt
def LoginOtpVerify(request):
    
    if request.method == 'POST':
        userotp = request.POST.get('otp')
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        user = authenticate(request,username=username, password=password)
        print("OTP:",userotp)
        print(user)
        if user is not None:
            login(request,user)
            print("login done")
            return redirect("base:welcome")
        else:
            print("login failed")

    return JsonResponse({'otp' : 'otp'}, status=200 )


def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = Account.objects.get(username=username)
            email = user.email
            role = user.role
            print(f'{username} {password} {email} {role}')
        except Account.DoesNotExist:
            print("user does not exist")

        user = authenticate(request,username=username, password=password)
        print(user)
        if user is not None:
            otp = random.randint(1000,9999)
            print("form is saved successfully")
            send_mail("TWO FACTOR AUTHENTICATION: ",f"LOGIN USING THIS OTP: {otp}",EMAIL_HOST_USER,[email],fail_silently=True)
            print("email sended successfully")
            context = {
                    'otp' : otp,
                    'username' : username,
                    'password' : password,
                    'role': role
                }
            return render(request,'template/LoginOtpVerify.html' ,context)
        else:
            print("Invalid Entry")
    
    return render(request, 'login.html')

def Logout(request):
    logout(request)
    print("logout done")
    return redirect('/login')