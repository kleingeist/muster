from django.contrib import admin

from .models import Page, Volume, PageColor

class VolumeAdmin(admin.ModelAdmin):
    list_display = ("record_id", "title", "object_name") 

admin.site.register(Volume, VolumeAdmin)


# class PageColorInline(admin.TabularInline): 
#     model = Page.colors.through

class PageAdmin(admin.ModelAdmin):
    list_display = ("record_id", "volume", "number")
    list_filter = ("volume", )

    # inlines = (PageColorInline,)

admin.site.register(Page, PageAdmin)

