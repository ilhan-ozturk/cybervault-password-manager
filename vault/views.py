from collections import Counter
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import CredentialForm, RegisterForm
from .models import AuditEvent, Credential
from .security import analyze_password, is_old
from .signals import ip


def audit(request,action,target=''):
    AuditEvent.objects.create(user=request.user if request.user.is_authenticated else None,action=action,target=target[:160],ip_address=ip(request))

def register(request):
    if request.user.is_authenticated: return redirect('vault:dashboard')
    form=RegisterForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        user=form.save(); login(request,user); messages.success(request,'Account created. Your private vault is ready.'); return redirect('vault:dashboard')
    return render(request,'registration/register.html',{'form':form})

def health_data(user):
    items=list(Credential.objects.filter(user=user))
    fingerprints=Counter(x.password_fingerprint for x in items if x.password_fingerprint)
    rows=[]; weak=reused=old=0
    for item in items:
        analysis=analyze_password(item.get_password()); repeated=fingerprints[item.password_fingerprint]>1; aged=is_old(item)
        weak += analysis['score']<60; reused += repeated; old += aged
        rows.append({'item':item,'analysis':analysis,'reused':repeated,'old':aged})
    if not items: health=100
    else:
        penalties=(weak*20)+(reused*15)+(old*10); health=max(0,round(100-penalties/len(items)))
    return {'rows':rows,'total':len(items),'weak':weak,'reused':reused,'old':old,'health':health}

@login_required
def dashboard(request):
    data=health_data(request.user); data['recent']=Credential.objects.filter(user=request.user).order_by('-updated_at')[:5]; data['events']=AuditEvent.objects.filter(user=request.user)[:6]
    return render(request,'vault/dashboard.html',data)

@login_required
def credential_list(request):
    q=request.GET.get('q','').strip(); category=request.GET.get('category','').strip(); status=request.GET.get('status','').strip()
    items=Credential.objects.filter(user=request.user)
    if q: items=items.filter(Q(title__icontains=q)|Q(website__icontains=q)|Q(username__icontains=q))
    if category: items=items.filter(category=category)
    rows=[]; fp=Counter(x.password_fingerprint for x in items)
    for item in items:
        analysis=analyze_password(item.get_password()); rows.append({'item':item,'analysis':analysis,'reused':fp[item.password_fingerprint]>1,'old':is_old(item)})
    if status=='weak': rows=[r for r in rows if r['analysis']['score']<60]
    elif status=='reused': rows=[r for r in rows if r['reused']]
    elif status=='old': rows=[r for r in rows if r['old']]
    elif status=='favorite': rows=[r for r in rows if r['item'].favorite]
    return render(request,'vault/list.html',{'rows':rows,'q':q,'category':category,'status':status,'categories':Credential.CATEGORY_CHOICES})

@login_required
def credential_create(request):
    form=CredentialForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        obj=form.save(commit=False); obj.user=request.user; obj.set_password(form.cleaned_data['password']); obj.set_notes(form.cleaned_data['notes']); obj.save(); audit(request,'create',obj.title)
        messages.success(request,'Credential encrypted and saved.'); return redirect('vault:list')
    return render(request,'vault/form.html',{'form':form,'heading':'Add credential','subheading':'Secrets are encrypted before they are stored.'})

@login_required
def credential_edit(request,pk):
    obj=get_object_or_404(Credential,pk=pk,user=request.user); form=CredentialForm(request.POST or None,instance=obj,initial={'password':obj.get_password(),'notes':obj.get_notes()})
    if request.method=='POST' and form.is_valid():
        obj=form.save(commit=False); obj.user=request.user; obj.set_password(form.cleaned_data['password']); obj.set_notes(form.cleaned_data['notes']); obj.save(); audit(request,'update',obj.title)
        messages.success(request,'Credential updated.'); return redirect('vault:list')
    return render(request,'vault/form.html',{'form':form,'heading':'Edit credential','subheading':'Updating the password resets its password-age timer.'})

@login_required
@require_POST
def credential_reveal(request,pk):
    obj=get_object_or_404(Credential,pk=pk,user=request.user); audit(request,'reveal',obj.title)
    return JsonResponse({'password':obj.get_password()})

@login_required
@require_POST
def toggle_favorite(request,pk):
    obj=get_object_or_404(Credential,pk=pk,user=request.user); obj.favorite=not obj.favorite; obj.save(update_fields=['favorite']); return redirect(request.META.get('HTTP_REFERER') or 'vault:list')

@login_required
def credential_delete(request,pk):
    obj=get_object_or_404(Credential,pk=pk,user=request.user)
    if request.method=='POST':
        title=obj.title; obj.delete(); audit(request,'delete',title); messages.success(request,'Credential deleted.'); return redirect('vault:list')
    return render(request,'vault/delete.html',{'item':obj})

@login_required
def security_center(request):
    data=health_data(request.user); audit(request,'security','Security Center'); return render(request,'vault/security.html',data)

@login_required
def activity_log(request):
    events=AuditEvent.objects.filter(user=request.user)[:100]; return render(request,'vault/activity.html',{'events':events})
