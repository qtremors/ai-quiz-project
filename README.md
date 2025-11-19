# Quizzer AI

**Master Coding Interactively with Gemini AI**

Quizzer AI is a modern, adaptive learning platform designed for developers. It leverages Google's Gemini AI to generate infinite, customized quizzes on any programming topic—from Python syntax to System Design architecture.

Unlike static quiz apps, Quizzer AI generates fresh content on the fly, analyzes your answers, and provides context-aware explanations for every mistake you make.

## ✨ Key Features

### 🧠 AI-Powered Generation

- **Dynamic Content:** No database of pre-written questions. Every quiz is generated live based on your specific request.
    
- **Natural Language Agent:** Chat directly with the AI (e.g., _"Give me a hard quiz on React Hooks optimization"_) to generate a session.
    
- **Coding Challenges:** Supports code-based questions with a split-screen syntax highlighter (Prism.js) for realistic debugging scenarios.
    

### 🎮 Immersive Player

- **Distraction-Free UI:** A full-screen, focused interface designed for deep work.
    
- **Adaptive Layout:** Automatically switches between text-only and split-code layouts based on the question type.
    
- **Instant Interactions:** Powered by **HTMX** for a smooth, single-page-app feel without page reloads.
    

### 📊 Analytics & Growth

- **Smart Explanations:** Don't just see _what_ is wrong, understand _why_. Click "Explain All Mistakes" to get an AI breakdown of your specific logic errors.
    
- **History Tracking:** A dashboard that tracks every attempt, score, and topic mastery over time.
    
- **Persistent Storage:** All AI-generated explanations are cached in the database to save API costs and provide instant retrieval later.
    

### 🎨 Modern Aesthetic

- **Theme:** A professional "Midnight" dark theme inspired by my other projects.
    
- **Responsive:** Fully responsive grid layouts that work on mobile, tablet, and wide-screen desktops.
    
- **Visual Identity:** Custom brand assets, dynamic score badges, and Devicon integration.
    

## 🏗️ Tech Stack

- **Backend:** Django 5.2 (Python 3.11+)
    
- **AI Engine:** Google Generative AI SDK (Gemini 2.0 Flash Lite)
    
- **Frontend:**
    
    - **HTMX:** For server-side reactivity and AJAX navigation.
        
    - **Alpine.js:** For client-side interactions (modals, dropdowns).
        
    - **CSS:** Custom CSS Variables (Theming) & Flex/Grid layouts.
        
- **Database:** SQLite (Dev) / PostgreSQL Ready (Prod)
    
- **Utilities:** Prism.js (Syntax Highlighting), Devicon (Logos).
    

## 📂 Architecture

The project follows a **Domain-Driven Design** (DDD) within Django:

- `apps/core`: Global pages (Home, Language Catalog) and shared templates.
    
- `apps/users`: Custom Authentication, Profile Management, and Dashboards.
    
- `apps/quizzes`: The core domain logic (Quiz generation, Question storage, Attempt tracking).
    
- `apps/ai_agent`: Isolated service layer for communicating with Google Gemini.