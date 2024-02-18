from django.contrib import admin

from .models import Card, Image


class CardAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'user')


admin.site.register(Card, CardAdmin)


# class ImageAdmin(admin.ModelAdmin):
#     list_display = ('path',)

# admin.site.register(Image, ImageAdmin)
