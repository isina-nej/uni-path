Here is the comprehensive Product Requirement Document (PRD) for **Unipath**, based on your specifications.

# 1. Overview

* **Summary:** "Unipath" is a cross-platform mobile application (Flutter) with a robust backend (Django) designed to streamline the university course selection process. It acts as an intelligent academic advisor, allowing students to visualize their curriculum (Chart), track passed courses, and receive algorithmic recommendations for future semesters based on prerequisites, co-requisites, and course "importance" weights.
* **Problem Statement:** University students often struggle to optimize their course selection. They miss critical prerequisites, fail to understand the dependency chains (which courses unlock others), or create conflicting weekly schedules, leading to delayed graduation and academic inefficiency.
* **Goal:** To empower students to make data-driven decisions for their semester planning, ensuring they prioritize high-impact courses (bottlenecks) and graduate on time, while providing faculty with tools to manage curriculum data effectively.

# 2. Scope & Out of Scope

### In Scope

* **User Management:** specific roles for Student, Admin, Professor, and Head of Department (HOD).
* **Curriculum (Chart) Management:** Digital representation of course trees, credits (theoretical/practical), and semester structures.
* **Academic History:** Students marking passed courses; Professors inputting grades.
* **Recommendation Engine:** An algorithm that calculates an "Importance Score" for available courses based on dependency chains and suggests the best load.
* **Schedule Visualization:** A weekly calendar view for selected courses.
* **Notifications:** Alerts regarding course selection periods or changes.
* **Profile Management:** Editing personal info and viewing history.

### Out of Scope

* **Financial/Payments:** Tuition payment processing.
* **LMS Features:** Homework submission, file sharing, or online class streaming.
* **Official Registrar Sync (Phase 1):** Direct integration with the university’s legacy ERP/database (system will operate standalone with manual data entry/import for this version).

# 3. User Personas & Use Cases

### Personas

1. **Arash (The Student):** Wants to graduate ASAP. Needs to know which course to take now to avoid getting stuck later.
2. **Dr. Sohrabi (Head of Dept - HOD):** Needs to define the rules (Pre/Co-requisites) and ensure the curriculum structure is logical.
3. **Ms. Tehrani (Admin):** Handles data entry, creates course entities, and manages user access.
4. **Mr. Karimi (Professor):** Inputs grades and validates prerequisite rules for his specific courses.

### Key Use Cases

**UC-01: Smart Course Recommendation**

* **Pre-conditions:** Student has logged in and marked their "Passed Courses".
* **Post-conditions:** Student sees a prioritized list of courses for the upcoming semester.
* **Main Flow:**
1. System retrieves the student's passed courses and the Major's Chart.
2. System identifies all courses where prerequisites are met.
3. System calculates a **Weight Score** for each candidate course (Logic: Score = Number of direct + indirect future courses dependent on this course).
4. System displays courses sorted by this Score (High impact first).


* **Alternate Flow:** If no courses are available (e.g., everything passed), show "Graduation Ready" status.

**UC-02: Weekly Schedule Planning**

* **Pre-conditions:** Student has selected a set of proposed courses.
* **Post-conditions:** A visual weekly grid is generated.
* **Main Flow:**
1. Student selects 5-6 courses from the recommended list.
2. Student navigates to "My Schedule".
3. System renders a visual timetable (Sat-Thu).
4. System highlights any time conflicts (overlaps).



**UC-03: Curriculum Management (Admin/HOD)**

* **Pre-conditions:** User is Admin or HOD.
* **Main Flow:**
1. User selects a Field of Study (Major).
2. User adds a new Course (Name, Code, Credits).
3. User defines Relationships (Selects "Prerequisite" or "Co-requisite" courses from the database).
4. System updates the dependency graph.



# 4. Functional Requirements

### 4.1. Authentication & Profile

* **FR-1:** System must allow registration and login via Email/Student ID and Password.
* **FR-2:** System must enforce Role-Based Access Control (RBAC) for Student, Admin, Professor, HOD.
* **FR-3:** Users must be able to edit profile details (Name, Student Number, Major).

### 4.2. Core Data (Curriculum/Chart)

* **FR-4:** System must store Course entities with attributes: Name, Code, Unit Type (Theoretical/Practical), Credits, Description.
* **FR-5:** System must model relationships: One-to-Many for Prerequisites and Co-requisites.
* **FR-6:** Admins must be able to Create, Read, Update, Delete (CRUD) courses and charts.

### 4.3. Student Logic

* **FR-7:** Students must be able to toggle the status of a course to "Passed".
* **FR-8:** **Algorithm:** System must compute a dynamic score for every unpassed course.
* *Formula:* Score = .


* **FR-9:** System must filter courses: specific courses cannot be selected if prerequisites are not marked "Passed".
* **FR-10:** System must display a visual history of past semesters.

### 4.4. Faculty Logic

* **FR-11:** Professors must be able to input/upload grades for students enrolled in their specific courses.
* **FR-12:** HOD must be able to modify the prerequisite structure for their specific department.

# 5. Non-Functional Requirements

* **Tech Stack:**
* **Frontend:** Flutter (iOS, Android, Web).
* **Backend:** Python (Django + Django REST Framework).
* **Database:** PostgreSQL.


* **Performance:** Recommendation algorithm must run in under 2 seconds for a chart of <200 courses.
* **Scalability:** Database schema must support complex recursive queries (for dependency graphs).
* **Security:**
* Passwords hashed (Argon2 or PBKDF2).
* JWT (JSON Web Tokens) for session management.
* API endpoints must validate user permissions (e.g., A student cannot modify course prerequisites).


* **UX/Accessibility:** Support for Dark Mode. UI must be RTL (Right-to-Left) native for Persian text.

# 6. Integration & API Hints

The backend will expose a RESTful API. Key resources:

* `POST /api/auth/login`: Returns JWT.
* `GET /api/chart/{major_id}`: Returns full curriculum tree.
* `GET /api/student/progress`: Returns list of passed courses.
* `POST /api/student/grade`: (Professor only) Submit grade.
* `GET /api/recommendations`: Triggers the ranking engine.
* *Input:* Student ID.
* *Output:* JSON list of courses with `importance_score` and `reasoning`.



**Database dependency:**

* **PostgreSQL** is required specifically for its strong support of recursive queries (Common Table Expressions - CTEs) which are necessary to efficiently calculate the "depth" of course prerequisites.

# 7. Analytics & Success Metrics

* **Course Adoption Rate:** % of students who choose the "Top Recommended" courses versus ignoring the advice.
* **Schedule Conflict Reduction:** Decrease in error messages regarding time conflicts over time.
* **User Retention:** Weekly Active Users (WAU) during the enrollment window.

# 8. Risks & Open Questions

* **Risk:** **Circular Dependencies.** If an Admin accidentally sets Course A as a pre-req for Course B, and Course B as a pre-req for Course A, the algorithm will crash.
* *Mitigation:* Backend validation must detect and reject cycles during course creation.


* **Risk:** **Data Entry Load.** Inputting hundreds of courses manually is tedious.
* *Question:* Can we import an Excel/CSV file of the university chart to bootstrap the system?


* **Risk:** **Legacy Data.**
* *Question:* How do we handle students who transferred from other universities with partial credits? (Need a manual "Credit Override" feature).



# 9. Acceptance Criteria

The feature is "Done" when:

1. A student can log in and see their specific Major's chart.
2. After marking "Math 1" as passed, "Math 2" becomes available in the recommendation list.
3. "Math 1" (which unlocks 4 other courses) appears higher in the recommendation list than "General History" (which unlocks 0 courses).
4. The Weekly Schedule view correctly renders 5 selected courses without visual bugs.
5. An Admin can add a new course, and it immediately reflects in the chart.
6. The backend successfully blocks a student from selecting a course if they haven't passed the prerequisite.

---