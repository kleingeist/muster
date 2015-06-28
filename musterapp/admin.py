from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Page, Volume, PageColor, Pattern, VolumeCategory, Vector, Professional

admin.site.register(VolumeCategory)

class VolumeAdmin(admin.ModelAdmin):
    list_display = ("record_id", "title", "category")

admin.site.register(Volume, VolumeAdmin)


# class PageColorInline(admin.TabularInline): 
#     model = Page.colors.through

from sorl.thumbnail.admin import AdminImageMixin
class PageAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ("record_id", "volume", "page_number")
    list_filter = ("volume", )
    readonly_fields = ("image", "image_name", "image_width", "image_height")

    # inlines = (PageColorInline,)


class ProfessionalInline(admin.StackedInline):
    model = Professional
    can_delete = False
    verbose_name_plural = 'professional'


class UserAdmin(UserAdmin):
    inlines = (ProfessionalInline, )

admin.site.register(Page, PageAdmin)

admin.site.register(Pattern)

admin.site.register(Vector)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
