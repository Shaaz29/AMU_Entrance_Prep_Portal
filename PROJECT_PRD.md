# AMU Entrance Portal - Product Requirements Document (PRD)

Version: 1.0  
Date: April 5, 2026  
Prepared from codebase audit of `AMU_ Entrance_Portal`

## 1. Product Overview
AMU Entrance Portal is a web-based mock test and preparation platform for AMU entrance aspirants. It currently supports course-wise mock test discovery, timed test-taking, result analytics, profile management, admin-driven question upload, and AI-assisted question explanation.

The product is built using Django and Bootstrap, with server-rendered templates and a PostgreSQL-or-SQLite compatible backend.

## 2. Vision and Goals
### Vision
Enable AMU aspirants to practice previous-year-style exams in a realistic interface and improve through measurable performance insights.

### Primary Goals
1. Provide exam-like timed mock tests per AMU course/year.
2. Deliver immediate score feedback with per-question review.
3. Improve learning with static and AI-generated explanations.
4. Offer simple admin workflows for large question-bank uploads.
5. Track learner performance over repeated attempts.

### Non-Goals (Current Version)
1. Multi-language learning experience.
2. Negative marking and weighted scoring rules.
3. Payments/subscriptions.
4. Adaptive difficulty engine.
5. Proctoring/anti-cheat controls.

## 3. Target Users
1. Aspirants (primary): register/login, attempt mocks, see results, track profile stats.
2. Academic Admin/Content Team: manage courses/tests/questions via Django admin and Excel upload.
3. Super Admin: environment setup, deployment, superuser management.

## 4. Key User Journeys
1. User registers -> logs in -> browses tests by course -> accepts rules -> attempts timed mock -> submits -> views analytics and explanations.
2. Returning user logs in -> revisits profile -> reviews recent attempts/performance trend.
3. Staff uploads Excel question file mapped to a mock test -> questions become available in test UI.

## 5. Current Feature Scope (As Implemented)
### 5.1 Authentication and Session
1. User registration with unique username/email validation.
2. Login/logout using Django auth.
3. Protected routes via `@login_required`.
4. Safe handling of `next` redirect in login.

### 5.2 Courses and Mock Tests
1. Home page lists available courses.
2. Mock test listing supports:
1. Course filtering (`course_id`).
2. Search by course name (`q`).
3. Course-specific listing route.
3. Navbar global course selector for authenticated users.

### 5.3 Exam Flow
1. Pre-test rules acceptance gate stored in session (`accepted_rules_test_<id>`).
2. Timed test interface with:
1. Sticky countdown timer.
2. Question palette navigation.
3. Answered progress tracker.
4. Auto-submit when timer reaches zero.
3. MCQ answer capture via radio inputs.
4. (Legacy/partial) numeric-answer keypad UI still present in template but model enforces MCQ-only.

### 5.4 Result and Review
1. Scoring by correct count.
2. Categorization: correct, incorrect, not attempted.
3. Percentage split for each category.
4. Rank and percentile per mock test across all attempts.
5. Performance remark bands based on percentile.
6. Per-question review with:
1. User answer and correct answer.
2. Static explanation toggle.
3. AI explanation API call with fallback messaging.
4. Client-side filters for question status.

### 5.5 AI Explanation
1. Endpoint: `GET /api/explain-question/<question_id>/?mode=short|medium|detailed`.
2. Gemini API integration via HTTP.
3. Prompting includes question, options, correct answer, and concept/explanation context.
4. Graceful fallback explanation when API is unavailable or key missing.

### 5.6 Profile and Performance
1. User profile model with full name, phone, bio, photo.
2. Photo upload validation (size <= 5MB; JPG/JPEG/PNG/GIF/WebP).
3. Avatar framing controls (`photo_position_x`, `photo_position_y`).
4. Profile stats:
1. Total attempts.
2. Unique mocks attempted.
3. Average percentage.
4. Best percentage.
5. Recent attempt table.

### 5.7 Admin and Content Operations
1. Django admin for Course, MockTest, Question, Result, UserProfile.
2. `django-import-export` enabled in admin models.
3. Staff-only manual Excel upload page for questions.
4. Upload utility supports:
1. Per-row `mocktest` ID.
2. Fallback selected mock test from form.
3. Validation of `correct_answer` in A/B/C/D.

### 5.8 Deployment and Operations
1. `gunicorn` WSGI deployment (Procfile).
2. WhiteNoise static serving.
3. Environment-based DB:
1. SQLite in debug.
2. `DATABASE_URL` required in production.
4. Build script installs dependencies, collects static files, migrates DB, ensures superuser.

## 6. Functional Requirements (PRD Baseline)
### FR-01 Authentication
1. System must allow account creation with username, email, password.
2. System must reject duplicate username/email.
3. System must support login, logout, and protected-page redirects.

### FR-02 Course and Mock Discovery
1. System must list all courses on landing page.
2. System must list mock tests with course/year/duration metadata.
3. System must support search and course filtering.

### FR-03 Rule-Gated Test Start
1. User must explicitly accept test instructions before seeing questions.
2. Rule acceptance must be test-specific and session-bound.

### FR-04 Timed Test Attempt
1. Timer must display remaining duration.
2. Timer expiry must auto-submit.
3. User must be able to navigate questions with palette.
4. UI must show answered-progress percentage.

### FR-05 Submission and Scoring
1. System must compute score out of total questions.
2. System must store each attempt as a Result record.
3. System must compute rank and percentile for mock-specific leaderboard context.

### FR-06 Result Review
1. System must show per-question correctness state.
2. System must display user answer and correct answer.
3. System must show available static explanations.
4. System must allow status filtering (all/correct/incorrect/not attempted).

### FR-07 AI Explainability
1. User must be able to request generated explanation for a question.
2. API must return structured response with source (`gemini`/`fallback`) and reason on fallback.
3. UI must handle errors gracefully without page reload.

### FR-08 Profile
1. Users must edit personal metadata and avatar.
2. System must validate avatar file type and size.
3. System must store avatar framing coordinates and apply in UI.
4. System must show user-level performance KPIs.

### FR-09 Content Ingestion
1. Staff must upload Excel sheets to create MCQ questions in bulk.
2. Upload must fail with clear errors for invalid mocktest/correct answer data.
3. Admin must be able to manage all entities through Django admin.

## 7. Non-Functional Requirements
1. Security:
1. CSRF protection on forms.
2. Auth checks on protected routes.
3. Host-validated `next` redirects.
2. Performance:
1. Mock list/result/profile should query efficiently with relation prefetch/select where used.
2. AI explanation requests should timeout and degrade gracefully.
3. Reliability:
1. Production must fail fast when `DATABASE_URL` missing and `DEBUG=False`.
2. Superuser bootstrap should be idempotent.
4. Usability:
1. Mobile-responsive layouts for navbar, test list, exam UI, result and profile pages.
2. Toast notifications for user feedback.
5. Operability:
1. Environment-driven config for DB, media root, Gemini settings.
2. Compatible with local SQLite and hosted PostgreSQL.

## 8. Data Model Requirements
1. `Course(name)`; ordered by name.
2. `MockTest(course, year, duration)`; ordered newest year first.
3. `Question(mocktest, type=MCQ fixed, text, option_a-d, correct_answer, explanation, concept, image)`.
4. `Result(user, mocktest, score, date)`; ordered latest first.
5. `UserProfile(user one-to-one, full_name, phone, bio, photo, photo_position_x/y, updated_at)`.

## 9. API/Endpoint Requirements
### Web Routes
1. `/` home.
2. `/register/`, `/login/`, `/logout/`.
3. `/dashboard/`, `/profile/`.
4. `/mock-tests/`, `/mock-tests/<course_id>/`.
5. `/start-test/<test_id>/`, `/submit-test/<test_id>/`, `/result/<test_id>/`.
6. `/upload-questions/` (staff only).

### JSON Route
1. `/api/explain-question/<question_id>/` with optional `mode`.

## 10. Analytics and Success Metrics
### Product KPIs
1. Registration-to-first-test conversion rate.
2. Weekly active test takers.
3. Average tests attempted per active user.
4. Average score improvement over last N attempts.
5. AI explanation usage rate per result page view.
6. Question upload success rate (staff operation quality).

### Operational KPIs
1. Explanation API error/fallback rate.
2. Test submission completion rate (manual + auto-submit).
3. Page load and server response times for test and result pages.

## 11. Risks and Gaps Found in Current Implementation
1. Registration form includes `confirm_password` input in UI but backend does not validate/match it.
2. Some templates/CSS contain encoding artifacts (garbled symbols) that can affect presentation quality.
3. `MockTest` and `Question` retrieval often uses `.get()` without graceful 404 handling.
4. Timer and answer states are client-side only; page refresh may lose in-progress state.
5. Numeric question branch exists in template/JS, but model/admin enforce MCQ-only (dead/legacy path).
6. Result image rendering is inconsistent:
1. Test page uses `{% static q.image %}`.
2. Result page uses `item.question.image.url` though `image` is currently a `CharField`.
7. No explicit rate limiting/caching on AI explanation endpoint.
8. No automated test suite found in repository.

## 12. Recommended Product Roadmap
### Phase 1 (Stability and Correctness)
1. Add confirm-password validation.
2. Standardize question image storage/reference strategy.
3. Replace `.get()` with `get_object_or_404` in user-facing routes.
4. Remove/complete numeric-question feature path.
5. Fix encoding artifacts in templates/CSS.

### Phase 2 (Learning Quality)
1. Topic-wise and difficulty-wise tagging.
2. Attempt history charts and trend lines.
3. Explanation quality controls (prompt guardrails, caching, retries).
4. Admin upload pre-validation and downloadable error reports.

### Phase 3 (Scale and Engagement)
1. Leaderboards by course/year cohort.
2. Personalized recommendation of next mock.
3. Daily practice goals and reminder nudges.
4. Optional subscription/payment layer.

## 13. Acceptance Criteria (Release-Ready Baseline)
1. User can complete full journey from registration to result review without server errors.
2. Test timer auto-submits reliably at expiry.
3. Result page correctly computes and displays score, percentages, rank, and remarks.
4. AI explanation endpoint returns either generated or fallback explanation with explicit source.
5. Staff can upload a valid Excel file and see newly created questions in selected mock.
6. Profile photo upload and framing persist across reloads.

## 14. Directory and File Audit (Traceability)
### Root
1. `manage.py`: Django command entrypoint.
2. `requirements.txt`: framework/libs (Django, pandas, requests, WhiteNoise, gunicorn, etc.).
3. `build.sh`: deploy pipeline (install, collectstatic, migrate, ensure superuser).
4. `Procfile`: WSGI launch command.
5. `runtime.txt`: Python runtime version.
6. `.gitignore`: ignores env/db/static/media artifacts.
7. `.env`: runtime secrets/config (not committed).
8. `db.sqlite3`: local dev database.

### Project Config (`amu_portal/`)
1. `settings.py`: env loading, DB strategy, static/media config, auth redirects, Gemini settings.
2. `urls.py`: root routing to app and media/static serving behavior.
3. `wsgi.py`: WSGI application entry.

### App (`prep/`)
1. `models.py`: domain entities (Course, MockTest, Question, Result, UserProfile).
2. `views.py`: auth, exam flow, scoring, profile, upload, AI explanation endpoints.
3. `urls.py`: route map for app screens and API.
4. `utils.py`: Excel parsing/import pipeline.
5. `forms.py`: profile form and photo validation.
6. `admin.py`: admin registration/list/search/filter behavior.
7. `context_processors.py`: authenticated navbar course injector.
8. `management/commands/ensure_superuser.py`: env-driven superuser create/update.
9. `migrations/0001-0005`: schema evolution (initial models, concept field, profile, photo positioning, MCQ-only).

### Templates (`templates/`)
1. `base.html`: global layout, navbar, toasts, scripts.
2. `home.html`: hero + courses + highlights.
3. `login.html`, `register.html`: auth forms.
4. `dashboard.html`: minimal welcome/start link.
5. `mock_test.html`: course panel + test list.
6. `test_rules.html`: pre-test consent page.
7. `start_test.html`: timed exam interface and JS logic.
8. `result.html`: analytics + review + AI explain integration.
9. `profile.html`: profile editor and recent attempts.
10. `upload.html`: staff-only Excel upload screen.

### Static (`static/`)
1. `css/style.css`: complete design system for navbar, exam, result, profile, mock list, toasts.
2. `diagrams/cell.jpg`, `diagrams/mouse.jpg`: question diagram assets.

### Generated/Runtime Directories
1. `media/`: user uploads (profile photos and potential media assets).
2. `staticfiles/`: collected static output for deployment.
3. `.venv/`, `venv/`: local virtual environments.

## 15. Future Technical Requirements (Recommended)
1. Add automated tests:
1. Unit tests for scoring/rank logic and upload parser.
2. Integration tests for auth and full test submission flow.
3. API tests for explanation endpoint fallback behavior.
2. Add observability:
1. Structured logging for exam submissions and explanation failures.
2. Basic monitoring/alerting on endpoint error rates.
3. Improve security hardening:
1. Strong password policy UX feedback.
2. Brute-force login protection.
3. File upload virus/content-type hardening.
4. Improve performance:
1. Cache frequently requested course/test lists.
2. Add pagination for large question banks and attempt history.

---

This PRD reflects the current implementation baseline and the recommended direction to evolve AMU Entrance Portal into a production-grade, scalable exam-prep platform.
