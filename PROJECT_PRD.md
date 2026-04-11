# AMU Entrance Portal - Product Requirements Document (PRD)

Version: 2.0  
Date: April 11, 2026  
Prepared from codebase audit of `AMU_ Entrance_Portal`

## 1. Product Overview
AMU Entrance Portal is a web-based mock test and preparation platform for AMU entrance aspirants. It seamlessly supports course-wise mock test discovery, timed test-taking, result analytics, advanced profile management, and a highly concurrent admin-driven question and image upload system powered by Cloudinary.

The product is built using Django and Bootstrap, with server-rendered templates, Postgres/SQLite backend compatibility, and offloaded media management.

## 2. Vision and Goals
### Vision
Enable AMU aspirants to practice previous-year-style exams in a realistic interface and improve through measurable performance insights and high-quality visual explanations.

### Primary Goals
1. Provide exam-like timed mock tests per AMU course/year.
2. Deliver immediate score feedback with per-question review and scalable multi-page visual explanations.
3. Offer an extremely fast, concurrent admin workflow for massive question-bank and multi-image ZIP uploads.
4. Scale media processing flawlessly using Cloudinary CDNs.
5. Track learner performance over repeated attempts.

### Non-Goals (Current Version)
1. Multi-language learning experience.
2. Negative marking and weighted scoring rules.
3. Payments/subscriptions.
4. Adaptive difficulty engine.
5. Proctoring/anti-cheat controls.

## 3. Target Users
1. Aspirants (primary): register/login, attempt mocks, see results, track profile stats, manage their photo layout.
2. Academic Admin/Content Team: manage courses/tests/questions via Django admin and high-speed multi-threaded ZIP/Excel imports.
3. Super Admin: environment setup, deployment, Cloudinary config management.

## 4. Key User Journeys
1. User registers -> logs in -> browses tests by course -> accepts rules -> attempts timed mock -> submits -> views analytics and visual multi-page explanations.
2. Returning user logs in -> revisits profile -> edits profile photo with drag-and-drop framing -> reviews recent attempts/performance trend.
3. Staff compiles Excel file (with multiple comma-separated images per row) and a ZIP of all images -> system concurrently extracts and blasts images to Cloudinary -> questions instantly available in test UI.

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
   2. Question palette navigation with smooth scrolling boundaries.
   3. Answered progress tracker.
   4. Auto-submit when timer reaches zero.
   5. Graceful support for questions with multiple natural-scale images rendered vertically.
3. MCQ answer capture via radio inputs.

### 5.4 Result and Review
1. Scoring by correct count.
2. Categorization: correct, incorrect, not attempted.
3. Percentage split for each category.
4. Rank and percentile per mock test across all attempts.
5. Performance remark bands based on percentile.
6. Per-question review with:
   1. User answer and correct answer status toggles.
   2. Support for multi-image visual explanations cleanly stacked.
   3. Client-side filters for question status review.

### 5.5 Profile and Performance
1. User profile model with full name, phone, bio, photo.
2. Photo upload validation (size <= 5MB; JPG/JPEG/PNG/GIF/WebP) automatically beamed to Cloudinary.
3. Avatar framing controls integrated directly into the image via drag-and-drop logic (`photo_position_x`, `photo_position_y`).
4. Profile stats:
   1. Total attempts.
   2. Unique mocks attempted.
   3. Average percentage.
   4. Best percentage.
   5. Recent attempt table.

### 5.6 Admin and Content Operations
1. Django admin for Course, MockTest, Question, Result, UserProfile.
2. `django-import-export` enabled in admin models.
3. Staff-only manual Excel upload page for questions with mandatory dropdown validations.
4. Concurrency Upload Pipeline:
   1. Support for comma-separated image listings in Excel (`image` & `explanation_image`).
   2. Hyper-threaded `ThreadPoolExecutor` parsing architecture pushing 15+ API requests simultaneously.
   3. Completely bypasses Render router timeouts for massive uploads.

### 5.7 Deployment and Operations
1. `gunicorn` WSGI deployment (Procfile).
2. WhiteNoise static serving.
3. Persistent High-Availability Media: `django-cloudinary-storage` via `STORAGES` dictionary.
4. Environment-based DB Configuration (PostgreSQL URL scaling).

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
3. User must be able to navigate questions with a scrollable palette.
4. Multiple document images must retain intrinsic scaling cleanly.

### FR-05 Submission and Scoring
1. System must compute score out of total questions.
2. System must store each attempt as a Result record.
3. System must compute rank and percentile for mock-specific leaderboard context.

### FR-06 Result Review
1. System must show per-question correctness state.
2. System must display user answer and correct answer.
3. System must cleanly stack zero-to-many explanation document images per question.
4. System must allow status filtering (all/correct/incorrect/not attempted).

### FR-07 Profile
1. Users must edit personal metadata and Cloudinary-persisted avatar.
2. Interactive drag logic must map framing coordinates and apply uniformly in UI header.
3. System must show user-level performance KPIs.

### FR-08 Content Ingestion
1. Staff must upload zipped Excel sheets to deploy heavily image-based MCQ questions in bulk.
2. Image binary processing must happen exclusively over multi-threaded background workers.
3. Admin must be able to manage all entities through Django admin.

## 7. Non-Functional Requirements
1. Security:
   1. CSRF protection on forms.
   2. Auth checks on protected routes.
   3. Host-validated `next` redirects.
2. Performance & Resiliency:
   1. Cloudinary CDN edge caching for all heavy media loadouts.
   2. Asynchronous thread pools preventing HTTP server crashes/timeouts on zip extraction.
3. Reliability:
   1. Production must fail fast when `DATABASE_URL` or `CLOUDINARY_URL` is missing and `DEBUG=False`.
4. Usability:
   1. Mobile-responsive layouts.
   2. Uniform typographies scaling via robust viewport logic rather than fixed-height containers.
5. Operability:
   1. Environment-driven config easily portable between SQLite local development and Cloud deployments.

## 8. Data Model Requirements
1. `Course(name)`; ordered by name.
2. `MockTest(course, year, duration)`; ordered newest year first.
3. `Question(mocktest, type=MCQ fixed, text, option_a-d, correct_answer, explanation, image [TextField], explanation_image [TextField])`.
4. `Result(user, mocktest, score, date)`; ordered latest first.
5. `UserProfile(user one-to-one, full_name, phone, bio, photo [ImageField over Cloudinary], photo_position_x/y, updated_at)`.

## 9. API/Endpoint Requirements
### Web Routes
1. `/` home.
2. `/register/`, `/login/`, `/logout/`.
3. `/dashboard/`, `/profile/`.
4. `/mock-tests/`, `/mock-tests/<course_id>/`.
5. `/start-test/<test_id>/`, `/submit-test/<test_id>/`, `/result/<test_id>/`.
6. `/upload-questions/` (staff only).

## 10. Analytics and Success Metrics
### Product KPIs
1. Registration-to-first-test conversion rate.
2. Weekly active test takers.
3. Question upload volumes and stability success rate.

### Operational KPIs
1. Concurrency extraction completion time benchmarks cleanly bypassing 100-sec thresholds.
2. Media load latency via Cloudinary nodes globally.

## 11. Known Deficits / Backlog
1. Registration form includes `confirm_password` input in UI but backend validation is currently trivialized.
2. `MockTest` retrieval utilizes traditional logic instead of strict `get_object_or_404`.
3. Timer and answer states are client-side only; a hard page refresh zeroes out in-progress test logic.
4. Missing automated CI/CD test suite validation.

## 12. Recommended Product Roadmap
### Phase 1 (Stability and Correctness)
1. Overhaul test auto-save states (synchronize timer and form radio choices to backend cache per tick).
2. Refactor routing handlers to strictly assert 404s.

### Phase 2 (Learning Quality)
1. Topic-wise and difficulty-wise tagging.
2. Attempt history charts and trend lines in User Profile.
3. Admin download reporting for analytics.

### Phase 3 (Scale and Engagement)
1. Course/year cohort public Leaderboards.
2. Personalized recommendation tracking.
3. Premium Mock subscription tier modeling.

---
*Updated April 2026 to reflect the complete extraction of legacy components (AI, Numeric pads, Ephemeral Local Storage, Fixed-Height cropping) towards the Multi-Image, Cloud-CDN driven pipeline architecture.*
