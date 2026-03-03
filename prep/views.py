from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# ================= HOME PAGE =================
def home(request):
    return render(request, 'home.html')


# ================= REGISTER =================
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

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
    """
    Only:
    1 Previous Year Paper
    2 Additional Mock Tests
    """
    tests = [
        {"id": 1, "name": "Previous Year Paper"},
        {"id": 2, "name": "Mock Test 1"},
        {"id": 3, "name": "Mock Test 2"},
    ]
    return render(request, 'mock_tests.html', {"tests": tests})


# ================= START TEST =================
@login_required
def start_test(request, test_id):
    return render(request, 'start_test.html', {'test_id': test_id})


# ================= SUBMIT TEST =================
@login_required
def submit_test(request, test_id):
    # Later: Calculate real score from database
    score = 85  # Temporary static score
    return redirect('result', test_id=test_id)


# ================= RESULT =================
@login_required
def result(request, test_id):
    score = 85  # Temporary
    return render(request, 'result.html', {
        'test_id': test_id,
        'score': score
    })


# ================= UPLOAD QUESTIONS (ADMIN ONLY) =================
@login_required
def upload_questions(request):

    # Only superuser can access
    if not request.user.is_superuser:
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
