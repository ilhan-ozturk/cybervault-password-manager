from django.urls import path
from . import views
app_name='vault'
urlpatterns=[
    path('',views.dashboard,name='dashboard'),
    path('vault/',views.credential_list,name='list'),
    path('vault/add/',views.credential_create,name='create'),
    path('vault/<int:pk>/edit/',views.credential_edit,name='edit'),
    path('vault/<int:pk>/delete/',views.credential_delete,name='delete'),
    path('vault/<int:pk>/reveal/',views.credential_reveal,name='reveal'),
    path('vault/<int:pk>/favorite/',views.toggle_favorite,name='favorite'),
    path('security/',views.security_center,name='security'),
    path('activity/',views.activity_log,name='activity'),
]
