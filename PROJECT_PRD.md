# AMU Entrance Portal - Product Requirements Document (PRD)

Version: 3.0  
Date: April 20, 2026  
Prepared from the latest codebase optimizations of `AMU_ Entrance_Portal`

## 1. Product Overview
AMU Entrance Portal is a high-end web-based mock test platform specifically designed for AMU aspirants. It seamlessly supports course-wise mock test discovery, timed test-taking, result analytics, advanced profile management, and a highly concurrent admin-driven question and image upload system powered by Cloudinary.

The product is built on Django and Bootstrap, heavily utilizing modern CSS (Midnight Glassmorphism aesthetics) and robust flexbox architecture to ensure production-grade reliability across all devices.

## 2. Vision and Goals
### Vision
Enable AMU aspirants to practice previous-year-style exams in a hyper-realistic, university-branded interface and improve through measurable performance insights and high-quality visual explanations.

### Primary Goals
1. Provide exam-like timed mock tests per AMU course/year.
2. Deliver immediate score feedback with per-question review and scalable multi-page visual explanations.
3. Offer an extremely fast, concurrent admin workflow for massive question-bank and multi-image ZIP uploads.
4. Scale media processing flawlessly using Cloudinary CDNs without breaking local storage constraints.
5. Provide a flawless aesthetic experience using modern web UI paradigms (Glassmorphism, seamless layout anchors).

### Non-Goals (Current Version)
1. Multi-language learning experience.
2. Integrated Payments/Subscriptions gateway.

## 3. Target Users
1. Aspirants (primary): register/login, attempt mocks, see results, track profile stats.
2. Admin/Content Team: manage courses/tests/questions via high-speed multi-threaded background imports.

## 4. Feature Scope (Current Production Implementation)

### 4.1 Authentication and UI Design
1. Secure Django Authentication (Login/Logout/Registration).
2. UI employs a **"Midnight Glassmorphism"** aesthetic leveraging inline Wikimedia AMU Gate assets to keep repository payloads zeroed out while delivering a highly prestigious identity across core landing and dashboard zones.
3. Fully isolated CSS namespaces ensuring components like student avatars and flex grids never overlap.

### 4.2 Courses and Mock Tests
1. Home page rendering categorized courses.
2. Filterable course/test lists relying on lightning-fast Postgres/SQLite queries.
3. "View All →" contextual routing architecture.

### 4.3 Exam Flow & Navigation Mechanics
1. Pre-test rules acceptance gate stored securely in local session data.
2. Timed test interface with sticky countdown overlays.
3. **Flawless Question Palette Navigation**: The test UI disables `loading="lazy"` on heavy exam images. This forces the browser to calculate document heights perfectly on mount, allowing the mock test palette buttons to instantly execute mathematically perfect `scrollIntoView(behavior:"smooth")` native jumps without mid-scroll DOM layout shifts.
4. MCQ answer capture mapped cleanly across standardized radio forms.

### 4.4 Result and Review Pipeline
1. Instant categorization: correct, incorrect, not attempted.
2. Performance percentiles mapped strictly against cohort metrics.
3. Per-question review rendering clean dynamic stacks of explanation images directly fetched via Cloudinary.
4. **Persistent Historical Vault**: Total test performance metadata (JSON payloads mapping individual user responses) is permanently injected into the database via backend serialization, allowing users to historically recreate dynamic result reports seamlessly.
5. Fractional float scoring supporting strict negative marking matrices.

### 4.5 Profile and Analytics Container
1. Robust drag-and-drop avatar framing persisting X/Y crop coordinates (`photo_position_x`, `photo_position_y`).
2. Centralized "Personal Information" GUI natively tracking contextual educational metrics (`institute`, `degree`) mapped faithfully to SQLite structural states.
3. Quick Stats Dashboard built purely on modern `flex-grow-1` constraints to prevent container intersections or bottom-margin text bleeding.
4. Interactive Historical Analytics table rows built out with hover physics seamlessly routing directly to historical test matrices securely.

### 4.6 Admin Bulk Ingestion Operations
1. Threaded `ThreadPoolExecutor` parsing architecture pushing 15+ API requests simultaneously.
2. **Background Upload Supervisor**: The view gracefully triggers Python's native `logging` daemon, logging potential asynchronous threading crashes completely out-of-band so that heavy 20MB zip extractions do not crash the primary HTTP 500 router or time-out Render instances.

## 5. Non-Functional Requirements
1. **Security**: CSRF enforcement; strict protected routes (`@login_required`).
2. **Performance**: Cloudinary CDN edge-caching; synchronous Eager fetching on critical test exam routes.
3. **Operability**: Configured perfectly for Render's ephemeral instance workflow via Postgres `DATABASE_URL` routing and WhiteNoise static middleware deployments.

## 6. Data Model Overview
1. `Course`: Name.
2. `MockTest`: Course FK, Year, Duration.
3. `Question`: MockTest FK, MCQ fields, Cloudinary Textual Arrays.
4. `Result`: User FK, Fractional float logic, Datetime stamps, JSON Vault metric storage.
5. `UserProfile`: Auth User FK, Avatar Cloudinary payloads, Interactive X/Y offsets, Native Educational Parameters.

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
*Updated April 20, 2026: Architecturally modified to document the integration of Persistent Historical Result tracking (JSON Data Models), FloatField negative scoring implementations, and Dynamic Educational Profile Fields.*
