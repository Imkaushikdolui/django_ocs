import os
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render , redirect,get_object_or_404
from .models import Course,Teacher,Student,Course_content,Payment
from accounts.models import Account
from base.forms import CourseForm,CourseContentForm
from django.views.generic import CreateView

from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm
from datetime import date,datetime
import uuid
from django.db.models import Q,Sum, Count
from django.core.mail import send_mail
from online_course.settings import EMAIL_HOST_USER


def home(request):
    course = Course.objects.all()
    return render(request, 'base/homepage.html',{'course':course})

def welcomepage(request):
    if request.user.role == 'admin':
        return redirect('base:adashboard')
    elif request.user.role == 'teacher':
        return redirect('base:tdashboard')
    elif request.user.role == 'student':
        return redirect('base:sdashboard')

def studentdashboard(request):
    course = Course.objects.all()
    return render(request, 'base/studentdashboard.html',{'course':course})


def admindashboard(request):
    course = Course.objects.all()
    return render(request, 'base/admindashboard.html',{'course':course})
        

def teacherdashboard(request):
    user = request.user # Retrieve the logged-in user directly
    
    try:
        teacher = get_object_or_404(Teacher, teacher_id_id=user.id)
        course = Course.objects.filter(teacher=teacher)
    except Teacher.DoesNotExist:
        return redirect('base:sdashboard')
    
    context = {
        'teacher': teacher,
        'course': course
    }
    return render(request, 'base/teacherdashboard.html', context)



def create_course(request, teacher_id):
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = teacher
            course.save()

            # Get the enrolled students for the teacher
            enrolled_students = Payment.objects.filter(teacher_id=teacher).values_list('student_id__student_id__email', flat=True)

            # Send email to each enrolled student
            for student_email in enrolled_students:
                subject = 'New Course Available'
                message = f"Dear student, a new course '{course.name}' has been created by {teacher.name}. Check it out!"
                from_email = EMAIL_HOST_USER
                to_email = student_email
                send_mail(subject, message, from_email, [to_email])

            return redirect('base:tdashboard')
    else:
        form = CourseForm()

    context = {
        'form': form,
    }
    return render(request, 'base/create_course.html', context)


def update_course(request,pk):
    course = Course.objects.get(id=pk)
    form = CourseForm(instance=course)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('base:tdashboard')
    context = {
        'course': course,
        'form' : form
        }
    return render(request,'base/update_course.html', context)

def delete_course(request,pk):
    obj = Course.objects.get(id=pk)
    obj.delete()
    return redirect('base:tdashboard')


def course_details(request, pk):
    course = get_object_or_404(Course, pk=pk)
    content = Course_content.objects.filter(course_id=course)

    context = {
        'course': course,
        'content': content,
    }
    return render(request, 'base/course_details.html', context)


def add_course_content(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        content_form = CourseContentForm(request.POST, request.FILES)
        if content_form.is_valid():
            content_item = content_form.save(commit=False)
            content_item.course_id = course
            content_item.save()

            enrolled_students = Payment.objects.filter(course_id=course).values_list('student_id__student_id__email', flat=True)

            subject = 'New Course Content Available'
            message = f"Dear student, new content has been added to the course '{course.name}'. Please login to your account to access it."
            from_email = EMAIL_HOST_USER  
            recipient_list = enrolled_students

            send_mail(subject, message, from_email, recipient_list)

            return redirect('base:course_details', pk=pk)
    else:
        content_form = CourseContentForm()

    context = {
        'form': content_form,
    }
    return render(request, 'base/add_course_content.html', context)

def update_course_content(request,pk,cc_id):
    course = get_object_or_404(Course, pk=pk)
    course_content = get_object_or_404(Course_content, pk=cc_id)
    form = CourseContentForm(instance=course_content)

    if request.method == 'POST':
        form = CourseContentForm(request.POST,request.FILES,instance=course_content)
        if form.is_valid():
            content_item = form.save(commit=False)
            content_item.course_id = course
            content_item.save()
            return redirect('base:course_details',pk=pk)

    context = {
        'course':course,
        'course_content':course_content,
        'form': form,
    }
    return render(request, 'base/update_course_content.html', context)

def delete_course_content(request,pk,cc_id):
    course = get_object_or_404(Course, pk=pk)
    course_content = get_object_or_404(Course_content, pk=cc_id)
    content_url = course_content.content.path

    course_content.delete()

    if os.path.exists(content_url):
        os.remove(content_url)
        
    return redirect('base:course_details',pk=pk)
    


# paypal payment integrations

def generate_invoice_number(prefix):
    # Generate a unique identifier
    unique_id = uuid.uuid4().hex
    # Get the current timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    # Combine the prefix, timestamp, and unique identifier
    invoice_number = '{}-{}-{}'.format(prefix, timestamp, unique_id)
    return invoice_number

def checkout(request,pk):
    course = get_object_or_404(Course, pk=pk)
    content = Course_content.objects.filter(course_id=course)

    host = request.get_host()
    invoice_number = generate_invoice_number('INV')
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': course.price,
        'item_name': course.name,
        'invoice': invoice_number,
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,reverse('base:paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,reverse('base:payment_completed')),
        'cancel_url': 'http://{}{}'.format(host,reverse('base:payment_failed')),
    }
    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

    # Store course information in session
    request.session['checkout_course_id'] = course.id
    request.session['invoice_number'] = invoice_number
    request.session['checkout_course_price'] = course.price


    context = {
        'course': course,
        'content': content,
        'paypal_payment_button': paypal_payment_button,
    }
    return render(request, 'base/s_course_details.html', context)

@login_required
def payment_completed(request):
    if request.user.is_authenticated:
        std_id = request.user.id
    if request.method == "GET":
            
            try:
                student = Student.objects.get(student_id=std_id)
                course_id = request.session.get('checkout_course_id')
                invoice_number = request.session.get('invoice_number')
                course_price = request.session.get('checkout_course_price')

                course = get_object_or_404(Course, id=course_id)
                payment = Payment.objects.create(
                    student_id=student,
                    teacher_id = course.teacher,
                    course_id=course,
                    date=timezone.now(),
                    payment_price=course_price,
                    invoice_number = invoice_number

                )
                payment.save()

                # Clear the session data
                del request.session['checkout_course_id']
                del request.session['invoice_number']
                del request.session['checkout_course_price']
            except Exception as e:
                print("Exception occurred while creating Payment instance:", str(e))

    return render(request,'base/payment_completed.html',{'course':course,'date':date,'invoice_number':invoice_number})

def payment_failed(request):
    return render(request,'base/payment_failed.html')

def enroll_courses(request, pk):
    student = Student.objects.get(student_id=pk)
    payments = Payment.objects.filter(student_id=student)
    course_ids = payments.values_list('course_id', flat=True)
    courses = Course.objects.filter(id__in=course_ids)

    context = {
        'student': student,
        'courses': courses,
    }
    return render(request, 'base/enroll_courses.html', context)

def enroll_course_details(request,pk):
    course = get_object_or_404(Course, pk=pk)
    content = Course_content.objects.filter(course_id=course)
    context = {
        'course': course,
        'content': content,
    }
    return render(request,'base/enroll_course_details.html',context)

def search(request):
    q = request.GET.get('q', '')
    courses = Course.objects.filter(
        Q(name__icontains=q) |
        Q(price__icontains=q) |
        Q(teacher__name__icontains=q) |
        Q(category__name__icontains=q)
    )

    return render(request, 'base/filter_course.html', {'courses': courses})

def teacher_stats(request, pk):
    teacher = Teacher.objects.get(teacher_id=pk)
    courses = Course.objects.filter(teacher_id=teacher).annotate(
        num_students=Count('payment__student_id', distinct=True),
        income=Sum('payment__payment_price')
    )

    context = {
        'teacher': teacher,
        'courses': courses,
    }

    return render(request, 'base/teacher_stats.html', context)
