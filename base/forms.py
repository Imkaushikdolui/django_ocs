from django import forms
from base.models import Course,Course_content

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        # fields = '__all__'
        fields = ('name', 'price', 'course_post_date', 'category', 'body', 'duration')

class CourseContentForm(forms.ModelForm):
    class Meta:
        model = Course_content
        fields = ['content', 'name', 'body']