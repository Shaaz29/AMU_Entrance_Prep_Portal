from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Mock Tests
    path('mock-tests/', views.mock_tests, name='mock_tests'),
    path('start-test/<int:test_id>/', views.start_test, name='start_test'),
    path('submit-test/<int:test_id>/', views.submit_test, name='submit_test'),
    path('result/<int:test_id>/', views.result, name='result'),

    # Admin Upload (Superuser Only)
    path('upload-questions/', views.upload_questions, name='upload_questions'),
]
