# Learning by Bits

An intelligent web application that dynamically generates programming quizzes using the **Google Gemini AI**. Test your knowledge with personalized questions, receive instant feedback, and get AI-powered explanations for your mistakes.

---

## Features

### Dynamic Quiz Generation
- Leverages the Google Gemini API to create unique multiple-choice questions on the fly.

### Customizable Quizzes
Users can tailor quizzes by selecting:
- **Programming Language** (Python currently supported)
- **Difficulty Level** (Beginner, Intermediate, Advanced)
- **Specific Topics** (e.g., Data Types, OOP, Control Flow)
- **Number of Questions**

### AI-Powered Explanations
- For every incorrect answer, the AI provides a concise explanation to help you learn and improve.

### Interactive UI
- Smooth, single-page quiz-taking experience, managed by vanilla JavaScript.
- Asynchronous topic loading on the setup page without a page refresh.
- Loading animations during API calls to provide clear user feedback.

### Code Syntax Highlighting
- Code snippets within questions are beautifully formatted and highlighted using **Marked.js** and **Highlight.js**.

### User Experience Focused
- Clean, modern, and intuitive interface.
- Persistent Light/Dark theme toggle that remembers the user's choice.

---

## Technology Stack

- **Backend:** Django, Django REST Framework  
- **Frontend:** HTML, CSS, Vanilla JavaScript  
- **AI:** Google Gemini API  
- **Database:** SQLite (for development)  

---

## 🚀 Future Roadmap

### User Accounts & Progression
- Full authentication system with Google Sign-In and standard email/password.
- Leveling system (Beginner → Expert) where users can "level up" by mastering topics.
- Store all quiz history, answers, and performance statistics for authenticated users.
- Limited experience for anonymous users with pre-cached questions to encourage sign-ups.

### Advanced Quiz Engine & Content
- Hybrid system using local pool of questions for introductory topics and dynamic AI generation for advanced concepts.
- Expand content with more Python topics (decorators, concurrency) and new languages like JavaScript, C++, Go, and Rust.
- Flexible backend supporting multiple AI providers (OpenAI, Anthropic) and optional user API keys.

### Gamification & Engagement
- Visual learning roadmap or skill tree where users can "unlock" new concepts as they progress.
- Achievements, badges (e.g., "Python Basics Master", "10-Day Streak"), and other gamified elements.

### Enhanced Results & User Profiles
- Detailed analytics, including time taken per question.
- Export quiz results to Markdown or PDF for offline review.
- Comprehensive user profile page with performance graphs (accuracy over time, topic mastery) and a GitHub-style activity chart.

---

