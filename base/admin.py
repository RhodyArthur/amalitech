from django.contrib import admin
from .models import AccessKey, User

# Register your models here.
class AccessKeyAdmin(admin.ModelAdmin):
    readonly_fields = ('key_value', 'date_procured',)
    list_display = ['key_value','user','date_procured', 'expiry_date',]
    
admin.site.register(AccessKey, AccessKeyAdmin)
admin.site.register(User)