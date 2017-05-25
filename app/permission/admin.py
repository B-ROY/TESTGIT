#encoding=utf-8

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin,GroupAdmin
from app.permission.models import *
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext, ugettext_lazy as _


from django.http import HttpResponseRedirect


class CooperateGameAdmin(admin.ModelAdmin):
    list_display = ('game_id', 'game_name',)


class NewUserAdmin(UserAdmin):

    actions = ["delete_selected","change_user_perms"]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    def change_user_perms(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect("/perm/user/edit?uid=%s" % (",".join(selected)))

    change_user_perms.short_description = u"调整权限"


class NewGroupAdmin(GroupAdmin):

    actions = ["delete_selected","change_group_perms"]

    def change_group_perms(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect("/perm/group/edit?gid=%s" % (",".join(selected)))
    change_group_perms.short_description = u"调整权限"


admin.site.unregister(User)
admin.site.register(User,NewUserAdmin)
admin.site.unregister(Group)
admin.site.register(Group,NewGroupAdmin)
admin.site.register(CooperateGame, CooperateGameAdmin)

