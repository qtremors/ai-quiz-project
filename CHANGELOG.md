# Changelog

All notable changes to the **Quizzer AI** project.

## [1.0.0] - 2025-11-19

### 🚀 Architecture & Core

- **Refactor:** Completely rebuilt the legacy project into a scalable `apps/` based architecture.
    
- **Settings:** Split configuration into `base.py` (shared) and `local.py` (dev).
    
- **Auth:** Implemented Custom User Model and secure session handling.
    

### 🧠 AI & Logic

- **Service Layer:** Created `QuizGenerator` service to abstract Gemini API calls.
    
- **Reliability:** Implemented JSON enforcement in prompts to prevent parsing errors.
    
- **Features:** Added support for "Coding Questions" (generating code snippets alongside text).
    
- **Agent:** Added a Natural Language Parser to convert chat messages (e.g., "Hard Python Quiz") into structured database queries.
    

### 🎨 UI/UX (The "Midnight" Theme)

- **Design:** Implemented a professional Dark Mode aesthetic using CSS Variables.
    
- **Layout:** * Created a 1600px wide responsive container for Dashboards.
    
    - Implemented a "Split View" layout for coding challenges (60/40 split).
        
    - Designed a Sticky Glassmorphism Navbar.
        
- **Interactions:**
    
    - Added HTMX loading states (spinners) to all major buttons.
        
    - Implemented Alpine.js dropdowns and form focus effects.
        
    - Created a seamless "Immersive Mode" for the Quiz Player (no scrolling required).
        

### 📱 Features

- **Dashboard:** Added a grid-based history view with score badges and stats.
    
- **Language Catalog:** Created a dedicated `/languages` page with Devicon integration.
    
- **Result Analysis:** Added "Explain All Mistakes" button that batch-processes wrong answers via AI and saves them to the DB.
    
- **Settings:** Added Profile management (Avatar upload, Username edit) and Password Reset flows.
    

### 🐛 Bug Fixes

- Fixed `floatform` template error by casting scores to integers in views.
    
- Fixed Navbar "Clone" bug by using `HX-Redirect` headers for page transitions.
    
- Fixed "Dots" on radio buttons by using `display: none` on inputs and styling labels.
    
- Fixed "Edit Button" overlap in settings by using Flexbox gaps.
    
- Fixed Language Auto-select logic to prioritize Custom Input over Dropdown.