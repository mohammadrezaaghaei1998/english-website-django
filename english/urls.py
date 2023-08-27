from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static 
from . import views
from django.contrib.auth import views as auth_views

# from django.views.generic import TemplateView





urlpatterns = [
    path('admin/', admin.site.urls),
#     path('acoounts/', TemplateView.as_view(template_name='main/google.html'), name='google'),
    
    
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),

    path("",views.HOME,name="home"),
    path("about/",views.ABOUT,name="about"),
    path("contact/",views.contact,name="contact"),
    path("courses/",views.COURSES,name="courses"),


    path('package/<int:package_id>/', views.package_detail, name='package_detail'),
    # path('purchase_package/<int:package_id>/', views.purchase_package, name='purchase_package'),
    # path('payment_succsess/', views.payment_success, name='payment_success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('packages/<int:package_id>/', views.packages, name='packages'),


     path('video_list/', views.video_list, name='video_list'),


    #DASHBOARD CHANGE_PASSWORD
    path('change_password/',views.change_password, name='change_password'),
    path('change_password_done/', views.change_password_done, name='change_password_done'),



    #EMIAL PASSWORD
    path('reset_password/', auth_views.PasswordResetView.as_view
         (template_name='main/reset_password.html')
         ,name='reset_password'),


    path('reset-password_sent/', auth_views.PasswordResetDoneView.as_view
         (template_name='main/password_reset_sent.html')
         ,name='password_reset_done'),


    path('reset-password_complete/', auth_views.PasswordResetCompleteView.as_view
         (template_name='main/change_password_done.html')
         ,name='password_reset_complete'),


    path('reset/uidb64/<token>',auth_views.PasswordResetConfirmView.as_view
          (template_name='main/change_password_done.html')
         ,name='password_reset_confirm'),




    path('index/<int:package_id>/', views.index,name='index'),
    path('odeme/<int:package_id>/', views.odeme, name='odeme'),
    path('ok-url/', views.ok_url,name='ok_url'),
    path('fail-url/', views.fail_url,name='fail_url'),

]


urlpatterns += static(settings.STATIC_URL , document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)
