from django.contrib import admin
from django.urls import path,include
from Request_Handler import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',auth_views.LoginView.as_view(template_name='login.html'),name='index'),
    path('register/',views.register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('home/',views.home,name='home'),
    path('arduino/request/',views.arduino,name='arduino'),
    path('test/',views.test,name='test'),
    path('agent/',views.agent,name='agent'),
    path('booknow/',views.bookAgent,name='book'),
    path('redeem/',views.redeem,name='redeem'),
    path('transaction/',views.transaction,name='transaction'),
    path('bookAgent/',views.bookAgent,name='bookAgent'),
    path('openClose/',views.openClose,name='openClose')

]