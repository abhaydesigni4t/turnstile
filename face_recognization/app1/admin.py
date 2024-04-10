from django.contrib import admin
from .models import UserEnrolled,CustomUser,Notification,Upload_data,Orientation,Asset,check_changes,Exit,Site,company,timeschedule

admin.site.register(CustomUser)
admin.site.register(UserEnrolled)
admin.site.register(Notification)
admin.site.register(Upload_data)
admin.site.register(Orientation)
admin.site.register(Asset)
admin.site.register(check_changes)
admin.site.register(Exit)
admin.site.register(Site)
admin.site.register(company)
admin.site.register(timeschedule)