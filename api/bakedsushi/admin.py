from django.contrib import admin
from .models import ContactListModel

class ContactListAdmin(admin.ModelAdmin):
    list_display = ['contact_id', 'firstname', 'lastname', 'contact_email', 'contact_number', 'message', 'created_at']

admin.site.register(ContactListModel, ContactListAdmin)