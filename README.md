# 🚀 Amazon SDE II Interview Prep - AI Assistant

A comprehensive AI-powered interview preparation tool specifically designed for Amazon SDE II candidates. Features realistic interview simulation, progress tracking, and personalized coaching.

## ✨ Features

### 🤖 **Advanced AI Integration**
- **Gemini AI Powered**: Real-time interview simulation with follow-up questions
- **Demo Mode**: Works without API key for immediate testing
- **Personalized Feedback**: AI evaluates your responses and provides detailed feedback

### 🎪 **Live Interview Mode**
- **Realistic Simulation**: AI acts as a senior Amazon interviewer
- **Dynamic Follow-ups**: Questions adapt based on your responses
- **Timed Sessions**: Real interview pressure with countdown timer
- **Multiple Rounds**: DSA, System Design, and Behavioral interviews

### 📊 **Advanced Analytics**
- **Performance Tracking**: Score progression over time
- **Skill Breakdown**: Radar charts for DSA, System Design, Behavioral
- **Session Analysis**: Interview duration and question tracking
- **Data Persistence**: Your progress is automatically saved

### 🎨 **Modern UI/UX**
- **Dark Theme**: Professional glassmorphism design
- **Responsive**: Works on all devices
- **Animations**: Voice wave, glowing effects
- **Accessibility**: High contrast and clear text

## 🚀 Quick Start

### **Option 1: Demo Mode (No Setup Required)**
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `streamlit run main_app.py`
4. Enable "Demo Mode" in the sidebar
5. Start practicing immediately!

### **Option 2: Full AI Experience**
1. Get free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to `.env` file: `GEMINI_API_KEY=your_api_key_here`
3. Run: `streamlit run main_app.py`
4. Experience truly dynamic interview coaching!

## 📁 Project Structure

```
Interview-cursor/
├── main_app.py              # Main application
├── requirements.txt          # Python dependencies
├── .env                     # API key (private)
├── .gitignore              # Git ignore rules
├── .streamlit/config.toml  # Streamlit configuration
├── DEPLOYMENT_GUIDE.md     # Deployment instructions
└── README.md               # This file
```

## 🎯 Interview Types

### **💻 DSA Coding Round**
- Arrays, Trees, Graphs, Dynamic Programming
- 45-minute timed sessions
- Code + explanation evaluation
- Follow-up questions on optimization

### **🏗️ System Design Round**
- Scalability and architecture challenges
- 60-minute deep-dive sessions
- Database design and caching strategies
- Real-world system constraints

### **🎭 Behavioral Round**
- Amazon Leadership Principles
- STAR method responses
- 30-minute focused sessions
- Follow-up questions on impact and learning

## 📊 Dashboard Features

- **Readiness Score**: Overall preparation level
- **Practice Time**: Total time invested
- **Questions Solved**: Progress across categories
- **Live Sessions**: Interview simulation count
- **Performance Charts**: Visual progress tracking

## 🔧 Technical Details

### **Dependencies**
- `streamlit>=1.28.0`: Web framework
- `google-generativeai>=0.3.0`: AI integration
- `pandas>=2.0.0`: Data manipulation
- `plotly>=5.15.0`: Interactive charts
- `python-dotenv>=1.0.0`: Environment variables

### **Data Persistence**
- Automatic saving of progress
- Session history preservation
- Performance metrics tracking
- Secure local storage

## 🚀 Deployment

### **Streamlit Cloud (Recommended)**
1. Push to GitHub
2. Connect to [Streamlit Cloud](https://share.streamlit.io)
3. Set main file: `main_app.py`
4. Add environment variable: `GEMINI_API_KEY`

### **Alternative Platforms**
- **Heroku**: Add Procfile
- **Railway**: Connect GitHub repository
- **Render**: Set start command

## 🛡️ Security

- API keys stored in `.env` (not in Git)
- User data saved locally
- No sensitive information exposed
- Demo mode for safe testing

## 🎉 Success Stories

This tool has helped candidates:
- ✅ Improve interview confidence
- ✅ Master Amazon Leadership Principles
- ✅ Practice realistic interview scenarios
- ✅ Track progress systematically
- ✅ Get personalized feedback

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

- **Demo Mode**: Works immediately without setup
- **API Issues**: Check [Google AI Studio](https://makersuite.google.com/)
- **Deployment**: See `DEPLOYMENT_GUIDE.md`
- **Features**: All documented in the app

---

**Ready to ace your Amazon SDE II interview? Start practicing now!** 🚀 