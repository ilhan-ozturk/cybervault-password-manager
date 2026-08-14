from django.conf import settings
from django.db import models
from django.utils import timezone
from .crypto import decrypt_text, encrypt_text, password_fingerprint
from .security import analyze_password

class Credential(models.Model):
    CATEGORY_CHOICES=[('work','Work'),('personal','Personal'),('social','Social'),('finance','Finance'),('development','Development'),('other','Other')]
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='credentials')
    title=models.CharField(max_length=120)
    website=models.URLField(blank=True)
    username=models.CharField(max_length=180,blank=True)
    password_encrypted=models.TextField()
    password_fingerprint=models.CharField(max_length=64,db_index=True)
    notes_encrypted=models.TextField(blank=True)
    category=models.CharField(max_length=20,choices=CATEGORY_CHOICES,default='other')
    favorite=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    password_changed_at=models.DateTimeField(default=timezone.now)
    class Meta: ordering=['-favorite','title']; indexes=[models.Index(fields=['user','title']),models.Index(fields=['user','category'])]
    def set_password(self,raw):
        self.password_encrypted=encrypt_text(raw); self.password_fingerprint=password_fingerprint(raw); self.password_changed_at=timezone.now()
    def get_password(self): return decrypt_text(self.password_encrypted)
    def set_notes(self,raw): self.notes_encrypted=encrypt_text(raw or '')
    def get_notes(self): return decrypt_text(self.notes_encrypted)
    def strength(self): return analyze_password(self.get_password())
    def masked_password(self): return '•'*12
    def __str__(self): return f'{self.title} — {self.user.username}'

class AuditEvent(models.Model):
    ACTIONS=[('login','Login'),('logout','Logout'),('create','Credential created'),('update','Credential updated'),('delete','Credential deleted'),('reveal','Password revealed'),('security','Security Center viewed')]
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True,related_name='vault_events')
    action=models.CharField(max_length=20,choices=ACTIONS)
    target=models.CharField(max_length=160,blank=True)
    ip_address=models.GenericIPAddressField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']
    def __str__(self): return f'{self.action} · {self.user or "anonymous"}'
