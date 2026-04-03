# StudyBuddy - Build Plan & Implementation Guide

## 🎯 Project Overview

**StudyBuddy** is an enhanced student learning platform based on StudyBuddy with added performance review and analytics capabilities.

### **Core Features (from StudyBuddy)**
✅ AI Chatbot with Knowledge Base  
✅ Resources/Material Sharing  
✅ Resume Analyzer  
✅ YouTube Mindmap Generator  
✅ Progress Tracking & Habits  
✅ Admin Panel  
✅ Chat History  

### **NEW Feature: Performance Review System** ⭐
- Student performance analytics dashboard
- Skills assessment and scoring
- Progress reports and analytics
- Instructor/Admin reviews of student performance
- Performance comparisons and leaderboards
- Detailed performance metrics visualization

---

## 📋 Implementation Steps

### **Phase 1: Project Setup** (1-2 hours)

#### Step 1.1: Create New Project Directory
```bash
cd /Users/vinay/Documents/prep
cp -r StudyBuddy StudyBuddy
cd StudyBuddy
```

#### Step 1.2: Update Project Identity
- Update `.git/config` to point to new repo
- Update `README.md` with "StudyBuddy" branding
- Update `app/` folder name references
- Update all documentation

#### Step 1.3: Setup New Git Repository
```bash
git remote remove origin
git remote add origin https://github.com/YOUR-USERNAME/StudyBuddy.git
git config user.name "Your Name"
git config user.email "your.email@gmail.com"
git add .
git commit -m "Initial StudyBuddy project - based on StudyBuddy template"
git push -u origin main
```

---

### **Phase 2: Database Extensions** (2-3 hours)

#### Step 2.1: Add Performance Tracking Tables

**New Tables to Add in `app/db.py`:**

```python
# Table: student_performance
CREATE TABLE student_performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    overall_score REAL DEFAULT 0.0,
    skills_completed INTEGER DEFAULT 0,
    courses_completed INTEGER DEFAULT 0,
    average_test_score REAL DEFAULT 0.0,
    learning_velocity REAL DEFAULT 0.0,  # How fast they're learning
    consistency_score REAL DEFAULT 0.0,   # How regular they practice
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
)

# Table: performance_metrics
CREATE TABLE performance_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    metric_name TEXT NOT NULL,  # e.g., "quiz_completion", "code_quality"
    metric_value REAL NOT NULL,
    metric_date TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
)

# Table: performance_reviews
CREATE TABLE performance_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_email TEXT NOT NULL,
    reviewer_email TEXT NOT NULL,  # Admin/Instructor email
    review_title TEXT NOT NULL,
    review_content TEXT,
    rating REAL,  # 1-5 stars
    reviewed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
)

# Table: skills_assessment
CREATE TABLE skills_assessment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    skill_name TEXT NOT NULL,
    proficiency_level TEXT,  # Beginner, Intermediate, Advanced
    assessment_score REAL,
    last_assessed TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(email, skill_name)
)
```

#### Step 2.2: Add Database Functions in `app/db.py`
- `save_performance_metrics(db_path, email, metrics_dict)`
- `get_student_performance(db_path, email)`
- `update_overall_score(db_path, email, new_score)`
- `create_performance_review(db_path, student_email, reviewer_email, review_data)`
- `get_performance_reviews(db_path, email)`
- `get_skills_assessment(db_path, email)`
- `update_skills_assessment(db_path, email, skill_name, proficiency, score)`
- `get_performance_analytics(db_path, filters)`

---

### **Phase 3: Backend Features** (4-6 hours)

#### Step 3.1: Create Performance Module (`app/performance_engine.py`)

```python
class PerformanceEngine:
    """Handles calculation and tracking of student performance"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def calculate_overall_score(self, email: str) -> float:
        """Calculate overall performance score based on:
        - Quiz/Exam scores (40%)
        - Course completion (30%)
        - Consistency (20%)
        - Learning velocity (10%)
        """
        pass
    
    def track_learning_velocity(self, email: str) -> float:
        """How many courses/skills completed per week"""
        pass
    
    def calculate_consistency_score(self, email: str) -> float:
        """Based on daily practice frequency"""
        pass
    
    def generate_performance_report(self, email: str) -> dict:
        """Generate comprehensive performance report"""
        pass
    
    def identify_weak_areas(self, email: str) -> list:
        """Identify skills needing improvement"""
        pass
    
    def get_performance_comparison(self, email: str) -> dict:
        """Compare student with class average"""
        pass
```

#### Step 3.2: Add API Endpoints in `app/routes.py`

**New Routes:**
```python
# Performance Dashboard
GET /performance-review              # Student dashboard
GET /api/performance/score           # Get overall score
GET /api/performance/metrics         # Get detailed metrics
GET /api/performance/skills          # Get skills assessment
GET /api/performance/reviews         # Get admin reviews

# Admin Performance Management
GET /admin/performance               # Admin analytics dashboard
GET /api/admin/performance/all       # All students performance
POST /api/admin/performance/review   # Create performance review
GET /api/admin/performance/analytics # Generate analytics reports
```

#### Step 3.3: Performance Calculation Logic
- Integrate with mock tests scores
- Integrate with resource uploads/interactions
- Track course completion
- Calculate learning streaks
- Update on schedule (daily/weekly)

---

### **Phase 4: Frontend UI** (3-4 hours)

#### Step 4.1: New Templates

Create in `app/templates/`:
- `performance_review.html` - Student performance dashboard
- Performance charts and visualizations
- Skills radar chart
- Learning progress graph
- Admin performance management page

#### Step 4.2: New JavaScript Modules

Create in `app/static/js/`:
- `performance-dashboard.js` - Frontend logic
- Chart.js integration for visualizations
- Real-time performance updates

#### Step 4.3: New Stylesheets

Create in `app/static/css/`:
- `performance.css` - Performance page styling
- Chart styling and animations

---

### **Phase 5: Testing & Integration** (2-3 hours)

#### Step 5.1: Create Test Script
```python
# test_performance_system.py
- Test score calculations
- Test performance tracking
- Test review creation
- Test analytics generation
```

#### Step 5.2: Integration Testing
- Ensure new features work with existing modules
- Test chatbot performance recommendations
- Test admin notifications

---

## 📊 Database Schema Diagram

```
students (existing) ──┐
                      ├─→ student_performance ──→ performance_metrics
                      │
mock_tests (existing) ┤
                      ├─→ performance_reviews (NEW)
resources (existing)  │
                      ├─→ skills_assessment (NEW)
                      │
habits (existing) ────┘
```

---

## 🎨 UI/UX Changes

### **New Pages:**
1. **Performance Review** (`/performance-review`)
   - Overall score card
   - Skills assessment radar
   - Learning velocity graph
   - Performance reviews from instructors
   - Weak areas identification
   - Recommendations

2. **Admin Performance Dashboard** (`/admin/performance`)
   - Class analytics
   - Individual student performance
   - Performance trends
   - Review management
   - Export performance reports

### **Updated Pages:**
- Dashboard: Add performance summary card
- Admin panel: Add performance tab

---

## 🔄 Workflow: How Performance Review Works

```
┌─────────────────────────────────────────────────────┐
│ STUDENT ACTIVITIES                                  │
│ - Take quizzes                                      │
│ - Complete courses                                  │
│ - Upload resources                                  │
│ - Practice habits (daily)                           │
└─────────────────────────────────────────────────────┘
                    ↓
        [Performance Engine Tracking]
                    ↓
┌─────────────────────────────────────────────────────┐
│ CALCULATE METRICS                                   │
│ - Quiz scores → 40% weight                          │
│ - Course completion → 30% weight                    │
│ - Daily consistency → 20% weight                    │
│ - Learning velocity → 10% weight                    │
│ = OVERALL SCORE (0-100)                             │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ ADMIN REVIEW                                        │
│ - Write written review                              │
│ - Rate student (1-5 stars)                          │
│ - Highlight strong areas                            │
│ - Suggest improvements                              │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ STUDENT VIEWS                                       │
│ - Performance dashboard                             │
│ - Instructor reviews                                │
│ - Recommendations                                   │
│ - Areas to improve                                  │
└─────────────────────────────────────────────────────┘
```

---

## 📁 File Structure

```
StudyBuddy/
├── app/
│   ├── __init__.py
│   ├── db.py                    (UPDATED: add new tables)
│   ├── routes.py                (UPDATED: add new endpoints)
│   ├── performance_engine.py    (NEW)
│   ├── rag_pipeline.py
│   ├── kb_manager.py
│   ├── email_utils.py
│   ├── static/
│   │   ├── css/
│   │   │   ├── performance.css  (NEW)
│   │   │   └── ...
│   │   └── js/
│   │       ├── performance-dashboard.js  (NEW)
│   │       └── ...
│   └── templates/
│       ├── performance_review.html       (NEW)
│       └── ...
├── app/
│   ├── __init__.py
│   └── ... (existing)
├── run.py
├── requirements.txt             (UPDATED: add Chart.js, etc)
└── README.md                    (UPDATED: StudyBuddy branding)
```

---

## 🛠️ Tech Stack

**Same as StudyBuddy:**
- Backend: Flask, Python 3.9+
- Database: SQLite
- AI: OpenAI APIs
- Frontend: Jinja2, JavaScript

**NEW Libraries to Add:**
```
chart.js          # Visualizations
plotly            # Advanced charts
numpy             # Performance calculations
pandas            # Data analysis
```

---

## 📋 Implementation Timeline

| Phase | Task | Time |
|-------|------|------|
| 1 | Project Setup & Git | 1-2 hours |
| 2 | Database Schema | 2-3 hours |
| 3 | Backend API | 4-6 hours |
| 4 | Frontend UI | 3-4 hours |
| 5 | Testing & Bugs | 2-3 hours |
| **Total** | **All Phases** | **12-18 hours** |

---

## ✅ Next Steps

1. ✅ Create StudyBuddy directory (copy from StudyBuddy)
2. ✅ Update all project identities
3. ✅ Update git remote
4. ✅ Add database tables
5. ✅ Create performance_engine.py
6. ✅ Add new API endpoints
7. ✅ Create frontend pages
8. ✅ Test everything
9. ✅ Deploy

---

## 🚀 Ready to Start?

Would you like me to help you implement any phase first?

Recommended order:
1. Phase 1: Project Setup
2. Phase 2: Database Extensions
3. Phase 3: Backend
4. Phase 4: Frontend
5. Phase 5: Testing
