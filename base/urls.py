from django.urls import path,include
from . import views
from django.conf import settings    
from django.conf.urls.static import static  


app_name = 'base'

urlpatterns = [

    path('',views.home,name='home'),
    path('welcome/',views.welcomepage,name='welcome'),
    path('tdashboard/',views.teacherdashboard,name='tdashboard'),
    path('adashboard/',views.admindashboard,name='adashboard'),
    path('sdashboard/',views.studentdashboard,name='sdashboard'),
    path('create_course/<int:teacher_id>/',views.create_course,name='create_course'),
    path('update_course/<str:pk>/',views.update_course,name='update_course'),
    path('delete_course/<str:pk>/',views.delete_course,name='delete_course'),
    path('course_details/<str:pk>/',views.course_details,name='course_details'),
    # path('s_course_details/<str:pk>/',views.s_course_details,name='s_course_details'),
    path('add_course_content/<str:pk>/',views.add_course_content,name='add_course_content'),
    path('update_course_content/<str:pk>/<str:cc_id>/',views.update_course_content,name='update_course_content'),
    path('delete_course_content/<str:pk>/<str:cc_id>/',views.delete_course_content,name='delete_course_content'),

    path('paypal/', include("paypal.standard.ipn.urls")),
    path('checkout/<str:pk>/',views.checkout,name='checkout'),
    path('payment_completed/',views.payment_completed,name='payment_completed'),
    path('payment_failed/',views.payment_failed,name='payment_failed'),
    path('enroll_courses/<str:pk>/',views.enroll_courses,name='enroll_course'),
    path('enroll_courses_details/<str:pk>/',views.enroll_course_details,name='enroll_course_details'),
    path('search/', views.search, name='search'),
    path('teacher_stats/<str:pk>/',views.teacher_stats,name='teacher_stats'),



] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)