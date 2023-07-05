from django.contrib import admin
from paypal.standard.ipn.models import PayPalIPN
# Register your models here.
from .models import Course,Category,Course_content,Payment

admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Course_content)
admin.site.register(Payment)
