from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import access_key_list, GenerateAccessKeyView

urlpatterns = [
    path('', views.homePage, name="home"),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),

    #user registration
    path('register/', views.register, name="register"),

    #password change
    path('password_change/', auth_views.PasswordChangeView.as_view(),name="password_change"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(),name="password_change_done"),

    #reset password
    path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    #access key
    path('access-keys/', views.access_key_list, name='access_key_list'),
    path('generate-keys/', views.GenerateAccessKeyView, name='generate_key_view'),
    path('school-key-details/', views.school_key_details, name='school_key_details'),

    #admin section
    path('admin_dashboard/', views.admin_dashboard, name="admin_dashboard"),
    path('revoke_access_key/<str:pk>/', views.revoke_access_key, name="revoke_access_key"),
]