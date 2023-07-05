from django.db import models
from django.utils import timezone
from accounts.models import Account
# Create your models here.

    
class Student(models.Model):
    student_id = models.ForeignKey(Account,on_delete=models.CASCADE)
    name = models.CharField(max_length=40,default='')

    def __str__(self):
        return self.name

class Teacher(models.Model):
    teacher_id = models.ForeignKey(Account,on_delete=models.CASCADE)
    name = models.CharField(max_length=40,default='')

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=40, primary_key=True)

    def __str__(self):
        return self.name
    
class Course(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    course_post_date = models.DateTimeField(default=timezone.now)
    teacher = models.ForeignKey(Teacher,  on_delete=models.CASCADE,null=True, blank=True)
    category = models.ForeignKey(Category,  on_delete=models.CASCADE,null=True, blank=True)
    body = models.TextField(null=True)
    duration = models.DurationField(null=True)

    def __str__(self):
        return self.name

def upload_location(instance,filename):
    file_path = 'course_contents/{course_name}/{course_id}-{name}-{filename}'.format(
        course_name=str(instance.course_id.name),course_id=str(instance.course_id.id),name=instance.name, filename=filename)
    return file_path

class Course_content(models.Model):
    content = models.FileField(upload_to=upload_location, null=True)
    name = models.CharField(max_length=200)
    body = models.TextField()
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name

class Payment(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    payment_price = models.IntegerField(null=True)
    invoice_number = models.CharField(max_length=100,null=True)

    def __str__(self):
        return f"{self.student_id}{self.course_id}{self.payment_price}{self.date}"

