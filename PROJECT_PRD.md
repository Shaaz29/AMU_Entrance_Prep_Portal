# AMU Entrance Portal - Product Requirements Document (PRD)

Version: 4.1  
Date: May 12, 2026  
Prepared from the latest codebase optimizations of `AMU_ Entrance_Portal`

## 1. Product Overview
AMU Entrance Portal is a high-end web-based mock test platform specifically designed for AMU aspirants. It seamlessly supports course-wise mock test discovery, timed test-taking, result analytics, advanced profile management, comprehensive Study Material provisioning with inline practice quizzes, and a highly concurrent admin-driven question and image upload system powered by Cloudinary.

The product is built on Django and Bootstrap, heavily utilizing modern CSS (Midnight Glassmorphism aesthetics) and robust flexbox architecture to ensure production-grade reliability across all devices.

## 2. Vision and Goals
### Vision
Enable AMU aspirants to practice previous-year-style exams in a hyper-realistic, university-branded interface, study categorized rich-text materials, and improve through measurable performance insights and highly interactive visual remediation.

### Primary Goals
1. Provide exam-like timed mock tests per AMU course/year with dynamic scaling palettes.
2. Deliver immediate score feedback with per-question review and scalable multi-page visual explanations.
3. Offer targeted Video Remediation and Alternate Practice questions specifically for areas of student weakness.
4. Offer an extremely fast, concurrent admin workflow for massive question-bank and multi-image ZIP uploads.
5. Scale media processing flawlessly using Cloudinary CDNs without breaking local storage constraints.
6. Provide a flawless aesthetic experience using modern web UI paradigms (Glassmorphism, seamless layout anchors).

### Non-Goals (Current Version)
1. Multi-language learning experience.
2. Integrated Payments/Subscriptions gateway.

## 3. Target Users
1. Aspirants (primary): register/login, study course notes, attempt mocks, see results, track profile stats.
2. Admin/Content Team: manage courses/tests/study materials via the customized Jazzmin dashboard and high-speed background imports.

## 4. Feature Scope (Current Production Implementation)

### 4.1 Authentication and UI Design
1. Secure Django Authentication (Login/Logout/Registration).
2. Advanced **OTP-based Forgot Password** flow using Brevo SMTP (configured with strict timeout rules and Port 2525 proxying for cloud-native worker stability).
3. **Password Visibility Toggles**: Interactive eye-icons on all authentication forms (Login, Register, Reset) for better user experience.
4. UI employs a **"Midnight Glassmorphism"** aesthetic leveraging inline Wikimedia AMU Gate assets.
5. Custom HTML Email templates for professional security interactions.

### 4.2 Study Materials & Curriculum
1. Rich-text editor integrated content publication (django-ckeditor).
2. Content strictly mapped by Course and dynamic `chapter_name` parameters for deep filtering.
3. Interactive "Practice Quizzes" seamlessly appended to the bottom of study materials to instantly test theoretical retention.

### 4.3 Courses and Mock Tests
1. Home page rendering categorized courses.
2. Filterable course/test lists relying on lightning-fast Postgres/SQLite queries.
3. "View All →" contextual routing architecture.

### 4.4 Exam Flow & Navigation Mechanics
1. Pre-test rules acceptance gate that dynamically counts attached questions.
2. Timed test interface with sticky countdown overlays.
3. **Flawless Question Palette Navigation**: Dynamic UI button matrices that natively expand to N-questions. The test UI disables `loading="lazy"` on heavy exam images, allowing the palette buttons to instantly execute mathematically perfect `scrollIntoView` jumps without DOM shifts.
4. MCQ answer capture mapped cleanly across standardized radio forms.

### 4.5 Result and Review Pipeline
1. Instant categorization: correct, incorrect, not attempted.
2. Performance percentiles mapped strictly against cohort metrics.
3. Per-question review rendering clean dynamic stacks of explanation images directly fetched via Cloudinary.
4. **Smart Video Remediation**: Automatically displays targeted YouTube video explanations exclusively for questions the student answered incorrectly or left blank.
5. **Interactive Alternate Questions**: Admin-defined alternate questions (with A/B/C/D interactive radio buttons and dropdown explanation toggles) displayed beneath remediation videos to instantly test concept mastery.
6. **Persistent Historical Vault**: Total test performance metadata is permanently injected into the database via backend serialization, allowing users to historically recreate dynamic result reports.
7. Fractional float scoring supporting strict negative marking matrices.

### 4.6 Profile and Analytics Container
1. Robust drag-and-drop avatar framing persisting X/Y crop coordinates (`photo_position_x`, `photo_position_y`).
2. Centralized "Personal Information" GUI tracking educational metrics mapped to SQLite states.
3. Interactive Historical Analytics table rows built out with hover physics seamlessly routing directly to historical test matrices.

### 4.7 Admin Bulk Ingestion & Management
1. **Jazzmin Dashboard**: The entire administrative pipeline is supercharged by `django-jazzmin`, featuring custom white-and-purple aesthetics mimicking modern SaaS metrics panels.
2. Threaded `ThreadPoolExecutor` parsing architecture pushing 15+ API requests simultaneously. Seamlessly supports dynamic column fallbacks (e.g., `question` vs `text` headers) and custom remediation fields (`youtube_link`, `alternate_image`, `alternate_explanation_image`).
3. Background Upload Supervisor gracefully utilizing Python's native `logging` daemon so heavy extractions do not crash Render HTTP instances.
4. Active `CONN_HEALTH_CHECKS` explicitly preventing database SSL drops over long-running proxy connections.

## 5. Non-Functional Requirements
1. **Security**: CSRF enforcement; strict protected routes (`@login_required`); OTP expirations strictly timed at 5-minutes.
2. **Performance**: Cloudinary CDN edge-caching; WhiteNoise strict-manifest toggling for smooth deployments of vendor libraries.
3. **Operability**: Configured perfectly for Render's ephemeral instance workflow via explicit timeout management and PostgreSQL health checks.

## 6. Data Model Overview
1. `Course`: Name.
2. `MockTest`: Course FK, Year, Duration.
3. `Question`: MockTest FK, MCQ fields, Cloudinary Textual Arrays, Video Links, and Custom Alternate Image references.
4. `Result`: User FK, Fractional float logic, JSON Vault metric storage.
5. `UserProfile`: Auth User FK, Avatar Cloudinary payloads, Interactive X/Y offsets, Native Educational Parameters.
6. `PasswordResetOTP`: Ephemeral numeric storage linked to User objects.
7. `StudyMaterial`: Course FK, Title, Chapter Name, Rich Text Content payload.
8. `PracticeQuestion`: StudyMaterial FK, MCQ fields.

## 7. Known Deficits / Backlog
1. Timer and answer states are client-side only; a hard page refresh zeroes out in-progress test logic.
2. Missing automated CI/CD test suite validation.

## 8. Recommended Product Roadmap
### Phase 1 (Data Resiliency)
1. Synchronize the countdown timer and radio choices to a continuous backend Ajax caching tick.

### Phase 2 (Student Motivation Loop)
1. Topic-wise difficulty tagging.
2. Attempt history line-charts in the Dashboard.

---
*Updated May 12, 2026: Architecturally modified to document the integration of Smart Video Remediation, Custom Alternate Practice Images, Password Visibility UI, and dynamic Excel header fallbacks.*
