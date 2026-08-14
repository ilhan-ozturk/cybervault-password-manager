from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
class Migration(migrations.Migration):
    initial=True
    dependencies=[migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations=[
        migrations.CreateModel(name='AuditEvent',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('action',models.CharField(choices=[('login','Login'),('logout','Logout'),('create','Credential created'),('update','Credential updated'),('delete','Credential deleted'),('reveal','Password revealed'),('security','Security Center viewed')],max_length=20)),('target',models.CharField(blank=True,max_length=160)),('ip_address',models.GenericIPAddressField(blank=True,null=True)),('created_at',models.DateTimeField(auto_now_add=True)),('user',models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.CASCADE,related_name='vault_events',to=settings.AUTH_USER_MODEL))],options={'ordering':['-created_at']}),
        migrations.CreateModel(name='Credential',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('title',models.CharField(max_length=120)),('website',models.URLField(blank=True)),('username',models.CharField(blank=True,max_length=180)),('password_encrypted',models.TextField()),('password_fingerprint',models.CharField(db_index=True,max_length=64)),('notes_encrypted',models.TextField(blank=True)),('category',models.CharField(choices=[('work','Work'),('personal','Personal'),('social','Social'),('finance','Finance'),('development','Development'),('other','Other')],default='other',max_length=20)),('favorite',models.BooleanField(default=False)),('created_at',models.DateTimeField(auto_now_add=True)),('updated_at',models.DateTimeField(auto_now=True)),('password_changed_at',models.DateTimeField(default=django.utils.timezone.now)),('user',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='credentials',to=settings.AUTH_USER_MODEL))],options={'ordering':['-favorite','title']}),
        migrations.AddIndex(model_name='credential',index=models.Index(fields=['user','title'],name='vault_crede_user_id_4e4b21_idx')),
        migrations.AddIndex(model_name='credential',index=models.Index(fields=['user','category'],name='vault_crede_user_id_55f51a_idx')),
    ]
