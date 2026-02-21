from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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
            return render(request, 'register.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('login')

    return render(request, 'register.html')


# ================= LOGIN =================
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

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
    return render(request, 'mock_tests.html')


# ================= START TEST =================
@login_required
def start_test(request, test_id):
    return render(request, 'start_test.html', {'test_id': test_id})


# ================= SUBMIT TEST =================
@login_required
def submit_test(request, test_id):
    # Later you will calculate score here
    return redirect('result', test_id=test_id)


# ================= RESULT =================
@login_required
def result(request, test_id):
    return render(request, 'result.html', {'test_id': test_id, 'score': 85})


# ================= UPLOAD QUESTIONS =================
@login_required
def upload_questions(request):
    """
    Admin can upload Excel file containing questions.
    Later we will process file and insert into database.
    """
    if request.method == 'POST':
        test_name = request.POST.get('test_name')
        uploaded_file = request.FILES.get('file')

        if not uploaded_file:
            return render(request, 'upload.html', {'error': 'Please select a file'})

        # For now just show success message
        return render(request, 'upload.html', {
            'message': f'File uploaded successfully for {test_name}'
        })

    return render(request, 'upload.html')