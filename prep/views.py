from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Import your models

from .models import MockTest, Question, Result, Course

# ================= HOME PAGE =================

def home(request):
    courses = Course.objects.all()
    return render(request, 'home.html', {'courses': courses})

# ================= REGISTER =================

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not email or not password:
            messages.error(request, "All fields are required")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
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
    tests = MockTest.objects.all()
    return render(request, 'mock_test.html', {'tests': tests, 'course': None})


# ================= COURSE MOCK TEST LIST =================

@login_required
def course_mock_tests(request, course_id):
    course = Course.objects.get(id=course_id)
    tests = MockTest.objects.filter(course=course)
    return render(request, 'mock_test.html', {'tests': tests, 'course': course})

# ================= START TEST =================

@login_required
def start_test(request, test_id):
    test = MockTest.objects.get(id=test_id)
    rules_session_key = f"accepted_rules_test_{test_id}"

    if request.method == 'POST' and request.POST.get('accept_rules') == 'yes':
        request.session[rules_session_key] = True
        return redirect('start_test', test_id=test_id)

    if request.session.get(rules_session_key):
        questions = Question.objects.filter(mocktest=test)
        return render(request, 'start_test.html', {
            'test': test,
            'questions': questions,
        })

    return render(request, 'test_rules.html', {
        'test': test,
    })

# ================= SUBMIT TEST =================

@login_required
def submit_test(request, test_id):

    test = MockTest.objects.get(id=test_id)
    rules_session_key = f"accepted_rules_test_{test_id}"

    if not request.session.get(rules_session_key):
        messages.warning(request, "Please accept test rules before starting the test.")
        return redirect('start_test', test_id=test_id)

    questions = Question.objects.filter(mocktest=test)

    score = 0
    total = questions.count()
    review_items = []
    correct_count = 0
    incorrect_count = 0
    not_attempted_count = 0

    for idx, q in enumerate(questions, start=1):

        user_answer = request.POST.get(f"q{q.id}")
        is_correct = bool(user_answer) and user_answer == q.correct_answer

        if q.type == 'MCQ':
            option_map = {
                'A': q.option_a,
                'B': q.option_b,
                'C': q.option_c,
                'D': q.option_d,
            }
            user_answer_display = f"{user_answer}. {option_map.get(user_answer, 'Not selected')}" if user_answer else "Not Attempted"
            correct_answer_display = f"{q.correct_answer}. {option_map.get(q.correct_answer, '')}".strip()
        else:
            user_answer_display = user_answer if user_answer else "Not Attempted"
            correct_answer_display = q.correct_answer

        if is_correct:
            score += 1
            correct_count += 1
            review_status = 'correct'
        elif user_answer:
            incorrect_count += 1
            review_status = 'incorrect'
        else:
            not_attempted_count += 1
            review_status = 'not_attempted'

        review_items.append({
            'number': idx,
            'question': q,
            'user_answer': user_answer_display,
            'correct_answer': correct_answer_display,
            'is_correct': is_correct,
            'is_attempted': bool(user_answer),
            'explanation': q.explanation,
            'review_status': review_status,
        })

    def pct(count, base):
        return round((count / base) * 100) if base else 0

    correct_percentage = pct(correct_count, total)
    incorrect_percentage = pct(incorrect_count, total)
    not_attempted_percentage = pct(not_attempted_count, total)

    # Save result
    Result.objects.create(
        user=request.user,
        mocktest=test,
        score=score
    )

    total_attempts = Result.objects.filter(mocktest=test).count()
    rank = Result.objects.filter(mocktest=test, score__gt=score).count() + 1
    rank_percentile = round(((total_attempts - rank + 1) / total_attempts) * 100) if total_attempts else 0

    if rank_percentile >= 90:
        performance_remark = "Outstanding performance. Keep this momentum going."
    elif rank_percentile >= 70:
        performance_remark = "Very good work. You are above most test takers."
    elif rank_percentile >= 50:
        performance_remark = "Good effort. With focused revision you can climb higher."
    else:
        performance_remark = "Keep practicing. Review explanations and strengthen fundamentals."

    if rules_session_key in request.session:
        del request.session[rules_session_key]

    return render(request, 'result.html', {
        'test': test,
        'score': score,
        'total': total,
        'review_items': review_items,
        'correct_count': correct_count,
        'incorrect_count': incorrect_count,
        'not_attempted_count': not_attempted_count,
        'correct_percentage': correct_percentage,
        'incorrect_percentage': incorrect_percentage,
        'not_attempted_percentage': not_attempted_percentage,
        'rank': rank,
        'total_attempts': total_attempts,
        'rank_percentile': rank_percentile,
        'performance_remark': performance_remark,
    })

# ================= RESULT =================

@login_required
def result(request, test_id):
    score = 85
    total = 100
    return render(request, 'result.html', {
        'test': MockTest.objects.get(id=test_id),
        'score': score,
        'total': total,
        'review_items': [],
        'correct_count': 0,
        'incorrect_count': 0,
        'not_attempted_count': 0,
        'correct_percentage': 0,
        'incorrect_percentage': 0,
        'not_attempted_percentage': 0,
        'rank': 0,
        'total_attempts': 0,
        'rank_percentile': 0,
        'performance_remark': '',
    })


# ================= UPLOAD QUESTIONS =================

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

        messages.success(request, f"File uploaded successfully for {test_name}")
        return redirect('upload_questions')

    return render(request, 'upload.html')

