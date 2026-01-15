from django.contrib import admin

# Register your models here.
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_envoi')
    list_filter = ('date_envoi',)
    search_fields = ('email', 'message')
