from django.urls import path
from user import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.user_dashboard_view, name='dashboard'),
    path('update-profile/', views.profile_update_view, name='update-profile')
]
