from django.contrib import admin
from .models import CustomUser,sender_name,sender_number

admin.site.register(CustomUser)
admin.site.register(sender_number)
admin.site.register(sender_name)
