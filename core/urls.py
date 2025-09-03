from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('jobs/create/', views.job_create, name='job_create'),
    # Messaging URLs
    path('proposals/<int:pk>/accept/', views.accept_proposal, name='accept_proposal'),
    path('threads/<int:pk>/', views.thread_detail, name='thread_detail'),
    # User Profile Edit
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    # Search
    path('search/', views.search, name='search'),
    # Job deletion
    path('jobs/<int:pk>/edit/', views.job_edit, name='job_edit'),
    path('jobs/<int:pk>/delete/', views.job_delete, name='job_delete'),
    path('dashboard/client/', views.client_dashboard, name='client_dashboard'),
    # Role choosing after google signup
    path('choose-role/', views.choose_role, name='choose_role'),
]