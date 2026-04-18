from django.urls import path
from . import views

urlpatterns = [

    # ================= HOME =================
    path('', views.home, name='home'),

    # ================= AUTHENTICATION =================
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # ================= PASSWORD RECOVERY =================
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),

    # ================= DASHBOARD =================
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),

    # ================= MOCK TESTS =================
    path('mock-tests/', views.mock_tests, name='mock_tests'),

    # Course-specific mock test list
    path('mock-tests/<int:course_id>/', views.course_mock_tests, name='course_mock_tests'),

    # Start Test
    path('start-test/<int:test_id>/', views.start_test, name='start_test'),

    # Submit Test
    path('submit-test/<int:test_id>/', views.submit_test, name='submit_test'),

    # Result Page
    path('result/<int:test_id>/', views.result, name='result'),


    # ================= ADMIN QUESTION UPLOAD =================
    path('upload-questions/', views.upload_questions, name='upload_questions'),
]