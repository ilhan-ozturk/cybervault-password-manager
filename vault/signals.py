from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import AuditEvent

def ip(request):
    if not request: return None
    forwarded=request.META.get('HTTP_X_FORWARDED_FOR','').split(',')[0].strip()
    return forwarded or request.META.get('REMOTE_ADDR') or None
@receiver(user_logged_in)
def on_login(sender,request,user,**kwargs): AuditEvent.objects.create(user=user,action='login',ip_address=ip(request))
@receiver(user_logged_out)
def on_logout(sender,request,user,**kwargs):
    if user and getattr(user,'is_authenticated',False): AuditEvent.objects.create(user=user,action='logout',ip_address=ip(request))
