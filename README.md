# 🚀 UTOPAI - AI Learning Platform for Children

UTOPAI is an interactive AI learning platform designed for children aged 9-12. Through gamified activities and personalized themes, children learn about AI, ChatGPT, and prompting in a fun and engaging way.

## ✨ Features

- **🎮 Gamified Learning:** Points, badges, and leaderboards
- **🎨 Theme Personalization:** Superhero or Princess themes
- **🤖 AI Integration:** Real ChatGPT interactions and learning
- **📱 Responsive Design:** Works on desktop, tablet, and mobile
- **🏝️ Island-based Learning:** Progress through different learning islands

## 🎯 Current Activities

### Ø 1: ChatGPT og Prompting
- **Activity 1:** "Hvad er ChatGPT?" - Interactive AI introduction
- **Activity 2:** "Dit første prompt" - Learn to build effective prompts

## 🛠️ Tech Stack

### Backend
- **Framework:** Flask (Python)
- **Database:** PostgreSQL (production) / SQLite (development)
- **AI Integration:** OpenAI GPT-3.5-turbo
- **Deployment:** Railway

### Frontend
- **Framework:** React + Vite
- **Styling:** Tailwind CSS + Radix UI
- **State Management:** React Hooks
- **Deployment:** Vercel

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- OpenAI API key

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
export OPENAI_API_KEY=your_openai_key
python start_server.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 📋 Deployment

### Railway (Backend)
1. Connect GitHub repository to Railway
2. Set environment variables:
   - `OPENAI_API_KEY`
   - `ALLOWED_ORIGINS`
   - `SECRET_KEY`
3. Add PostgreSQL database
4. Deploy automatically

### Vercel (Frontend)
1. Connect GitHub repository to Vercel
2. Set environment variables:
   - `VITE_API_BASE_URL`
3. Deploy automatically

## 📚 Documentation

- [Backend Deployment Guide](backend/README_DEPLOYMENT.md)
- [Frontend Deployment Guide](frontend/README_FRONTEND_DEPLOYMENT.md)
- [Integration Guide](README_INTEGRATION.md)
- [Testing Guide](README_FINAL_TESTING.md)
- [Complete Deployment Overview](DEPLOYMENT_COMPLETE.md)

## 🧪 Testing

```bash
# Backend API testing
python activity_test_suite.py https://your-backend-url

# UX validation
python user_experience_validator.py https://backend-url https://frontend-url

# Integration testing
python integration_test.py https://backend-url https://frontend-url
```

## 🔒 Security & Compliance

- HTTPS-only in production
- COPPA-compliant for children's platform
- Input validation and sanitization
- Secure session management

## 🎨 Themes

Children can choose between two engaging themes:
- **🦸‍♂️ Superhero Theme:** Learn AI with superhero examples and metaphors
- **👸 Princess Theme:** Explore AI through princess stories and adventures

## 🏆 Gamification

- **Points System:** Earn points for completing activities
- **Badge Collection:** Unlock badges for achievements
- **Leaderboard:** Compete with other learners
- **Progress Tracking:** Visual progress through learning islands

## 📈 Roadmap

### Phase 1 (Current)
- ✅ Activity 1: ChatGPT Introduction
- ✅ Activity 2: Prompt Building
- ✅ Gamification System
- ✅ Theme Personalization

### Phase 2 (Planned)
- 🔄 Activity 3: Clear vs Unclear Prompts
- 🔄 Activity 4: Chat with AI Mentor
- 🔄 Activity 5: Creative Prompt Challenge

### Phase 3 (Future)
- 🔄 Ø 2: Midjourney and AI Images
- 🔄 Ø 3: AI Video Generation
- 🔄 Advanced Analytics
- 🔄 Parent Dashboard

## 🤝 Contributing

This is a private educational project. For questions or suggestions, please contact the development team.

## 📄 License

Private educational project. All rights reserved.

## 🙏 Acknowledgments

- OpenAI for GPT-3.5-turbo API
- Railway for backend hosting
- Vercel for frontend hosting
- The amazing open-source community

---

**Built with ❤️ for young AI learners**

