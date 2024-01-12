from django.contrib import admin

# Register your models here.
from . models import KBKform
class BKB_Admin(admin.ModelAdmin):
    list_display = ('Name','Email','Phone_no','Url','Company','Date')

admin.site.register(KBKform,BKB_Admin)