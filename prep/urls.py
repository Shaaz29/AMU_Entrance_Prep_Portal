from django.urls import path
from . import views

urlpatterns = [
    # Home page of AMU Entrance Prep Portal
    path('', views.home, name='home'),

    # User authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Dashboard after login
    path('dashboard/', views.dashboard, name='dashboard'),

    # Mock test section
    path('mock-tests/', views.mock_tests, name='mock_tests'),
    path('start-test/<int:test_id>/', views.start_test, name='start_test'),
    path('submit-test/<int:test_id>/', views.submit_test, name='submit_test'),
    path('result/<int:test_id>/', views.result, name='result'),
]