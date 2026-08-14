from django.contrib import admin
from .models import Credential, AuditEvent
@admin.register(Credential)
class CredentialAdmin(admin.ModelAdmin):
    list_display=('title','user','category','favorite','updated_at'); list_filter=('category','favorite'); search_fields=('title','username','user__username')
    readonly_fields=('password_encrypted','password_fingerprint','notes_encrypted','created_at','updated_at','password_changed_at')
@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display=('created_at','user','action','target','ip_address'); list_filter=('action',); search_fields=('user__username','target','ip_address')
