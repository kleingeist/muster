from django.contrib import admin

from .models import Page, Volume, PageColor

class VolumeAdmin(admin.ModelAdmin):
    list_display = ("record_id", "title", "object_name") 

admin.site.register(Volume, VolumeAdmin)


# class PageColorInline(admin.TabularInline): 
#     model = Page.colors.through

from sorl.thumbnail.admin import AdminImageMixin
class PageAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ("record_id", "volume", "number")
    list_filter = ("volume", )
    readonly_fields = ("image", "image_meta",
                       "image_name", "image_width", "image_height")

    # inlines = (PageColorInline,)

admin.site.register(Page, PageAdmin)

