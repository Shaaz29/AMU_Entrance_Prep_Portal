from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Import your models
from .models import MockTest


# ================= HOME PAGE =================
def home(request):
    return render(request, 'home.html')


# ================= REGISTER =================
def register(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check empty fields
        if not username or not email or not password:
            messages.error(request, "All fields are required")
            return redirect('register')

        # Check username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        # Check email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')

    return render(request, 'register.html')


# ================= LOGIN =================
def user_login(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')


# ================= LOGOUT =================
def user_logout(request):
    logout(request)
    return redirect('home')


# ================= DASHBOARD =================
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


# ================= MOCK TEST LIST =================
@login_required
def mock_tests(request):

    # Load tests from database
    tests = MockTest.objects.all()

    return render(request, 'mock_tests.html', {"tests": tests})


# ================= START TEST =================
@login_required
def start_test(request, test_id):

    test = MockTest.objects.get(id=test_id)

    return render(request, 'start_test.html', {
        'test': test
    })


# ================= SUBMIT TEST =================
@login_required
def submit_test(request, test_id):

    # Later: real scoring logic
    score = 85

    return redirect('result', test_id=test_id)


# ================= RESULT =================
@login_required
def result(request, test_id):

    score = 85

    return render(request, 'result.html', {
        'test_id': test_id,
        'score': score
    })


# ================= UPLOAD QUESTIONS (ADMIN ONLY) =================
@login_required
def upload_questions(request):

    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('dashboard')

    if request.method == 'POST':

        test_name = request.POST.get('test_name')
        uploaded_file = request.FILES.get('file')

        if not uploaded_file:
            messages.error(request, "Please select a file")
            return redirect('upload_questions')

        messages.success(request, f'File uploaded successfully for {test_name}')
        return redirect('upload_questions')

    return render(request, 'upload.html')