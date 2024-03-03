from django.contrib import admin

# Register your models here.
from . models import KBKform,signup_model
class BKB_Admin(admin.ModelAdmin):
    list_display = ('Name','Email','Phone_no','Url','Company','Date')

admin.site.register(KBKform,BKB_Admin)

#############################

admin.site.register(signup_model)
