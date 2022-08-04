from django.contrib import admin
from .models import CustomUser,sender_name,list_numbers,UserAPI,report

admin.site.register(CustomUser)
admin.site.register(list_numbers)
admin.site.register(sender_name)
admin.site.register(UserAPI)
admin.site.register(report)

