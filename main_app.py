import streamlit as st
import json
import time
import os
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any
import re
import google.generativeai as genai

# Optional dotenv import for local development
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not available, continue without it
    pass

# Page configuration
st.set_page_config(
    page_title="Amazon SDE II Interview Prep - AI Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS with better visibility and modern design
st.markdown("""
<style>
    /* Global styles for better visibility */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #ffffff;
    }
    
    /* Main header with advanced styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Interview Session Card */
    .interview-session-card {
        background: linear-gradient(135deg, rgba(255, 0, 150, 0.2) 0%, rgba(255, 0, 150, 0.1) 100%);
        backdrop-filter: blur(15px);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 0, 150, 0.3);
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(255, 0, 150, 0.3);
        color: #ffffff;
        text-align: center;
    }
    
    /* Live Interview Mode */
    .live-interview-mode {
        background: linear-gradient(135deg, rgba(0, 255, 0, 0.2) 0%, rgba(0, 255, 0, 0.1) 100%);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(0, 255, 0, 0.3);
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 255, 0, 0.2);
        color: #ffffff;
    }
    
    /* Recording Simulation */
    .recording-sim {
        background: linear-gradient(135deg, #ff4757 0%, #ff6b7a 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        animation: pulse 1.5s ease-in-out infinite alternate;
        margin: 1rem 0;
    }
    
    @keyframes pulse {
        from { transform: scale(1); box-shadow: 0 0 10px rgba(255, 71, 87, 0.5); }
        to { transform: scale(1.02); box-shadow: 0 0 20px rgba(255, 71, 87, 0.8); }
    }
    
    /* Advanced metric cards with glassmorphism */
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 0.8rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        color: #ffffff;
    }
    .metric-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    .metric-card h2 {
        color: #00d4ff;
        font-size: 2.5rem;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    }
    .metric-card h3 {
        color: #ffffff;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    .metric-card p {
        color: #b8c5d6;
        font-size: 0.9rem;
    }
    
    /* Advanced question cards */
    .question-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        color: #ffffff;
    }
    .question-card h4 {
        color: #00d4ff;
        font-size: 1.3rem;
        margin-bottom: 1rem;
    }
    .question-card p {
        color: #e0e6ed;
        line-height: 1.6;
    }
    
    /* Enhanced feedback styles */
    .feedback-positive {
        background: linear-gradient(135deg, rgba(40, 167, 69, 0.2) 0%, rgba(40, 167, 69, 0.1) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(40, 167, 69, 0.3);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(40, 167, 69, 0.2);
        color: #ffffff;
    }
    .feedback-negative {
        background: linear-gradient(135deg, rgba(220, 53, 69, 0.2) 0%, rgba(220, 53, 69, 0.1) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(220, 53, 69, 0.3);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(220, 53, 69, 0.2);
        color: #ffffff;
    }
    
    /* Advanced chat messages */
    .chat-message {
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .user-message {
        background: linear-gradient(135deg, rgba(33, 150, 243, 0.2) 0%, rgba(33, 150, 243, 0.1) 100%);
        margin-left: 20%;
        border-left: 4px solid #2196f3;
        color: #ffffff;
    }
    .ai-message {
        background: linear-gradient(135deg, rgba(255, 149, 0, 0.2) 0%, rgba(255, 149, 0, 0.1) 100%);
        margin-right: 20%;
        border-left: 4px solid #FF9500;
        color: #ffffff;
    }
    .interviewer-message {
        background: linear-gradient(135deg, rgba(128, 0, 128, 0.2) 0%, rgba(128, 0, 128, 0.1) 100%);
        margin-right: 20%;
        border-left: 4px solid #800080;
        color: #ffffff;
    }
    
    /* Timer display */
    .timer-display {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        padding: 1rem 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
    }
    
    /* Advanced buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 0.8rem 2rem;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Voice wave animation simulation */
    .voice-wave {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 8px;
        margin: 1rem 0;
    }
    
    .voice-wave span {
        width: 6px;
        height: 30px;
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        border-radius: 3px;
        animation: wave 1.2s ease-in-out infinite alternate;
    }
    
    .voice-wave span:nth-child(2) { animation-delay: 0.15s; }
    .voice-wave span:nth-child(3) { animation-delay: 0.3s; }
    .voice-wave span:nth-child(4) { animation-delay: 0.45s; }
    .voice-wave span:nth-child(5) { animation-delay: 0.6s; }
    
    @keyframes wave {
        0% { height: 20px; opacity: 0.3; }
        100% { height: 50px; opacity: 1; }
    }
    
    /* Advanced animations */
    @keyframes glow {
        0% { box-shadow: 0 0 5px rgba(0, 212, 255, 0.5); }
        50% { box-shadow: 0 0 20px rgba(0, 212, 255, 0.8); }
        100% { box-shadow: 0 0 5px rgba(0, 212, 255, 0.5); }
    }
    
    .glow-effect {
        animation: glow 2s ease-in-out infinite alternate;
    }
</style>
""", unsafe_allow_html=True) 

# Data persistence functions
def save_user_data():
    """Save user data to local storage"""
    data = {
        'chat_history': st.session_state.chat_history,
        'interview_sessions': st.session_state.interview_sessions,
        'performance_data': st.session_state.performance_data,
        'session_count': st.session_state.session_count,
        'total_study_time': st.session_state.total_study_time
    }
    
    # Save to local file (in production, you'd use a database)
    try:
        with open('user_data.json', 'w') as f:
            json.dump(data, f, default=str)
    except Exception as e:
        st.error(f"Error saving data: {e}")

def load_user_data():
    """Load user data from local storage"""
    try:
        with open('user_data.json', 'r') as f:
            data = json.load(f)
            
        st.session_state.chat_history = data.get('chat_history', [])
        st.session_state.interview_sessions = data.get('interview_sessions', [])
        st.session_state.performance_data = data.get('performance_data', {
            'dsa_scores': [],
            'system_design_scores': [],
            'behavioral_scores': [],
            'timestamps': []
        })
        st.session_state.session_count = data.get('session_count', 0)
        st.session_state.total_study_time = data.get('total_study_time', 0)
        
    except FileNotFoundError:
        # First time user, initialize with defaults
        pass
    except Exception as e:
        st.error(f"Error loading data: {e}")

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.current_session = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.chat_history = []
    st.session_state.interview_sessions = []
    st.session_state.performance_data = {
        'dsa_scores': [],
        'system_design_scores': [],
        'behavioral_scores': [],
        'timestamps': []
    }
    st.session_state.current_question = None
    st.session_state.current_category = None
    st.session_state.question_start_time = None
    st.session_state.total_study_time = 0
    st.session_state.gemini_client = None
    st.session_state.demo_mode = False
    st.session_state.live_interview_mode = False
    st.session_state.is_recording = False
    st.session_state.interview_timer = None
    st.session_state.follow_up_count = 0
    st.session_state.current_interview_questions = []
    st.session_state.session_count = 0
    
    # Load existing data
    load_user_data()

# Amazon Leadership Principles
LEADERSHIP_PRINCIPLES = [
    "Customer Obsession", "Ownership", "Invent and Simplify", "Are Right, A Lot",
    "Learn and Be Curious", "Hire and Develop the Best", "Insist on the Highest Standards",
    "Think Big", "Bias for Action", "Frugality", "Earn Trust", "Dive Deep",
    "Have Backbone; Disagree and Commit", "Deliver Results", "Strive to be Earth's Best Employer",
    "Success and Scale Bring Broad Responsibility"
]

# Enhanced Question banks with follow-up questions
DSA_QUESTIONS = [
    {
        "id": 1,
        "difficulty": "Medium",
        "topic": "Arrays",
        "question": "Given an array of integers, find two numbers such that they add up to a specific target number. Return indices of the two numbers.",
        "hints": ["Think about using a hash map", "What's the time complexity?"],
        "expected_approach": "Hash map for O(n) solution",
        "follow_ups": [
            "What if the array is sorted? Can you optimize further?",
            "How would you handle duplicate numbers?",
            "What if we need to find three numbers instead of two?",
            "Can you implement this without using extra space?"
        ]
    },
    {
        "id": 2,
        "difficulty": "Hard",
        "topic": "Dynamic Programming",
        "question": "Given a string s, find the longest palindromic substring in s. You may assume that the maximum length of s is 1000.",
        "hints": ["Consider expand around centers", "Think about Manacher's algorithm"],
        "expected_approach": "Expand around centers or dynamic programming",
        "follow_ups": [
            "Can you optimize the space complexity?",
            "How would you handle very large strings?",
            "What if we need to count all palindromic substrings?",
            "Explain the difference between your approach and Manacher's algorithm."
        ]
    },
    {
        "id": 3,
        "difficulty": "Medium",
        "topic": "Trees",
        "question": "Given a binary tree, determine if it is a valid binary search tree (BST).",
        "hints": ["In-order traversal should be sorted", "Think about bounds"],
        "expected_approach": "In-order traversal or bounds checking",
        "follow_ups": [
            "How would you handle duplicate values?",
            "Can you do this without extra space?",
            "What if the tree is very large and doesn't fit in memory?",
            "How would you modify this for a k-ary tree?"
        ]
    },
    {
        "id": 4,
        "difficulty": "Medium",
        "topic": "Graphs",
        "question": "Given a 2D grid representing a map where 1s are land and 0s are water, count the number of islands.",
        "hints": ["Use DFS or BFS", "Mark visited cells"],
        "expected_approach": "DFS/BFS with visited tracking",
        "follow_ups": [
            "How would you handle a very large grid?",
            "What if the grid is dynamic and changes over time?",
            "Can you solve this with Union-Find?",
            "How would you find the largest island?"
        ]
    }
]

SYSTEM_DESIGN_QUESTIONS = [
    {
        "id": 1,
        "question": "Design a URL shortening service like bit.ly",
        "focus_areas": ["Scalability", "Database design", "Caching", "Load balancing"],
        "key_components": ["URL encoding", "Database schema", "Cache layer", "Analytics"],
        "follow_ups": [
            "How would you handle 10x more traffic?",
            "What about custom URLs?",
            "How would you implement analytics and click tracking?",
            "What if we need to support different geographical regions?",
            "How would you prevent spam and malicious URLs?"
        ]
    },
    {
        "id": 2,
        "question": "Design a chat system like WhatsApp",
        "focus_areas": ["Real-time messaging", "Message delivery", "Scalability", "Security"],
        "key_components": ["WebSocket connections", "Message queuing", "Database design", "Push notifications"],
        "follow_ups": [
            "How would you implement group chats with 1000+ members?",
            "What about end-to-end encryption?",
            "How would you handle offline users and message delivery?",
            "What about file sharing and media messages?",
            "How would you implement message sync across multiple devices?"
        ]
    },
    {
        "id": 3,
        "question": "Design a video streaming service like YouTube",
        "focus_areas": ["Video processing", "CDN", "Scalability", "Storage"],
        "key_components": ["Video encoding", "Metadata storage", "Recommendation engine", "Analytics"],
        "follow_ups": [
            "How would you handle live streaming?",
            "What about video recommendations?",
            "How would you optimize for mobile vs desktop?",
            "What about content moderation at scale?",
            "How would you handle viral videos that get millions of views?"
        ]
    }
]

BEHAVIORAL_QUESTIONS = [
    {
        "principle": "Customer Obsession",
        "question": "Tell me about a time when you had to make a decision between what was best for the customer and what was best for the business.",
        "follow_ups": [
            "How did you measure the actual impact on customers?",
            "What was the business team's reaction to your decision?",
            "Would you make the same decision again? Why or why not?",
            "How did this experience influence your future decision-making?",
            "What metrics did you use to validate your choice?"
        ]
    },
    {
        "principle": "Ownership",
        "question": "Describe a situation where you took ownership of a problem that wasn't necessarily your responsibility.",
        "follow_ups": [
            "How did you convince others to support your initiative?",
            "What obstacles did you face and how did you overcome them?",
            "How did you ensure this problem wouldn't happen again?",
            "What did you learn about cross-team collaboration?",
            "How do you balance taking ownership with respecting boundaries?"
        ]
    },
    {
        "principle": "Dive Deep",
        "question": "Tell me about a time when you had to dig deep into data or details to solve a complex problem.",
        "follow_ups": [
            "What tools and techniques did you use for analysis?",
            "How did you know when you had enough information?",
            "What was the most surprising thing you discovered?",
            "How did you communicate your findings to stakeholders?",
            "What would you do differently if faced with a similar problem?"
        ]
    }
] 

def initialize_gemini_client():
    """Initialize Gemini API client"""
    st.sidebar.header("🔑 API Configuration")
    
    # Demo mode toggle
    demo_mode = st.sidebar.checkbox("🎭 Demo Mode (No API Key Required)", value=st.session_state.demo_mode)
    st.session_state.demo_mode = demo_mode
    
    if demo_mode:
        st.sidebar.success("✅ Demo mode enabled - using sample responses")
        return "demo"
    
    # Try to get API key from environment variable first
    env_api_key = os.getenv('GEMINI_API_KEY')
    
    if env_api_key:
        st.sidebar.success("✅ API Key loaded from environment")
        try:
            genai.configure(api_key=env_api_key)
            st.session_state.gemini_client = genai.GenerativeModel('gemini-1.5-pro')
            st.sidebar.success("✅ Gemini connected successfully!")
            return st.session_state.gemini_client
        except Exception as e:
            st.sidebar.error(f"Error with environment API key: {e}")
    
    # Fallback to manual input
    api_key = st.sidebar.text_input("Enter Gemini API Key (optional)", type="password", 
                                   help="Get your free API key from Google AI Studio")
    
    if api_key:
        # Test the API key
        if st.sidebar.button("🔍 Test API Key"):
            test_result = test_gemini_api_key(api_key)
            if test_result["success"]:
                st.sidebar.success("✅ API Key is working!")
            else:
                st.sidebar.error(f"❌ API Test Failed: {test_result['error']}")
        
        try:
            genai.configure(api_key=api_key)
            st.session_state.gemini_client = genai.GenerativeModel('gemini-1.5-pro')
            st.sidebar.success("✅ Gemini connected successfully!")
            return st.session_state.gemini_client
        except Exception as e:
            st.sidebar.error(f"Error initializing Gemini: {e}")
            return None
    
    if not env_api_key and not api_key:
        st.sidebar.info("💡 Add your API key to .env file or enter it manually")
    
    return None

def test_gemini_api_key(api_key: str) -> dict:
    """Test if the Gemini API key is valid and working"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content("Say 'Hello' if you can read this.")
        return {"success": True, "response": response.text}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_ai_response(prompt: str, context: str = "", is_interviewer: bool = False) -> str:
    """Get response from Gemini API or demo mode"""
    
    # Demo mode responses
    if st.session_state.demo_mode or st.session_state.gemini_client == "demo":
        return get_demo_response(prompt, is_interviewer)
    
    if not st.session_state.gemini_client:
        return "Please configure Gemini API key in the sidebar or enable demo mode."
    
    try:
        if is_interviewer:
            interviewer_prompt = f"""
            You are a senior Amazon Software Development Engineer II interviewer. You are professional, thorough, and realistic. 
            
            Context: {context}
            
            Candidate's response: {prompt}
            
            As an Amazon interviewer, you should:
            1. Ask probing follow-up questions to test deeper understanding
            2. Challenge assumptions and explore edge cases
            3. Evaluate the candidate's problem-solving approach
            4. Test their ability to think about trade-offs and optimizations
            5. Assess communication skills and technical depth
            6. Stay in character as a real interviewer - be encouraging but maintain professional standards
            7. Ask questions that would typically come up in a real Amazon SDE II interview
            
            Respond naturally as if you're in a real interview room. Keep responses focused and ask specific follow-up questions.
            """
        else:
            interviewer_prompt = f"""
            You are an expert Amazon SDE II interview coach. You provide detailed, constructive feedback and guidance.
            
            Context: {context}
            
            User: {prompt}
            
            Provide a comprehensive response that includes:
            1. Direct answer to the question/request
            2. Specific feedback and suggestions
            3. Areas for improvement
            4. Actionable advice for Amazon interviews
            """
        
        response = st.session_state.gemini_client.generate_content(interviewer_prompt)
        return response.text
    except Exception as e:
        error_msg = str(e)
        
        if "API_KEY_INVALID" in error_msg or "invalid" in error_msg.lower() or "404" in error_msg or "models/gemini-pro" in error_msg:
            return f"""🔴 **API Key Issue**

**Error:** {error_msg}

**Quick Fix:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Delete your current key**
3. **Create a new API key**
4. **Copy the ENTIRE key** (should be ~40 characters)
5. Paste it here

**Demo Mode:** Enable in sidebar for immediate testing!

**Common Issues:**
- Key is truncated/incomplete
- Key is expired
- Wrong API endpoint"""
        
        elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
            return f"""🔴 **API Quota Exceeded**

**Error:** {error_msg}

**Solutions:**
1. Check your quota at [Google AI Studio](https://makersuite.google.com/)
2. Wait for quota reset (daily limits)
3. Consider upgrading your plan
4. Use Demo Mode for now

**Demo Mode:** Available in sidebar!"""
        
        else:
            return f"""🔴 **API Error**

**Error:** {error_msg}

**Troubleshooting:**
1. Verify your API key is correct
2. Check internet connection
3. Try Demo Mode for immediate testing

**Demo Mode:** Enable in sidebar to continue!"""

def get_demo_response(prompt: str, is_interviewer: bool = False) -> str:
    """Get demo responses for interview simulation"""
    prompt_lower = prompt.lower()
    
    if is_interviewer:
        # Simulate realistic interviewer responses
        if "hash map" in prompt_lower or "two sum" in prompt_lower or "array" in prompt_lower:
            return """Great! I can see you understand the hash map approach. Let me dive deeper into your solution:

1. **Edge Case**: What happens if there are duplicate numbers in the array? Walk me through your logic.

2. **Optimization**: You mentioned O(n) time complexity. If the array was sorted, could we optimize this further? What would be the trade-offs?

3. **Space Complexity**: Can you think of a way to solve this without using the extra hash map space?

4. **Scale**: How would your solution perform with an array of 10 million integers?

Also, I noticed you mentioned returning indices. What if the problem asked for the actual values instead of indices? Would that change your approach?"""
        
        elif "system design" in prompt_lower or "url" in prompt_lower or "design" in prompt_lower:
            return """Good start on the architecture! I'd like to explore some specific areas deeper:

1. **Database Design**: You mentioned using a database. Would you choose SQL or NoSQL? Walk me through your table schema.

2. **URL Encoding**: What happens when you get hash collisions? How would you handle that at scale?

3. **Caching Strategy**: Where would you implement caching in your system? What would you cache and why?

4. **Scale**: If we need to handle 100 million URL shortenings per day, how would your design change?

5. **Analytics**: How would you track click metrics? What if a URL goes viral and gets millions of clicks in an hour?

Can you also walk me through the entire flow when a user clicks on a shortened URL?"""
        
        elif "behavioral" in prompt_lower or "customer" in prompt_lower or "ownership" in prompt_lower:
            return """Thank you for sharing that example. I can see you demonstrated strong ownership principles.

Let me ask some follow-up questions to understand the depth of your experience:

1. **Impact Measurement**: How did you quantify the success of your decision? What metrics did you track?

2. **Stakeholder Management**: You mentioned pushback from the business team. How specifically did you handle that resistance?

3. **Learning**: Looking back, what would you do differently? What did this experience teach you about balancing customer needs with business constraints?

4. **Long-term**: How has this experience influenced your decision-making in subsequent similar situations?

5. **Scale**: Have you faced similar decisions at a larger scale? How did your approach evolve?

I'm particularly interested in the specific actions YOU took versus what your team did."""
        
        elif "palindrome" in prompt_lower or "dynamic programming" in prompt_lower:
            return """Interesting approach! Let me challenge your solution a bit:

1. **Algorithm Choice**: You mentioned expand around centers. Why did you choose that over dynamic programming? What are the trade-offs?

2. **Space Optimization**: Your current solution uses O(1) space. Could you optimize it further for very long strings?

3. **Edge Cases**: How does your solution handle empty strings, single characters, or strings with no palindromes?

4. **Performance**: What's the worst-case scenario for your algorithm? Can you give me an example input?

5. **Alternative**: Have you heard of Manacher's algorithm? How would it compare to your approach?

Can you code up the expand around centers approach and walk me through it step by step?"""
        
        else:
            return """That's a solid response! Let me probe deeper to understand your thinking process:

1. **Alternative Approaches**: What other solutions did you consider? Why did you choose this one?

2. **Trade-offs**: Every solution has trade-offs. What are the downsides of your approach?

3. **Edge Cases**: Walk me through some edge cases. How would your solution handle them?

4. **Optimization**: If you had to optimize this for production at Amazon scale, what would you change?

5. **Testing**: How would you test this solution? What test cases would you write?

I'm also curious - what questions do you have for me about this problem or about working at Amazon?"""
    
    else:
        # Regular coaching responses
        if "system design" in prompt_lower:
            return """🎯 **System Design Interview Framework**

**Amazon's Approach (45-60 minutes):**

**1. Requirements Clarification (5-10 min)**
- Ask about scale: DAU, QPS, data volume
- Functional requirements: core features
- Non-functional: availability, consistency, latency

**2. High-Level Design (10-15 min)**
- Draw major components
- Show data flow
- Discuss API design

**3. Deep Dive (20-25 min)**
- Database schema and choice (SQL vs NoSQL)
- Detailed component design
- Key algorithms and data structures

**4. Scale & Optimize (10-15 min)**
- Identify bottlenecks
- Caching strategies
- Load balancing
- Monitoring and alerting

**Pro Tips for Amazon:**
- Start simple, then scale
- Discuss trade-offs for every decision
- Think about failure scenarios
- Consider operational aspects (monitoring, deployment)
- Be ready for deep technical questions"""
        
        elif "behavioral" in prompt_lower or "leadership" in prompt_lower:
            return """⭐ **Amazon Leadership Principles Mastery**

**STAR Method Structure:**
- **Situation (20%)**: Context and background
- **Task (20%)**: Your specific responsibility
- **Action (40%)**: What YOU did (most critical part)
- **Result (20%)**: Quantifiable outcomes and learning

**Top Principles for SDE II:**

**1. Customer Obsession**
- Put customer needs first, even when difficult
- Use data to understand customer impact
- Think long-term customer value

**2. Ownership**
- Take end-to-end responsibility
- Act on behalf of the entire company
- Never say "that's not my job"

**3. Dive Deep**
- Get into technical details
- Question assumptions with data
- Stay connected to the details

**4. Deliver Results**
- Focus on key inputs and deliver quality results
- Rise above setbacks and obstacles
- Take accountability for outcomes

**Interview Tips:**
- Prepare 2-3 detailed stories per principle
- Practice with specific metrics and outcomes
- Be ready for deep follow-up questions
- Show growth and learning from experiences"""
        
        elif "coding" in prompt_lower or "dsa" in prompt_lower:
            return """💻 **Amazon Coding Interview Strategy**

**Common Patterns at Amazon:**
1. **Array/String manipulation** (Two pointers, sliding window)
2. **Tree/Graph traversal** (DFS, BFS, tree problems)
3. **Dynamic Programming** (Optimization problems)
4. **System Design coding** (OOP design questions)

**Interview Process (45 min):**
1. **Problem Understanding (5 min)**
   - Ask clarifying questions
   - Confirm input/output format
   - Discuss constraints and edge cases

2. **Approach Discussion (10 min)**
   - Explain your approach before coding
   - Discuss time/space complexity
   - Consider multiple solutions

3. **Coding (20 min)**
   - Write clean, readable code
   - Think out loud
   - Handle edge cases

4. **Testing & Optimization (10 min)**
   - Test with examples
   - Look for bugs
   - Optimize if needed

**Amazon-Specific Tips:**
- Focus on clean, production-ready code
- Explain your thought process clearly
- Consider scalability and edge cases
- Be prepared for follow-up questions about optimization"""
        
        else:
            return """🤖 **Demo Mode Active - Gemini API Simulation**

I'm currently providing demo responses to showcase the interview simulation capabilities.

**🎯 What I Can Help With:**

**Live Interview Simulation:**
- Act as a real Amazon interviewer
- Ask follow-up questions based on your responses
- Challenge your assumptions and probe deeper
- Test edge cases and optimizations

**Interview Preparation:**
- System design frameworks and patterns
- Coding interview strategies and common problems
- Behavioral question preparation with STAR method
- Amazon Leadership Principles deep-dive

**🔑 To Unlock Full AI Power:**
1. Get a free Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Enter it in the sidebar
3. Experience truly dynamic, personalized interview coaching!

**💡 Try asking:**
- "Help me practice the Two Sum problem"
- "How should I approach system design questions?"
- "Give me a Customer Obsession behavioral question"

Ready for the most realistic interview practice available! 🚀"""

def evaluate_answer(question: dict, answer: str, category: str) -> dict:
    """Evaluate user's answer using AI"""
    evaluation_prompt = f"""
    Evaluate this {category} interview answer for Amazon SDE II position:
    
    Question: {question}
    Answer: {answer}
    
    Provide evaluation in this format:
    Score: X/10
    Strengths: [list specific strengths]
    Weaknesses: [list areas for improvement]  
    Suggestions: [actionable suggestions for improvement]
    Amazon Focus: [how this aligns with Amazon's standards]
    """
    
    ai_feedback = get_ai_response(evaluation_prompt)
    
    # Parse AI response to extract score
    score_match = re.search(r'Score:\s*(\d+)', ai_feedback)
    score = int(score_match.group(1)) if score_match else 5
    
    return {
        'score': score,
        'feedback': ai_feedback,
        'timestamp': datetime.now()
    } 

def start_live_interview():
    """Start a live interview session with real-time interaction"""
    st.session_state.live_interview_mode = True
    st.session_state.interview_timer = datetime.now()
    st.session_state.follow_up_count = 0
    st.session_state.current_interview_questions = []
    st.session_state.session_count += 1

def conduct_live_interview():
    """Conduct live interview with follow-up questions"""
    st.markdown("""
    <div class="live-interview-mode">
        <h3>🎪 Live Interview Mode - Amazon SDE II Simulation</h3>
        <p>You're now in a realistic Amazon interview. The AI will act as your senior interviewer with follow-up questions.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Timer display
    if st.session_state.interview_timer:
        elapsed = datetime.now() - st.session_state.interview_timer
        minutes = elapsed.seconds // 60
        seconds = elapsed.seconds % 60
        st.markdown(f"""
        <div class="timer-display">
            ⏱️ Interview Time: {minutes:02d}:{seconds:02d}
        </div>
        """, unsafe_allow_html=True)
    
    # Interview type selection
    interview_type = st.selectbox(
        "Select Interview Round",
        ["DSA Coding Round", "System Design Round", "Behavioral Round"],
        key="live_interview_type"
    )
    
    # Generate initial question if none exists or category changed
    if not st.session_state.current_question or st.session_state.current_category != interview_type:
        if interview_type == "DSA Coding Round":
            question_idx = st.session_state.session_count % len(DSA_QUESTIONS)
            question = DSA_QUESTIONS[question_idx]
            st.session_state.current_question = question
            st.session_state.current_category = "DSA"
            
        elif interview_type == "System Design Round":
            question_idx = st.session_state.session_count % len(SYSTEM_DESIGN_QUESTIONS)
            question = SYSTEM_DESIGN_QUESTIONS[question_idx]
            st.session_state.current_question = question
            st.session_state.current_category = "System Design"
            
        else:  # Behavioral
            question_idx = st.session_state.session_count % len(BEHAVIORAL_QUESTIONS)
            question = BEHAVIORAL_QUESTIONS[question_idx]
            st.session_state.current_question = question
            st.session_state.current_category = "Behavioral"
        
        # Reset follow-up count for new question
        st.session_state.follow_up_count = 0
    
    # Display current question
    question = st.session_state.current_question
    
    if st.session_state.current_category == "DSA":
        st.markdown(f"""
        <div class="question-card">
            <h4>🎯 Coding Question: {question['topic']} ({question['difficulty']})</h4>
            <p><strong>Interviewer:</strong> "{question['question']}"</p>
            <p><em>Take your time to understand the problem. Feel free to ask any clarifying questions before you start coding.</em></p>
            <p><strong>Hints available:</strong> {', '.join(question['hints'])}</p>
        </div>
        """, unsafe_allow_html=True)
        
    elif st.session_state.current_category == "System Design":
        st.markdown(f"""
        <div class="question-card">
            <h4>🏗️ System Design Challenge</h4>
            <p><strong>Interviewer:</strong> "{question['question']}"</p>
            <p><em>Let's start by clarifying the requirements. What questions do you have about the scope and scale?</em></p>
            <p><strong>Focus Areas:</strong> {', '.join(question['focus_areas'])}</p>
        </div>
        """, unsafe_allow_html=True)
        
    else:  # Behavioral
        st.markdown(f"""
        <div class="question-card">
            <h4>🎭 Behavioral Question: {question['principle']}</h4>
            <p><strong>Interviewer:</strong> "{question['question']}"</p>
            <p><em>Please structure your response using the STAR method - Situation, Task, Action, Result.</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Voice recording simulation section
    st.subheader("🎤 Response Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎤 Simulate Voice Recording", type="secondary", key="voice_sim"):
            st.session_state.is_recording = not st.session_state.is_recording
            st.rerun()
    
    with col2:
        if st.button("📝 Text Response", type="secondary", key="text_mode"):
            st.session_state.is_recording = False
            st.rerun()
    
    # Recording simulation display
    if st.session_state.is_recording:
        st.markdown("""
        <div class="recording-sim">
            🔴 VOICE RECORDING SIMULATION
            <div class="voice-wave">
                <span></span><span></span><span></span><span></span><span></span>
            </div>
            <p>In the full version, this would capture your voice response!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Auto-stop recording after demo
        time.sleep(0.1)  # Brief pause for effect
    
    # Response input
    st.subheader("💬 Your Response")
    response = st.text_area(
        "Share your solution, approach, or answer:",
        height=200,
        placeholder="Type your response here... Explain your thinking process clearly.",
        key="interview_response"
    )
    
    # Submit response button
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        submit_clicked = st.button("📤 Submit Response", type="primary", key="submit_response", use_container_width=True)
    
    if submit_clicked and response:
        # Get interviewer's follow-up response
        context = f"""
        Interview Type: {st.session_state.current_category}
        Current Question: {question}
        Follow-up Count: {st.session_state.follow_up_count}
        """
        
        interviewer_response = get_ai_response(
            response, 
            context, 
            is_interviewer=True
        )
        
        # Add to chat history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': response,
            'timestamp': datetime.now(),
            'question_context': question
        })
        
        st.session_state.chat_history.append({
            'role': 'interviewer',
            'content': interviewer_response,
            'timestamp': datetime.now()
        })
        
        # Increment follow-up count
        st.session_state.follow_up_count += 1
        
        # Clear the response box and show success
        st.success("✅ Response submitted! Check the interviewer's follow-up below.")
        st.rerun()
    
    # Display interview conversation
    if st.session_state.chat_history:
        st.subheader("💬 Interview Conversation")
        
        # Show recent conversation (last 6 messages for better context)
        recent_messages = st.session_state.chat_history[-6:]
        
        for msg in recent_messages:
            if msg['role'] == 'user':
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong> {msg['content']}
                </div>
                """, unsafe_allow_html=True)
            elif msg['role'] == 'interviewer':
                st.markdown(f"""
                <div class="chat-message interviewer-message">
                    <strong>🎯 Interviewer:</strong> {msg['content']}
                </div>
                """, unsafe_allow_html=True)
    
    # Interview controls
    st.subheader("🎮 Interview Controls")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔄 Next Question", key="next_question"):
            # Move to next question in sequence
            if st.session_state.current_category == "DSA":
                next_idx = (st.session_state.session_count) % len(DSA_QUESTIONS)
                st.session_state.current_question = DSA_QUESTIONS[next_idx]
            elif st.session_state.current_category == "System Design":
                next_idx = (st.session_state.session_count) % len(SYSTEM_DESIGN_QUESTIONS)
                st.session_state.current_question = SYSTEM_DESIGN_QUESTIONS[next_idx]
            else:  # Behavioral
                next_idx = (st.session_state.session_count) % len(BEHAVIORAL_QUESTIONS)
                st.session_state.current_question = BEHAVIORAL_QUESTIONS[next_idx]
            
            st.session_state.follow_up_count = 0
            st.session_state.session_count += 1
            st.rerun()
    
    with col2:
        if st.button("💡 Get Hint", key="get_hint"):
            if 'hints' in question:
                hint = question['hints'][st.session_state.follow_up_count % len(question['hints'])]
                st.info(f"💡 Hint: {hint}")
    
    with col3:
        if st.button("📊 Get Feedback", key="get_feedback"):
            if st.session_state.chat_history:
                # Get recent responses for evaluation
                recent_responses = [msg['content'] for msg in st.session_state.chat_history[-3:] if msg['role'] == 'user']
                if recent_responses:
                    feedback_context = f"Recent responses: {' | '.join(recent_responses)}"
                    feedback = get_ai_response(
                        "Please provide detailed feedback on the candidate's interview performance so far",
                        feedback_context
                    )
                    st.markdown(f"""
                    <div class="feedback-positive">
                        <h4>📊 Interview Feedback</h4>
                        <p>{feedback}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("Submit at least one response to get feedback!")
            else:
                st.warning("No responses yet to evaluate!")
    
    with col4:
        if st.button("🏁 End Interview", key="end_interview"):
            # Store session data
            session_data = {
                'timestamp': datetime.now(),
                'type': st.session_state.current_category,
                'duration': (datetime.now() - st.session_state.interview_timer).seconds // 60,
                'questions_asked': st.session_state.follow_up_count + 1,
                'responses': len([msg for msg in st.session_state.chat_history if msg['role'] == 'user'])
            }
            st.session_state.interview_sessions.append(session_data)
            
            # Save data automatically
            save_user_data()
            
            # Reset interview state
            st.session_state.live_interview_mode = False
            st.session_state.current_question = None
            st.session_state.follow_up_count = 0
            st.session_state.is_recording = False
            
            st.success("🎉 Interview session completed! Great job!")
            st.balloons()
            
            # Show session summary
            st.markdown(f"""
            <div class="feedback-positive">
                <h4>📋 Session Summary</h4>
                <p><strong>Duration:</strong> {session_data['duration']} minutes</p>
                <p><strong>Questions:</strong> {session_data['questions_asked']}</p>
                <p><strong>Responses:</strong> {session_data['responses']}</p>
                <p><strong>Type:</strong> {session_data['type']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            time.sleep(2)
            st.rerun() 

def main():
    # Advanced header with animations
    st.markdown("""
    <div class="main-header glow-effect">
        <h1>🚀 Amazon SDE II Interview Prep - AI Assistant</h1>
        <p>Advanced AI-powered preparation with realistic interviewer simulation</p>
        <div style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
            <span style="color: #00d4ff;">🤖</span> Powered by Gemini AI
            <span style="color: #00d4ff; margin-left: 1rem;">🎪</span> Live Interview Mode 
            <span style="color: #00d4ff; margin-left: 1rem;">🎯</span> Real-time Follow-ups
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize Gemini client
    if not st.session_state.gemini_client and not st.session_state.demo_mode:
        initialize_gemini_client()
        if not st.session_state.gemini_client and not st.session_state.demo_mode:
            st.markdown("""
            <div style="background: rgba(255, 193, 7, 0.1); padding: 1rem; border-radius: 10px; border-left: 4px solid #ffc107; margin: 1rem 0;">
                <h4>🔑 API Setup Required</h4>
                <p>Please enter your Gemini API key in the sidebar or enable demo mode to continue.</p>
                <p><a href="https://makersuite.google.com/app/apikey" target="_blank">Get your free API key here</a></p>
            </div>
            """, unsafe_allow_html=True)
            return
    
    # Main navigation
    if st.session_state.live_interview_mode:
        conduct_live_interview()
    else:
        # Sidebar navigation
        st.sidebar.header("📊 Navigation")
        page = st.sidebar.selectbox(
            "Choose Mode",
            ["🏠 Dashboard", "🎪 Live Interview", "💬 AI Chat Coach", "📝 Mock Interview", "📈 Progress Tracking", "📚 Resources"]
        )
        
        if page == "🏠 Dashboard":
            show_dashboard()
        elif page == "🎪 Live Interview":
            show_live_interview_page()
        elif page == "💬 AI Chat Coach":
            show_chat_coach()
        elif page == "📝 Mock Interview":
            show_mock_interview()
        elif page == "📈 Progress Tracking":
            show_progress_tracking()
        elif page == "📚 Resources":
            show_resources()

def show_live_interview_page():
    """Live interview setup page"""
    st.header("🎪 Live Interview Simulation")
    
    st.markdown("""
    <div class="interview-session-card">
        <h3>🚀 Realistic Amazon SDE II Interview Experience</h3>
        <p>Experience the most realistic interview simulation with AI-powered follow-up questions!</p>
        <ul style="text-align: left; margin: 1rem auto; max-width: 600px;">
            <li>🎯 <strong>Dynamic Questioning</strong> - AI asks follow-ups based on your responses</li>
            <li>⏱️ <strong>Real-time Pressure</strong> - Timed sessions with realistic interview flow</li>
            <li>🔄 <strong>Adaptive Difficulty</strong> - Questions get deeper as you progress</li>
            <li>📊 <strong>Live Feedback</strong> - Immediate evaluation and guidance</li>
            <li>🎤 <strong>Voice Simulation</strong> - Practice speaking your solutions</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Interview type selection with enhanced descriptions
    st.subheader("🎯 Choose Your Interview Round")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card" style="text-align: center;">
            <h3>💻 DSA Coding</h3>
            <p>Arrays, Trees, Graphs, DP</p>
            <p><strong>Duration:</strong> 45 minutes</p>
            <p><strong>Format:</strong> Code + Follow-ups</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start DSA Round", use_container_width=True, type="primary", key="start_dsa"):
            st.session_state.current_category = "DSA Coding Round"
            start_live_interview()
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="metric-card" style="text-align: center;">
            <h3>🏗️ System Design</h3>
            <p>Scalability, Architecture</p>
            <p><strong>Duration:</strong> 60 minutes</p>
            <p><strong>Format:</strong> Design + Deep Dive</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start System Design", use_container_width=True, type="primary", key="start_system"):
            st.session_state.current_category = "System Design Round"
            start_live_interview()
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="metric-card" style="text-align: center;">
            <h3>🎭 Behavioral</h3>
            <p>Leadership Principles</p>
            <p><strong>Duration:</strong> 30 minutes</p>
            <p><strong>Format:</strong> STAR + Follow-ups</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start Behavioral", use_container_width=True, type="primary", key="start_behavioral"):
            st.session_state.current_category = "Behavioral Round"
            start_live_interview()
            st.rerun()
    
    # Recent interview sessions
    if st.session_state.interview_sessions:
        st.subheader("📈 Recent Interview Sessions")
        
        sessions_df = pd.DataFrame(st.session_state.interview_sessions)
        sessions_df['timestamp'] = sessions_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        
        st.dataframe(
            sessions_df[['timestamp', 'type', 'duration', 'questions_asked', 'responses']],
            column_config={
                'timestamp': 'Date & Time',
                'type': 'Interview Type',
                'duration': 'Duration (min)',
                'questions_asked': 'Questions',
                'responses': 'Responses'
            },
            use_container_width=True
        )
    
    # Success tips
    st.subheader("💡 Tips for Maximum Success")
    
    tips_col1, tips_col2 = st.columns(2)
    
    with tips_col1:
        st.markdown("""
        **🎯 Before Starting:**
        - Find a quiet, focused environment
        - Have a whiteboard or paper ready
        - Prepare your mindset for realistic pressure
        - Review Amazon Leadership Principles
        
        **💬 During the Interview:**
        - Think out loud - explain your reasoning
        - Ask clarifying questions when needed
        - Don't be afraid to admit uncertainty
        - Stay calm and methodical in your approach
        """)
    
    with tips_col2:
        st.markdown("""
        **🔄 Follow-up Strategy:**
        - Listen carefully to follow-up questions
        - Build on your previous responses
        - Show depth of technical knowledge
        - Demonstrate problem-solving skills
        
        **📊 After Each Session:**
        - Review the feedback carefully
        - Identify specific areas for improvement
        - Practice weak areas before next session
        - Track your progress over time
        """)

def show_dashboard():
    """Enhanced dashboard with live interview metrics"""
    st.header("📊 Interview Preparation Dashboard")
    
    # Calculate metrics
    total_dsa = len(st.session_state.performance_data['dsa_scores'])
    total_system = len(st.session_state.performance_data['system_design_scores'])
    total_behavioral = len(st.session_state.performance_data['behavioral_scores'])
    total_questions = total_dsa + total_system + total_behavioral
    total_sessions = len(st.session_state.interview_sessions)
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate readiness score
    if total_questions > 0:
        avg_dsa = sum(st.session_state.performance_data['dsa_scores']) / max(len(st.session_state.performance_data['dsa_scores']), 1)
        avg_system = sum(st.session_state.performance_data['system_design_scores']) / max(len(st.session_state.performance_data['system_design_scores']), 1)
        avg_behavioral = sum(st.session_state.performance_data['behavioral_scores']) / max(len(st.session_state.performance_data['behavioral_scores']), 1)
        overall_score = ((avg_dsa + avg_system + avg_behavioral) / 3) * 10
    else:
        overall_score = 0
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎯 Readiness Score</h3>
            <h2>{overall_score:.0f}%</h2>
            <p>{'Ready to ace it!' if overall_score >= 80 else 'Good progress!' if overall_score >= 60 else 'Keep practicing!'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        study_hours = st.session_state.session_count * 0.5
        st.markdown(f"""
        <div class="metric-card">
            <h3>⏱️ Practice Time</h3>
            <h2>{study_hours:.1f}h</h2>
            <p>Total time invested</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📝 Questions Solved</h3>
            <h2>{total_questions}</h2>
            <p>Across all categories</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎪 Live Sessions</h3>
            <h2>{total_sessions}</h2>
            <p>Interview simulations</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick actions - updated to highlight live interview
    st.subheader("🚀 Quick Start Your Practice")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💻 DSA Practice", use_container_width=True):
            st.session_state.quick_start = "dsa"
            # Navigate to mock interview page
    
    with col2:
        if st.button("🏗️ System Design", use_container_width=True):
            st.session_state.quick_start = "system_design"
    
    with col3:
        if st.button("🎭 Behavioral Prep", use_container_width=True):
            st.session_state.quick_start = "behavioral"
    
    with col4:
        if st.button("🎪 Live Interview", use_container_width=True, type="primary"):
            show_live_interview_page()
    
    # Performance visualization
    if total_questions > 0:
        st.subheader("📈 Performance Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Create performance trend chart
            if st.session_state.performance_data['timestamps']:
                df_data = []
                for i, timestamp in enumerate(st.session_state.performance_data['timestamps']):
                    if i < len(st.session_state.performance_data['dsa_scores']):
                        df_data.append({'Date': timestamp, 'Score': st.session_state.performance_data['dsa_scores'][i], 'Type': 'DSA'})
                    if i < len(st.session_state.performance_data['system_design_scores']):
                        df_data.append({'Date': timestamp, 'Score': st.session_state.performance_data['system_design_scores'][i], 'Type': 'System Design'})
                    if i < len(st.session_state.performance_data['behavioral_scores']):
                        df_data.append({'Date': timestamp, 'Score': st.session_state.performance_data['behavioral_scores'][i], 'Type': 'Behavioral'})
                
                if df_data:
                    df = pd.DataFrame(df_data)
                    fig = px.line(df, x='Date', y='Score', color='Type', title="Performance Progress Over Time")
                    fig.update_layout(height=350, yaxis_range=[0, 10])
                    st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Skill breakdown radar chart
            skills = ['DSA', 'System Design', 'Behavioral']
            scores = [
                sum(st.session_state.performance_data['dsa_scores']) / max(len(st.session_state.performance_data['dsa_scores']), 1) if st.session_state.performance_data['dsa_scores'] else 0,
                sum(st.session_state.performance_data['system_design_scores']) / max(len(st.session_state.performance_data['system_design_scores']), 1) if st.session_state.performance_data['system_design_scores'] else 0,
                sum(st.session_state.performance_data['behavioral_scores']) / max(len(st.session_state.performance_data['behavioral_scores']), 1) if st.session_state.performance_data['behavioral_scores'] else 0
            ]
            
            fig = go.Figure(data=go.Scatterpolar(
                r=scores,
                theta=skills,
                fill='toself',
                name='Your Skills'
            ))
            fig.update_layout(
                height=350,
                polar=dict(radialaxis=dict(range=[0, 10])),
                title="Skill Breakdown"
            )
            st.plotly_chart(fig, use_container_width=True)

def show_chat_coach():
    """AI Chat Coach with Gemini"""
    st.header("💬 AI Interview Coach (Powered by Gemini)")
    st.markdown("""
    <div style="background: rgba(33, 150, 243, 0.1); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
        <strong>🤖 Your Personal AI Coach</strong><br>
        Get personalized guidance, practice specific problems, and receive expert feedback for your Amazon SDE II interview.
    </div>
    """, unsafe_allow_html=True)
    
    # Chat interface
    for i, message in enumerate(st.session_state.chat_history):
        if message['role'] == 'user':
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong> {message['content']}
            </div>
            """, unsafe_allow_html=True)
        elif message['role'] == 'assistant':
            st.markdown(f"""
            <div class="chat-message ai-message">
                <strong>🤖 AI Coach:</strong> {message['content']}
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Ask your AI coach anything about Amazon interviews...")
    
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now()
        })
        
        # Get AI response
        context = f"Amazon SDE II interview preparation. User preparing for interview."
        ai_response = get_ai_response(user_input, context)
        
        # Add AI response to history
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': ai_response,
            'timestamp': datetime.now()
        })
        
        st.rerun()
    
    # Suggested questions
    st.subheader("💡 Popular Questions")
    suggestions = [
        "How should I approach system design interviews?",
        "What are the key Amazon Leadership Principles for SDE II?",
        "Help me practice the Two Sum problem with follow-ups",
        "How can I improve my behavioral interview responses?",
        "What's the best way to handle coding interview pressure?",
        "Give me a Customer Obsession behavioral question"
    ]
    
    cols = st.columns(2)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(suggestion, key=f"suggestion_{i}", use_container_width=True):
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': suggestion,
                    'timestamp': datetime.now()
                })
                
                context = f"Amazon SDE II interview preparation. User preparing for interview."
                ai_response = get_ai_response(suggestion, context)
                
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': ai_response,
                    'timestamp': datetime.now()
                })
                
                st.rerun()

def show_mock_interview():
    """Traditional mock interview mode"""
    st.header("📝 Mock Interview Practice")
    
    st.info("💡 For the most realistic experience with follow-up questions, try the **Live Interview Mode** in the sidebar!")
    
    # Interview type selection
    interview_type = st.selectbox(
        "Select Practice Type",
        ["🔢 Data Structures & Algorithms", "🏗️ System Design", "🎭 Behavioral (Leadership Principles)"]
    )
    
    if "Data Structures" in interview_type:
        show_dsa_practice()
    elif "System Design" in interview_type:
        show_system_design_practice()
    else:
        show_behavioral_practice()

def show_dsa_practice():
    """DSA practice mode"""
    st.subheader("💻 Data Structures & Algorithms Practice")
    
    if st.button("🎲 Generate New DSA Question", type="primary"):
        question_idx = st.session_state.session_count % len(DSA_QUESTIONS)
        question = DSA_QUESTIONS[question_idx]
        st.session_state.current_question = question
        st.session_state.current_category = "DSA"
        st.session_state.question_start_time = datetime.now()
        st.session_state.session_count += 1
    
    if st.session_state.current_question and st.session_state.current_category == "DSA":
        question = st.session_state.current_question
        
        st.markdown(f"""
        <div class="question-card">
            <h4>🎯 {question['topic']} - {question['difficulty']}</h4>
            <p><strong>Question:</strong> {question['question']}</p>
            <p><strong>💡 Hints:</strong> {', '.join(question['hints'])}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Timer
        if st.session_state.question_start_time:
            elapsed = datetime.now() - st.session_state.question_start_time
            st.info(f"⏱️ Time elapsed: {elapsed.seconds // 60}m {elapsed.seconds % 60}s")
        
        # Code input
        st.subheader("💻 Your Solution")
        language = st.selectbox("Programming Language", ["Python", "Java", "C++", "JavaScript"])
        
        code_solution = st.text_area(
            "Write your code solution:",
            height=300,
            placeholder="def solution(nums, target):\n    # Your approach here\n    pass"
        )
        
        # Explanation input
        explanation = st.text_area(
            "Explain your approach and complexity:",
            height=150,
            placeholder="My approach is to...\nTime Complexity: O(?)\nSpace Complexity: O(?)"
        )
        
        if st.button("✅ Submit Solution", type="primary"):
            if code_solution and explanation:
                # Evaluate the solution
                full_answer = f"Code:\n{code_solution}\n\nExplanation:\n{explanation}"
                evaluation = evaluate_answer(question['question'], full_answer, "DSA")
                
                        # Store performance data
        st.session_state.performance_data['dsa_scores'].append(evaluation['score'])
        st.session_state.performance_data['timestamps'].append(datetime.now())
        
        # Save data automatically
        save_user_data()
        
        # Show feedback
        if evaluation['score'] >= 7:
            st.markdown(f"""
            <div class="feedback-positive">
                <h4>✅ Excellent! Score: {evaluation['score']}/10</h4>
                <p>{evaluation['feedback']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="feedback-negative">
                <h4>📈 Room for Improvement - Score: {evaluation['score']}/10</h4>
                <p>{evaluation['feedback']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Clear current question
        st.session_state.current_question = None
        st.session_state.current_category = None
    else:
        st.error("Please provide both code solution and explanation.")

def show_system_design_practice():
    """System design practice mode"""
    st.subheader("🏗️ System Design Practice")
    
    if st.button("🎲 Generate New System Design Question", type="primary"):
        question_idx = st.session_state.session_count % len(SYSTEM_DESIGN_QUESTIONS)
        question = SYSTEM_DESIGN_QUESTIONS[question_idx]
        st.session_state.current_question = question
        st.session_state.current_category = "System Design"
        st.session_state.question_start_time = datetime.now()
        st.session_state.session_count += 1
    
    if st.session_state.current_question and st.session_state.current_category == "System Design":
        question = st.session_state.current_question
        
        st.markdown(f"""
        <div class="question-card">
            <h4>🎯 {question['question']}</h4>
            <p><strong>🎪 Focus Areas:</strong> {', '.join(question['focus_areas'])}</p>
            <p><strong>🔧 Key Components:</strong> {', '.join(question['key_components'])}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Timer
        if st.session_state.question_start_time:
            elapsed = datetime.now() - st.session_state.question_start_time
            st.info(f"⏱️ Time elapsed: {elapsed.seconds // 60}m {elapsed.seconds % 60}s")
        
        # System design response sections
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Requirements & Scale")
            requirements = st.text_area(
                "Functional and Non-functional Requirements:",
                height=150,
                placeholder="Functional: Users can...\nNon-functional: Handle X requests/day, 99.9% availability..."
            )
            
            st.subheader("🎯 High-Level Design")
            high_level = st.text_area(
                "High-level architecture:",
                height=150,
                placeholder="Client -> Load Balancer -> API Gateway -> Services..."
            )
        
        with col2:
            st.subheader("🗄️ Database Design")
            database = st.text_area(
                "Database schema and technology choices:",
                height=150,
                placeholder="Tables, relationships, SQL vs NoSQL choice..."
            )
            
            st.subheader("⚡ Deep Dive & Scaling")
            deep_dive = st.text_area(
                "Detailed component discussion:",
                height=150,
                placeholder="Caching strategy, load balancing, monitoring..."
            )
        
        if st.button("✅ Submit Design", type="primary"):
            if all([requirements, high_level, database, deep_dive]):
                full_answer = f"Requirements: {requirements}\nHigh-level: {high_level}\nDatabase: {database}\nDeep dive: {deep_dive}"
                evaluation = evaluate_answer(question['question'], full_answer, "System Design")
                
                # Store performance data
                st.session_state.performance_data['system_design_scores'].append(evaluation['score'])
                st.session_state.performance_data['timestamps'].append(datetime.now())
                
                # Save data automatically
                save_user_data()
                
                # Show feedback
                if evaluation['score'] >= 7:
                    st.markdown(f"""
                    <div class="feedback-positive">
                        <h4>✅ Strong Design! Score: {evaluation['score']}/10</h4>
                        <p>{evaluation['feedback']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="feedback-negative">
                        <h4>📈 Areas to Strengthen - Score: {evaluation['score']}/10</h4>
                        <p>{evaluation['feedback']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Clear current question
                st.session_state.current_question = None
                st.session_state.current_category = None
            else:
                st.error("Please fill in all sections of the system design.")

def show_behavioral_practice():
    """Behavioral practice mode"""
    st.subheader("🎭 Behavioral Interview Practice")
    
    if st.button("🎲 Generate New Behavioral Question", type="primary"):
        question_idx = st.session_state.session_count % len(BEHAVIORAL_QUESTIONS)
        question = BEHAVIORAL_QUESTIONS[question_idx]
        st.session_state.current_question = question
        st.session_state.current_category = "Behavioral"
        st.session_state.question_start_time = datetime.now()
        st.session_state.session_count += 1
    
    if st.session_state.current_question and st.session_state.current_category == "Behavioral":
        question = st.session_state.current_question
        
        st.markdown(f"""
        <div class="question-card">
            <h4>🎯 Leadership Principle: {question['principle']}</h4>
            <p><strong>Question:</strong> {question['question']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("⭐ STAR Format Response")
        st.info("💡 Structure your answer using STAR: Situation, Task, Action, Result")
        
        # STAR format inputs
        col1, col2 = st.columns(2)
        
        with col1:
            situation = st.text_area(
                "🎬 Situation:",
                height=120,
                placeholder="Describe the context and background..."
            )
            
            action = st.text_area(
                "⚡ Action:",
                height=120,
                placeholder="What specific actions did YOU take..."
            )
        
        with col2:
            task = st.text_area(
                "📋 Task:",
                height=120,
                placeholder="What was your responsibility or goal..."
            )
            
            result = st.text_area(
                "🎯 Result:",
                height=120,
                placeholder="What was the outcome? Include metrics..."
            )
        
        if st.button("✅ Submit STAR Response", type="primary"):
            if all([situation, task, action, result]):
                full_answer = f"Situation: {situation}\n\nTask: {task}\n\nAction: {action}\n\nResult: {result}"
                evaluation = evaluate_answer(question['question'], full_answer, "Behavioral")
                
                # Store performance data
                st.session_state.performance_data['behavioral_scores'].append(evaluation['score'])
                st.session_state.performance_data['timestamps'].append(datetime.now())
                
                # Save data automatically
                save_user_data()
                
                # Show feedback
                if evaluation['score'] >= 7:
                    st.markdown(f"""
                    <div class="feedback-positive">
                        <h4>✅ Strong STAR Response! Score: {evaluation['score']}/10</h4>
                        <p>{evaluation['feedback']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="feedback-negative">
                        <h4>📈 Strengthen Your STAR - Score: {evaluation['score']}/10</h4>
                        <p>{evaluation['feedback']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Clear current question
                st.session_state.current_question = None
                st.session_state.current_category = None
            else:
                st.error("Please complete all STAR components.")

def show_progress_tracking():
    """Enhanced progress tracking"""
    st.header("📈 Advanced Progress Tracking & Analytics")
    
    # Performance overview
    if st.session_state.performance_data['timestamps']:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.session_state.performance_data['dsa_scores']:
                avg_dsa = sum(st.session_state.performance_data['dsa_scores']) / len(st.session_state.performance_data['dsa_scores'])
                st.metric("🔢 DSA Average", f"{avg_dsa:.1f}/10", f"+{avg_dsa-5:.1f}")
        
        with col2:
            if st.session_state.performance_data['system_design_scores']:
                avg_sys = sum(st.session_state.performance_data['system_design_scores']) / len(st.session_state.performance_data['system_design_scores'])
                st.metric("🏗️ System Design Average", f"{avg_sys:.1f}/10", f"+{avg_sys-5:.1f}")
        
        with col3:
            if st.session_state.performance_data['behavioral_scores']:
                avg_beh = sum(st.session_state.performance_data['behavioral_scores']) / len(st.session_state.performance_data['behavioral_scores'])
                st.metric("🎭 Behavioral Average", f"{avg_beh:.1f}/10", f"+{avg_beh-5:.1f}")
        
        # Performance trends
        st.subheader("📊 Detailed Performance Analysis")
        
        # Combine all scores for comprehensive view
        all_scores = []
        all_types = []
        all_timestamps = []
        
        for i, score in enumerate(st.session_state.performance_data['dsa_scores']):
            all_scores.append(score)
            all_types.append('DSA')
            all_timestamps.append(st.session_state.performance_data['timestamps'][i])
        
        for i, score in enumerate(st.session_state.performance_data['system_design_scores']):
            all_scores.append(score)
            all_types.append('System Design')
            if i < len(st.session_state.performance_data['timestamps']):
                all_timestamps.append(st.session_state.performance_data['timestamps'][i])
        
        for i, score in enumerate(st.session_state.performance_data['behavioral_scores']):
            all_scores.append(score)
            all_types.append('Behavioral')
            if i < len(st.session_state.performance_data['timestamps']):
                all_timestamps.append(st.session_state.performance_data['timestamps'][i])
        
        if all_scores:
            df = pd.DataFrame({
                'Score': all_scores,
                'Type': all_types,
                'Timestamp': all_timestamps[:len(all_scores)]  # Ensure same length
            })
            
            fig = px.line(df, x='Timestamp', y='Score', color='Type', 
                         title="Score Progression Over Time")
            fig.update_layout(height=400, yaxis_range=[0, 10])
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📝 Complete some practice questions to see your detailed progress!")
    
    # Interview sessions analysis
    if st.session_state.interview_sessions:
        st.subheader("🎪 Live Interview Sessions Analysis")
        
        sessions_df = pd.DataFrame(st.session_state.interview_sessions)
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_duration = sessions_df['duration'].mean()
            st.metric("⏱️ Avg Session Duration", f"{avg_duration:.1f} min")
        
        with col2:
            total_questions = sessions_df['questions_asked'].sum()
            st.metric("❓ Total Questions Asked", f"{total_questions}")
        
        with col3:
            avg_responses = sessions_df['responses'].mean()
            st.metric("💬 Avg Responses per Session", f"{avg_responses:.1f}")
        
        # Session breakdown chart
        if len(sessions_df) > 1:
            session_chart = px.bar(sessions_df, x='timestamp', y='duration', 
                                 color='type', title="Interview Session Durations")
            st.plotly_chart(session_chart, use_container_width=True)
    
    # Personalized recommendations
    st.subheader("🎯 AI-Powered Recommendations")
    
    if st.session_state.performance_data['timestamps']:
        recommendations = []
        
        # Analyze weak areas
        if st.session_state.performance_data['dsa_scores']:
            avg_dsa = sum(st.session_state.performance_data['dsa_scores']) / len(st.session_state.performance_data['dsa_scores'])
            if avg_dsa < 7:
                recommendations.append(f"🔢 **DSA Focus Needed** - Current average: {avg_dsa:.1f}/10. Practice more array and tree problems.")
        
        if st.session_state.performance_data['system_design_scores']:
            avg_sys = sum(st.session_state.performance_data['system_design_scores']) / len(st.session_state.performance_data['system_design_scores'])
            if avg_sys < 7:
                recommendations.append(f"🏗️ **System Design Improvement** - Current average: {avg_sys:.1f}/10. Focus on scalability patterns.")
        
        if st.session_state.performance_data['behavioral_scores']:
            avg_beh = sum(st.session_state.performance_data['behavioral_scores']) / len(st.session_state.performance_data['behavioral_scores'])
            if avg_beh < 7:
                recommendations.append(f"🎭 **Behavioral Enhancement** - Current average: {avg_beh:.1f}/10. Strengthen STAR method responses.")
        
        # Session-based recommendations
        if not st.session_state.interview_sessions:
            recommendations.append("🎪 **Try Live Interview Mode** - Experience realistic interview pressure with follow-up questions.")
        
        if len(st.session_state.interview_sessions) < 3:
            recommendations.append("🔄 **More Practice Needed** - Complete at least 3 live interview sessions for comprehensive preparation.")
        
        if not recommendations:
            recommendations.append("🎉 **Excellent Progress!** - You're performing well across all areas. Keep practicing to maintain your edge!")
        
        for rec in recommendations:
            st.markdown(f"• {rec}")
    else:
        st.markdown("""
        **🚀 Get Started:**
        • Complete your first practice question to see personalized recommendations
        • Try the Live Interview Mode for realistic practice
        • Focus on areas where you feel less confident
        """)

def show_resources():
    """Enhanced resources page"""
    st.header("📚 Comprehensive Interview Resources")
    
    tabs = st.tabs(["🔗 Essential Links", "📖 Study Guides", "🎯 Amazon Specific", "💡 Success Tips"])
    
    with tabs[0]:
        st.subheader("🌟 Top Preparation Resources")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **💻 Coding Practice:**
            - [LeetCode](https://leetcode.com/problemset/all/) - Essential DSA problems
            - [AlgoExpert](https://www.algoexpert.io/) - Video explanations
            - [Pramp](https://www.pramp.com/) - Mock interviews with peers
            - [InterviewBit](https://www.interviewbit.com/) - Structured learning path
            
            **🏗️ System Design:**
            - [System Design Primer](https://github.com/donnemartin/system-design-primer) - Comprehensive guide
            - [Grokking System Design](https://www.educative.io/courses/grokking-the-system-design-interview) - Structured course
            - [High Scalability](http://highscalability.com/) - Real system architectures
            - [AWS Architecture](https://aws.amazon.com/architecture/) - Cloud design patterns
            """)
        
        with col2:
            st.markdown("""
            **🎭 Behavioral Prep:**
            - [Amazon Leadership Principles](https://www.amazon.jobs/en/principles) - Official guide
            - [Glassdoor Amazon Reviews](https://www.glassdoor.com/Interview/Amazon-Interview-Questions-E6036.htm) - Real experiences
            - [Blind](https://www.teamblind.com/) - Anonymous employee insights
            - [Levels.fyi](https://www.levels.fyi/) - Compensation data
            
            **📚 Additional Resources:**
            - [Cracking the Coding Interview](https://www.amazon.com/Cracking-Coding-Interview-Programming-Questions/dp/0984782850) - Classic book
            - [Designing Data-Intensive Applications](https://www.amazon.com/Designing-Data-Intensive-Applications-Reliable-Maintainable/dp/1449373321) - System design deep dive
            - [YouTube Tech Channels](https://www.youtube.com/c/BackToBackSWE) - Free video tutorials
            """)
    
    with tabs[1]:
        st.subheader("📚 Structured Study Plans")
        
        study_plans = {
            "🔢 DSA Study Plan (2 weeks)": {
                "Week 1": [
                    "Day 1-2: Arrays & Strings (Two pointers, sliding window)",
                    "Day 3-4: Hash Tables & Sets (Fast lookups, counting)",
                    "Day 5-6: Linked Lists (Manipulation, cycle detection)",
                    "Day 7: Review and practice mixed problems"
                ],
                "Week 2": [
                    "Day 8-9: Trees & Binary Search Trees (Traversals, validation)",
                    "Day 10-11: Graphs (DFS, BFS, shortest path)",
                    "Day 12-13: Dynamic Programming (Memoization, bottom-up)",
                    "Day 14: Mock interview and review weak areas"
                ]
            },
            "🏗️ System Design Study Plan (1 week)": {
                "Days 1-2": [
                    "Fundamentals: Scalability, reliability, availability",
                    "Database concepts: SQL vs NoSQL, ACID, CAP theorem",
                    "Practice: Design a simple key-value store"
                ],
                "Days 3-4": [
                    "Caching strategies: LRU, write-through, write-back",
                    "Load balancing: Round-robin, consistent hashing",
                    "Practice: Design a URL shortener"
                ],
                "Days 5-7": [
                    "Microservices vs monoliths",
                    "Message queues and event-driven architecture",
                    "Practice: Design a chat system and social media feed"
                ]
            }
        }
        
        for plan_name, plan_details in study_plans.items():
            with st.expander(plan_name):
                for phase, tasks in plan_details.items():
                    st.write(f"**{phase}:**")
                    for task in tasks:
                        st.write(f"• {task}")
    
    with tabs[2]:
        st.subheader("🎯 Amazon-Specific Preparation")
        
        st.markdown("""
        ## 🏢 Amazon Interview Process Overview
        
        **SDE II Interview Structure:**
        1. **Phone Screen** (45 min) - 1 coding + behavioral
        2. **Virtual Onsite** (4-5 rounds):
           - 2x **Coding Interviews** (45 min each)
           - 1x **System Design** (60 min)
           - 1x **Behavioral/Bar Raiser** (45 min)
           - 1x **Hiring Manager** (30 min)
        
        ## 📋 Leadership Principles Deep Dive
        
        **Most Critical for SDE II:**
        """)
        
        principles_detail = {
            "Customer Obsession": "Start with customer needs and work backwards. Show data-driven decisions that prioritize customer experience.",
            "Ownership": "Take end-to-end responsibility. Act on behalf of the entire company, not just your team.",
            "Invent and Simplify": "Look for ways to innovate and simplify complex problems. Show creative problem-solving.",
            "Dive Deep": "Stay connected to the details. Audit frequently and question assumptions with data.",
            "Deliver Results": "Focus on key business inputs and deliver quality results despite setbacks."
        }
        
        for principle, description in principles_detail.items():
            st.markdown(f"**{principle}:** {description}")
        
        st.markdown("""
        ## 💰 Compensation Insights (2024)
        
        **Amazon SDE II Total Compensation:**
        - **Base Salary:** $130K - $170K
        - **Stock (RSUs):** $50K - $150K/year (vests over 4 years)
        - **Signing Bonus:** $20K - $50K (first 1-2 years)
        - **Total Package:** $200K - $370K
        
        *Note: Varies by location (Seattle, SF Bay Area typically higher)*
        """)
    
    with tabs[3]:
        st.subheader("💡 Expert Success Tips")
        
        tips_categories = {
            "🎯 Interview Day Strategy": [
                "Arrive 10-15 minutes early to settle in",
                "Bring multiple copies of your resume",
                "Prepare 3-4 thoughtful questions for each interviewer",
                "Practice your elevator pitch (30-60 seconds)",
                "Have specific examples ready for each leadership principle"
            ],
            "💻 Coding Interview Tactics": [
                "Always clarify the problem before coding",
                "Start with a brute force solution, then optimize",
                "Think out loud and explain your thought process",
                "Test your code with edge cases",
                "Ask about follow-up optimizations"
            ],
            "🏗️ System Design Strategy": [
                "Start with requirements gathering (5-10 minutes)",
                "Draw high-level architecture first",
                "Discuss trade-offs for every decision",
                "Think about failure scenarios and monitoring",
                "Be ready to dive deep into any component"
            ],
            "🎭 Behavioral Excellence": [
                "Use recent examples (within last 2 years)",
                "Focus on YOUR specific actions and decisions",
                "Include quantifiable results and metrics",
                "Show learning and growth from experiences",
                "Practice stories out loud with timing"
            ]
        }
        
        for category, tips in tips_categories.items():
            with st.expander(category):
                for tip in tips:
                    st.write(f"✅ {tip}")
        
        st.markdown("""
        ## 🔥 Final Week Preparation Checklist
        
        **3 Days Before:**
        - [ ] Complete final mock interviews in all areas
        - [ ] Review your resume and be ready to discuss every project
        - [ ] Prepare questions about Amazon's culture and role
        
        **1 Day Before:**
        - [ ] Light review only - avoid cramming
        - [ ] Prepare your setup (good lighting, stable internet)
        - [ ] Get a good night's sleep (8+ hours)
        
        **Interview Day:**
        - [ ] Eat a good breakfast
        - [ ] Do a technical warmup (1 easy coding problem)
        - [ ] Review your behavioral stories one final time
        - [ ] Stay confident and remember - they want you to succeed!
        """)

if __name__ == "__main__":
    main() 