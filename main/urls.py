from django.urls import path
from django.contrib.auth.views import LogoutView # шоб выйти можно было
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView

from .views import index
from .views import reservation
from .views import BBLoginView
from .views import ChangeUserInfoView
from .views import PasswordChangeView
from .views import RegisterUserView, RegisterDoneView
from .views import user_activate
from .views import DeleteuserView
from .views import RoomView

app_name='main'
urlpatterns=[
    path('',index, name='index'),
    path('reservation/', reservation, name='reservation'),
    path('accounts/login/', BBLoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='main:index'),
         name='logout'),
    path('accounts/profile_delete/', DeleteuserView.as_view(),
         name='profile_delete'),
    path('accounts/profile_change/', ChangeUserInfoView.as_view(),
         name='profile_change'),
    path('accounts/password_change/', PasswordChangeView.as_view(),
         name='password_change'),
    path('accounts/register/done', RegisterDoneView.as_view(),
         name='register_done'),
    path('accounts/register', RegisterUserView.as_view(),
         name='register'),
    path('accounts/register/activate/<str:sign>', user_activate,
         name='register_activate'),
    path('password_reset/', PasswordResetView.as_view( #говно какое-то
        template_name = 'main/reset_password.html',
        subject_template_name='email/reset_subjetc.txt',
        email_template_name='email/reset_email.html'),
        name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(
         template_name='email/email_sent.html'),
         name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
         template_name='email/confirm_password.html'),
         name='password_reset_confirm'),
    path('accounts/reset/done/', PasswordResetCompleteView.as_view( #конец говна
         template_name='email/password_confirmed.html'),
         name='password_reset_complete'),
    path('rooms/', RoomView, name='rooms')
]
