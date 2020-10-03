from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('trytest', views.trytest, name='trytest'),

    path('studentlogin', views.studentlogin, name='studentlogin'),
    path('studentregister', views.studentregister, name='studentregister'),
    path('studentloginVal', views.studentloginVal, name='studentloginVal'),
    path('studentregisterVal', views.studentregisterVal, name='studentregisterVal'),
    path('studentlogout', views.studentlogout, name='studentlogout'),
    
    path('taketest', views.taketest, name='taketest'),
    path('papersubmit', views.papersubmit, name='papersubmit'),

    path('clientlogin', views.clientlogin, name='clientlogin'),
    path('clientregister', views.clientregister, name='clientregister'),
    path('clienthome', views.clienthome, name='clienthome'),
    path('clientregisterVal', views.clientregisterVal, name='clientregisterVal'),
    path('clientlogout', views.clientlogout, name='clientlogout'),
    path('clientloginVal', views.clientloginVal, name='clientloginVal'),
   
    path('addtest', views.addtest, name='addtest'),
    path('upload', views.upload, name='upload'),
    path('(<test_id>[0-9]+)/deletetest/', views.deletetest, name='deletetest'),
    path('studentinfo', views.studentinfo, name='studentinfo'),
    path('studentmarks', views.studentmarks, name='studentmarks'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
