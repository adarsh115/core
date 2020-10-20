from django.contrib import admin

from website.models import *


admin.site.register(WebSettings)
admin.site.register(SKU)


class FaqCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

admin.site.register(FaqCategory)


class FaqItemAdmin(admin.ModelAdmin):
    list_display = ['question', 'department']
admin.site.register(FaqItem)
admin.site.register(WishlistItem)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'image']

admin.site.register(Department, DepartmentAdmin)
admin.site.register(ProductImage)








