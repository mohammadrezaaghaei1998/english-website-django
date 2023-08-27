from django.contrib import admin
from .models import Package, Video, Purchase, UserPackage,ContactSubmission,UserInformation

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'hour', 'price')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'package')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'timestamp', 'successful')
    list_filter = ('successful', 'package')
    search_fields = ('user__username', 'package__name')

@admin.register(UserPackage)
class UserPackageAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'unlocked')
    list_filter = ('unlocked', 'package')
    search_fields = ('user__username', 'package__name')


admin.site.register(ContactSubmission)
admin.site.register(UserInformation)