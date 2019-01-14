from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.models import UserPro
from django.contrib.auth.models import User

# Register your models here.
class UserProLine(admin.StackedInline):
    model = UserPro
    can_delete = False
    verbose_name_plural = '扩展信息'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProLine,)


admin.site.unregister(User)
admin.site.register(User,UserAdmin)
