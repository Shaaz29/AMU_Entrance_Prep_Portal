from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.utils.http import url_has_allowed_host_and_scheme
import requests as http_requests
from requests import exceptions as req_exceptions
import logging

from .models import MockTest, Question, Result, Course, UserProfile
from .utils import import_questions
from .forms import UserProfileForm


logger = logging.getLogger(__name__)


def _call_gemini(prompt):
    api_key = getattr(settings, 'GEMINI_API_KEY', '').strip()
    model_name = getattr(settings, 'GEMINI_MODEL', 'gemini-2.5-flash').strip() or 'gemini-2.5-flash'
    if not api_key or api_key == 'your-gemini-api-key-here':
        return None, 'missing_api_key'
    url = (
        'https://generativelanguage.googleapis.com/v1beta/models/'
        + model_name + ':generateContent?key=' + api_key
    )
    body = {
        'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': {'temperature': 0.4, 'maxOutputTokens': 512},
    }
    try:
        resp = http_requests.post(url, json=body, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        text = data['candidates'][0]['content']['parts'][0]['text'].strip()
        if not text:
            return None, 'empty_response'
        return text, None
    except req_exceptions.HTTPError as exc:
        status_code = getattr(getattr(exc, 'response', None), 'status_code', 'unknown')
        logger.warning('Gemini HTTPError status=%s body=%s', status_code, getattr(getattr(exc, 'response', None), 'text', '')[:400])
        return None, f'http_{status_code}'
    except req_exceptions.Timeout:
        logger.warning('Gemini API request timed out.')
        return None, 'timeout'
    except req_exceptions.RequestException as exc:
        logger.warning('Gemini API request exception: %s', str(exc))
        return None, 'request_exception'
    except Exception:
        logger.exception('Unexpected Gemini API failure.')
        return None, 'unexpected_error'


def _build_gemini_prompt(question, mode):
    q_text = question.text.strip()
    stored_note = (question.concept or question.explanation or '').strip()

    if question.type == 'MCQ':
        options_block = (
            f"A) {question.option_a}\n"
            f"B) {question.option_b}\n"
            f"C) {question.option_c}\n"
            f"D) {question.option_d}"
        )
        correct = question.correct_answer.strip().upper()
        option_map = {'A': question.option_a, 'B': question.option_b,
                      'C': question.option_c, 'D': question.option_d}
        correct_text = option_map.get(correct, '')

        detail_instruction = {
            'short': 'Give a concise 2-3 sentence explanation.',
            'medium': 'Give a clear explanation in 4-6 sentences covering why the correct answer is right and why the other options are wrong.',
            'detailed': 'Give a thorough step-by-step explanation covering the concept behind the question, why the correct option is right, and why each of the other options is wrong.',
        }.get(mode, 'Give a clear explanation in 4-6 sentences.')

        prompt = (
            f"You are an expert teacher helping a student understand an exam question.\n\n"
            f"Question: {q_text}\n\n"
            f"Options:\n{options_block}\n\n"
            f"Correct Answer: {correct}) {correct_text}\n\n"
        )
        if stored_note:
            prompt += f"Additional note from teacher: {stored_note}\n\n"
        prompt += detail_instruction + "\nDo not use markdown formatting, just plain text."
    else:
        detail_instruction = {
            'short': 'Give a concise 2-3 sentence explanation.',
            'medium': 'Explain step by step how to arrive at the answer in 4-6 sentences.',
            'detailed': 'Give a thorough step-by-step solution covering the formula, substitution, and verification.',
        }.get(mode, 'Explain step by step.')

        prompt = (
            f"You are an expert teacher helping a student understand an exam question.\n\n"
            f"Question: {q_text}\n\n"
            f"Correct Answer: {question.correct_answer}\n\n"
        )
        if stored_note:
            prompt += f"Additional note from teacher: {stored_note}\n\n"
        prompt += detail_instruction + "\nDo not use markdown formatting, just plain text."

    return prompt


def _build_fallback_explanation(question, mode):
    """Template-based fallback when Gemini API key is not set."""
    if question.type == 'MCQ':
        option_map = {
            'A': question.option_a, 'B': question.option_b,
            'C': question.option_c, 'D': question.option_d,
        }
        correct_text = option_map.get(question.correct_answer, '').strip()
        answer_line = f"Correct option is {question.correct_answer}"
        if correct_text:
            answer_line += f": {correct_text}."
        else:
            answer_line += "."
        points = [answer_line]
    else:
        points = [f"Correct answer is {question.correct_answer}."]

    if question.concept:
        points.append(f"Concept: {question.concept}")
    elif question.explanation:
        points.append(f"Explanation: {question.explanation}")
    else:
        points.append("No detailed explanation is available for this question. Add an explanation in the admin panel.")

    return "\n\n".join(points)


def _build_live_explanation(question, mode='medium'):
    mode = (mode or 'medium').lower().strip()
    if mode not in {'short', 'medium', 'detailed'}:
        mode = 'medium'

    prompt = _build_gemini_prompt(question, mode)
    ai_result, reason = _call_gemini(prompt)
    if ai_result:
        return {
            'text': ai_result,
            'source': 'gemini',
            'fallback_reason': None,
        }

    return {
        'text': _build_fallback_explanation(question, mode),
        'source': 'fallback',
        'fallback_reason': reason or 'unknown',
    }


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
        next_url = request.POST.get('next') or request.GET.get('next')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
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
    selected_course_id = (request.GET.get('course_id') or '').strip()
    search_query = (request.GET.get('q') or '').strip()
    tests = MockTest.objects.select_related('course').all()
    selected_course = None

    if selected_course_id.isdigit():
        selected_course = Course.objects.filter(id=int(selected_course_id)).first()
        if selected_course:
            tests = tests.filter(course=selected_course)

    if search_query:
        tests = tests.filter(course__name__icontains=search_query)

    context = {
        'tests': tests,
        'course': selected_course,
        'search_query': search_query,
        'selected_course_id': selected_course_id,
    }
    return render(request, 'mock_test.html', context)


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

    return render(request, 'test_rules.html', {'test': test})


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

    Result.objects.create(
        user=request.user,
        mocktest=test,
        score=score
    )

    total_attempts = Result.objects.filter(mocktest=test).count()
    rank = Result.objects.filter(mocktest=test, score__gt=score).count() + 1
    rank_percentile = round(((total_attempts - rank + 1) / total_attempts) * 100) if total_attempts else 0

    if rank_percentile >= 90:
        performance_remark = "Outstanding performance."
    elif rank_percentile >= 70:
        performance_remark = "Very good work."
    elif rank_percentile >= 50:
        performance_remark = "Good effort."
    else:
        performance_remark = "Keep practicing."

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


# ================= RESULT VIEW (REQUIRED FOR URL) =================
@login_required
def result(request, test_id):
    test = MockTest.objects.get(id=test_id)
    questions = Question.objects.filter(mocktest=test)

    return render(request, 'result.html', {
        'test': test,
        'score': 0,
        'total': questions.count(),
        'review_items': []
    })


@login_required
def upload_questions(request):
    if not request.user.is_staff:
        messages.error(request, 'Only admin/staff users can upload questions.')
        return redirect('dashboard')

    tests = MockTest.objects.select_related('course').all()

    if request.method == 'POST':
        mocktest_id = request.POST.get('mocktest_id')
        upload_file = request.FILES.get('file')

        if not mocktest_id or not upload_file:
            messages.error(request, 'Please select a test and choose an Excel file.')
            return render(request, 'upload.html', {'tests': tests})

        try:
            import_questions(upload_file, mocktest_id)
            messages.success(request, 'Questions uploaded successfully.')
            return redirect('upload_questions')
        except Exception as exc:
            messages.error(request, f'Upload failed: {exc}')

    return render(request, 'upload.html', {'tests': tests})


@login_required
def profile(request):
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
        messages.error(request, 'Please correct the errors in your profile form.')
    else:
        form = UserProfileForm(instance=profile_obj)

    attempts_qs = Result.objects.filter(user=request.user).select_related('mocktest', 'mocktest__course').order_by('-date')

    attempts = []
    percentages = []
    for item in attempts_qs:
        total_questions = item.mocktest.questions.count()
        score_percentage = round((item.score / total_questions) * 100, 1) if total_questions else 0.0
        percentages.append(score_percentage)
        attempts.append({
            'date': item.date,
            'course_name': item.mocktest.course.name,
            'year': item.mocktest.year,
            'score': item.score,
            'total_questions': total_questions,
            'score_percentage': score_percentage,
        })

    total_attempts = len(attempts)
    unique_mocks = Result.objects.filter(user=request.user).values('mocktest').distinct().count()
    average_percentage = round(sum(percentages) / total_attempts, 1) if total_attempts else 0.0
    best_percentage = round(max(percentages), 1) if percentages else 0.0
    recent_attempts = attempts[:8]

    context = {
        'profile_obj': profile_obj,
        'form': form,
        'total_attempts': total_attempts,
        'unique_mocks': unique_mocks,
        'average_percentage': average_percentage,
        'best_percentage': best_percentage,
        'recent_attempts': recent_attempts,
    }
    return render(request, 'profile.html', context)


@login_required
def explain_question(request, question_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed.'}, status=405)

    question = Question.objects.filter(id=question_id).first()
    if not question:
        return JsonResponse({'error': 'Question not found.'}, status=404)

    mode = request.GET.get('mode', 'medium')
    result = _build_live_explanation(question, mode=mode)
    return JsonResponse({
        'explanation': result['text'],
        'source': result['source'],
        'fallback_reason': result['fallback_reason'],
        'mode': mode,
    })