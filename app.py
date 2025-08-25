import streamlit as st
import sqlite3
import hashlib
import re
import datetime

# Initialize database
def init_db():
    conn = sqlite3.connect('healthmate.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create chat history table
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            user_message TEXT,
            bot_response TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create symptom records table
    c.execute('''
        CREATE TABLE IF NOT EXISTS symptom_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            symptom TEXT NOT NULL,
            severity INTEGER,
            notes TEXT,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Create user
def create_user(username, email, password):
    conn = sqlite3.connect('healthmate.db')
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, hash_password(password))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Verify user
def verify_user(username, password):
    conn = sqlite3.connect('healthmate.db')
    c = conn.cursor()
    c.execute(
        "SELECT id, password_hash FROM users WHERE username = ?",
        (username,)
    )
    user = c.fetchone()
    conn.close()
    
    if user and user[1] == hash_password(password):
        return user[0]  # Return user ID
    return None

# Save chat history
def save_chat_history(user_id, user_message, bot_response):
    conn = sqlite3.connect('healthmate.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO chat_history (user_id, user_message, bot_response) VALUES (?, ?, ?)",
        (user_id, user_message, bot_response)
    )
    conn.commit()
    conn.close()

# Get chat history
def get_chat_history(user_id, limit=10):
    conn = sqlite3.connect('healthmate.db')
    c = conn.cursor()
    c.execute(
        "SELECT user_message, bot_response, timestamp FROM chat_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
        (user_id, limit)
    )
    history = c.fetchall()
    conn.close()
    return history

# Save symptom record
def save_symptom_record(user_id, symptom, severity, notes):
    conn = sqlite3.connect('healthmate.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO symptom_records (user_id, symptom, severity, notes) VALUES (?, ?, ?, ?)",
        (user_id, symptom, severity, notes)
    )
    conn.commit()
    conn.close()

# Get symptom history
def get_symptom_history(user_id, limit=10):
    conn = sqlite3.connect('healthmate.db')
    c = conn.cursor()
    c.execute(
        "SELECT symptom, severity, notes, recorded_at FROM symptom_records WHERE user_id = ? ORDER BY recorded_at DESC LIMIT ?",
        (user_id, limit)
    )
    history = c.fetchall()
    conn.close()
    return history

# Health Q&A function
def ask_healthmate(user_input):
    # Emergency keyword detection
    emergency_keywords = ['chest pain', 'difficulty breathing', 'fainting', 'severe bleeding', 'stroke', 'severe headache']
    if any(keyword in user_input.lower() for keyword in emergency_keywords):
        return "⚠️ Possible emergency detected! Please seek immediate medical attention. This assistant cannot handle emergencies, please call emergency services or go to the nearest hospital."
    
    # Symptom keyword mapping
    symptom_keywords = {
        'fever': ['fever', 'temperature', 'hot', 'sweating'],
        'headache': ['headache', 'head pain', 'migraine'],
        'cough': ['cough', 'coughing', 'phlegm'],
        'sore throat': ['sore throat', 'throat pain', 'swallowing pain'],
        'fatigue': ['tired', 'fatigue', 'exhausted', 'low energy'],
        'nausea': ['nausea', 'sick', 'vomit', 'queasy']
    }
    
    # Detect symptom keywords
    detected_symptom = None
    for symptom, keywords in symptom_keywords.items():
        if any(keyword in user_input.lower() for keyword in keywords):
            detected_symptom = symptom
            break
    
    # Get advice
    if detected_symptom:
        advice = get_health_advice(detected_symptom)
        
        # Build response
        response = f"**About {detected_symptom}:**\n\n{advice['description']}\n\n"
        response += "**Recommended actions:**\n"
        for i, item in enumerate(advice['advice'], 1):
            response += f"{i}. {item}\n"
        
        response += f"\n**When to see a doctor:**\n{advice['when_to_see_doctor']}\n\n"
    else:
        # General advice
        response = "Based on your description, here are some general health recommendations:\n\n"
        response += "1. Rest and allow your body time to recover\n"
        response += "2. Stay hydrated by drinking plenty of fluids\n"
        response += "3. Eat a balanced diet with plenty of fruits and vegetables\n"
        response += "4. Monitor your symptoms and note any changes\n"
        response += "5. Consider over-the-counter remedies if appropriate for your symptoms\n\n"
        response += "If your symptoms persist or worsen, it's important to consult with a healthcare professional for proper diagnosis and treatment.\n\n"
    
    # Add disclaimer
    response += "---\n"
    response += "⚠️ **Disclaimer:** This information is for educational purposes only and is not a substitute for professional medical advice. Always consult with a healthcare provider for proper diagnosis and treatment."
    
    return response

# Provide professional health advice based on symptoms
def get_health_advice(symptom):
    advice_dict = {
        'fever': {
            'description': 'Fever is a common symptom that indicates your body is fighting an infection.',
            'advice': [
                'Stay hydrated by drinking plenty of fluids',
                'Rest and allow your body to recover',
                'Use over-the-counter fever reducers like acetaminophen or ibuprofen (follow dosage instructions)',
                'Apply cool compresses to your forehead and wrists',
                'Monitor your temperature regularly'
            ],
            'when_to_see_doctor': 'If fever is above 103°F (39.4°C), lasts more than 3 days, or is accompanied by severe symptoms like difficulty breathing or rash.'
        },
        'headache': {
            'description': 'Headaches can have various causes including tension, dehydration, or underlying conditions.',
            'advice': [
                'Rest in a quiet, dark room',
                'Apply a cold or warm compress to your forehead or neck',
                'Stay hydrated',
                'Practice relaxation techniques like deep breathing',
                'Consider over-the-counter pain relievers if appropriate'
            ],
            'when_to_see_doctor': 'If headaches are severe, frequent, or accompanied by vision changes, confusion, or fever.'
        },
        'cough': {
            'description': 'Coughing is a reflex that helps clear your airways of irritants and mucus.',
            'advice': [
                'Stay hydrated to thin mucus',
                'Use a humidifier to add moisture to the air',
                'Try honey in warm tea (for adults and children over 1 year)',
                'Avoid irritants like smoke and strong perfumes',
                'Elevate your head with extra pillows while sleeping'
            ],
            'when_to_see_doctor': 'If cough persists for more than 3 weeks, is accompanied by fever, difficulty breathing, or produces bloody mucus.'
        },
        'sore throat': {
            'description': 'Sore throat is often caused by viral infections but can sometimes be bacterial.',
            'advice': [
                'Gargle with warm salt water',
                'Drink warm liquids like tea with honey',
                'Use throat lozenges or hard candy to increase saliva production',
                'Rest your voice',
                'Use a humidifier to add moisture to the air'
            ],
            'when_to_see_doctor': 'If sore throat is severe, lasts more than a week, or is accompanied by difficulty breathing or swallowing.'
        },
        'fatigue': {
            'description': 'Fatigue can be caused by various factors including lack of sleep, stress, or underlying health conditions.',
            'advice': [
                'Ensure you get 7-9 hours of quality sleep each night',
                'Maintain a regular sleep schedule',
                'Stay physically active with moderate exercise',
                'Eat a balanced diet with plenty of fruits and vegetables',
                'Manage stress through relaxation techniques'
            ],
            'when_to_see_doctor': 'If fatigue is persistent, severe, or accompanied by other symptoms like weight loss or fever.'
        },
        'nausea': {
            'description': 'Nausea can be caused by various factors including digestive issues, infections, or motion sickness.',
            'advice': [
                'Eat small, bland meals throughout the day',
                'Avoid strong odors and spicy or fatty foods',
                'Stay hydrated with small sips of clear fluids',
                'Try ginger tea or ginger candies',
                'Get plenty of fresh air'
            ],
            'when_to_see_doctor': 'If nausea is severe, persistent, or accompanied by vomiting, fever, or abdominal pain.'
        }
    }
    
    # Default response
    default_response = {
        'description': 'This is a general health concern.',
        'advice': [
            'Rest and allow your body time to recover',
            'Stay hydrated by drinking plenty of fluids',
            'Monitor your symptoms and seek medical attention if they worsen'
        ],
        'when_to_see_doctor': 'If symptoms persist for more than a few days or become severe.'
    }
    
    return advice_dict.get(symptom.lower(), default_response)

# Generate health tips
def generate_health_tip():
    tips = [
        "Drink enough water daily - aim for 8 glasses to stay properly hydrated.",
        "Regular exercise is key to good health - aim for at least 150 minutes of moderate activity per week.",
        "Eat a variety of colorful fruits and vegetables - aim for at least 5 servings daily.",
        "Prioritize quality sleep - adults need 7-9 hours per night for optimal health.",
        "Reduce processed foods and sugar - choose whole grains and lean proteins instead.",
        "Manage stress levels through meditation, deep breathing, or enjoyable hobbies.",
        "Get regular health check-ups to detect potential issues early.",
        "Practice good posture, especially if you sit for long periods.",
        "Use sunscreen daily, even on cloudy days, to protect your skin.",
        "Maintain social connections - strong relationships contribute to mental wellbeing.",
        "Take breaks from screens every hour to reduce eye strain and improve posture.",
        "Practice mindful eating - pay attention to hunger cues and eat slowly.",
        "Include strength training in your exercise routine at least twice a week.",
        "Limit alcohol consumption and avoid smoking for better long-term health.",
        "Practice gratitude daily - it can improve mental health and overall wellbeing."
    ]
    
    # Select tip based on day of year
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    return tips[day_of_year % len(tips)]

# Initialize database
init_db()

# Page configuration
st.set_page_config(
    page_title="GPT-HealthMate Health Assistant",
    page_icon="🩺",
    layout="centered"
)

# Application title
st.title("🩺 GPT-HealthMate Health Assistant")

# Initialize session state
if "user" not in st.session_state:
    st.session_state.user = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "page" not in st.session_state:
    st.session_state.page = "Login"

# Display navigation menu in main content area
if not st.session_state.user:
    # Display navigation menu without label
    menu = st.radio("", ["Login", "Register"], horizontal=True)
    
    # Display info message below navigation menu
    st.info("Please login or register to use the health assistant")
else:
    # For logged in users, display in sidebar
    with st.sidebar:
        st.success(f"Welcome, {st.session_state.user}!")
        menu = st.radio("Navigation Menu", ["Health Q&A", "BMI Calculator", "Daily Tips", "Symptom Tracker", "Chat History"])
        if st.button("Logout"):
            st.session_state.user = None
            st.session_state.user_id = None
            st.session_state.page = "Login"
            st.rerun()

# Login page
if not st.session_state.user and menu == "Login":
    st.subheader("User Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            user_id = verify_user(username, password)
            if user_id:
                st.session_state.user = username
                st.session_state.user_id = user_id
                st.session_state.page = "Health Q&A"
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")

# Registration page - All fields left-aligned in single column
elif not st.session_state.user and menu == "Register":
    st.subheader("User Registration")
    
    # All fields in a single column, left-aligned
    username = st.text_input("Username", key="reg_username")
    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
    
    # Register button
    submitted = st.button("Register", use_container_width=True)
    
    if submitted:
        if not username or not email or not password:
            st.error("Please fill in all fields")
        elif password != confirm_password:
            st.error("Passwords do not match")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.error("Please enter a valid email address")
        else:
            if create_user(username, email, password):
                st.success("Registration successful! Please login")
                st.session_state.page = "Login"
                st.rerun()
            else:
                st.error("Username or email already exists")

# Health Q&A page
elif st.session_state.user and menu == "Health Q&A":
    st.subheader("Health Q&A Assistant")
    st.info("Describe your symptoms or health concerns, and I'll provide general advice.")
    
    # Symptom selector
    common_symptoms = ["Fever", "Headache", "Cough", "Sore throat", "Fatigue", "Nausea", "Other"]
    selected_symptom = st.selectbox("Select your main symptom:", common_symptoms)
    
    # Detailed description
    if selected_symptom == "Other":
        user_input = st.text_area("Please describe your symptoms in detail:", height=100)
    else:
        user_input = st.text_area(f"Please describe your {selected_symptom.lower()} in detail:", height=100)
    
    if st.button("Get Advice"):
        if user_input:
            with st.spinner("Analyzing your symptoms..."):
                # Get professional advice
                response = ask_healthmate(user_input)
                save_chat_history(st.session_state.user_id, user_input, response)
                
                # Display advice
                st.success("Here's my advice based on your symptoms:")
                st.markdown(response)
        else:
            st.warning("Please describe your symptoms.")

# BMI Calculator page
elif st.session_state.user and menu == "BMI Calculator":
    st.subheader("BMI Calculator")
    st.info("Calculate your Body Mass Index and get personalized health recommendations.")
    
    # Input method selection
    input_method = st.radio("Select input method:", ["Sliders", "Manual Input"])
    
    if input_method == "Sliders":
        col1, col2 = st.columns(2)
        with col1:
            height = st.slider("Height (cm)", 100, 250, 170)
        with col2:
            weight = st.slider("Weight (kg)", 30, 200, 70)
    else:
        col1, col2 = st.columns(2)
        with col1:
            height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0, step=0.1)
        with col2:
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=65.0, step=0.1)
    
    # Additional information
    age = st.slider("Age", 1, 100, 30)
    gender = st.radio("Gender", ["Male", "Female"])
    
    if st.button("Calculate BMI"):
        if height > 0 and weight > 0:
            height_m = height / 100
            bmi = weight / (height_m ** 2)
            
            st.metric("Your BMI", f"{bmi:.2f}")
            
            # Detailed classification and recommendations
            if bmi < 16:
                st.error("Severely underweight")
                st.info("""
                **Recommendations:**
                - Consult with a healthcare provider for a comprehensive evaluation
                - Work with a nutritionist to develop a healthy weight gain plan
                - Focus on nutrient-dense foods rather than empty calories
                - Consider small, frequent meals throughout the day
                """)
            elif bmi < 18.5:
                st.warning("Underweight")
                st.info("""
                **Recommendations:**
                - Gradually increase calorie intake with healthy foods
                - Include protein-rich foods in your diet
                - Strength training can help build muscle mass
                - Monitor your progress and adjust as needed
                """)
            elif bmi < 25:
                st.success("Healthy weight")
                st.info("""
                **Recommendations:**
                - Maintain your current healthy habits
                - Continue balanced nutrition and regular physical activity
                - Regular health check-ups are still important
                - Focus on maintaining rather than changing your weight
                """)
            elif bmi < 30:
                st.warning("Overweight")
                st.info("""
                **Recommendations:**
                - Consider gradual weight loss through diet and exercise
                - Focus on whole foods and reduce processed foods
                - Aim for at least 150 minutes of moderate exercise per week
                - Set realistic goals and track your progress
                """)
            else:
                st.error("Obese")
                st.info("""
                **Recommendations:**
                - Consult with a healthcare provider for a personalized plan
                - Consider working with a dietitian or nutritionist
                - Focus on sustainable lifestyle changes rather than quick fixes
                - Even modest weight loss (5-10%) can provide significant health benefits
                """)
            
            # Add age and gender-based recommendations
            st.markdown("---")
            st.subheader("Personalized Recommendations")
            
            if age < 25:
                st.info("As a young adult, focus on establishing healthy habits that will benefit you throughout your life.")
            elif age < 50:
                st.info("In your middle years, maintaining a healthy weight becomes increasingly important for long-term health.")
            else:
                st.info("As an older adult, focus on maintaining muscle mass and bone density through appropriate exercise and nutrition.")
                
            if gender == "Female":
                st.info("Women should pay particular attention to bone health through adequate calcium and vitamin D intake.")
        else:
            st.error("Please enter valid height and weight values")

# Daily Tips page
elif st.session_state.user and menu == "Daily Tips":
    st.subheader("Daily Health Tips")
    
    if st.button("Get Today's Tip"):
        tip = generate_health_tip()
        st.info(tip)
        
        # Save to chat history
        save_chat_history(
            st.session_state.user_id, 
            "Requested daily health tip", 
            f"Today's tip: {tip}"
        )

# Symptom Tracker page
elif st.session_state.user and menu == "Symptom Tracker":
    st.subheader("Symptom Tracker")
    st.info("Track your symptoms over time to identify patterns and share with your healthcare provider.")
    
    with st.form("symptom_form"):
        symptom = st.selectbox("Symptom", ["Fever", "Headache", "Cough", "Fatigue", "Nausea", "Other"])
        severity = st.slider("Severity (1-10)", 1, 10, 5)
        notes = st.text_area("Additional notes")
        submitted = st.form_submit_button("Record Symptom")
        
        if submitted:
            save_symptom_record(st.session_state.user_id, symptom, severity, notes)
            st.success("Symptom recorded successfully!")
    
    st.markdown("---")
    st.subheader("Symptom History")
    
    history = get_symptom_history(st.session_state.user_id)
    if history:
        for symptom, severity, notes, recorded_at in history:
            with st.expander(f"{recorded_at} - {symptom} (Severity: {severity}/10)"):
                if notes:
                    st.write(f"Notes: {notes}")
                # Display different colors based on severity
                if severity >= 7:
                    st.error("High severity - consider consulting a healthcare provider")
                elif severity >= 4:
                    st.warning("Moderate severity - monitor closely")
                else:
                    st.success("Low severity")
    else:
        st.info("No symptom records yet. Start tracking your symptoms above.")

# Chat History page
elif st.session_state.user and menu == "Chat History":
    st.subheader("Chat History")
    
    history = get_chat_history(st.session_state.user_id)
    
    if history:
        for user_msg, bot_resp, timestamp in reversed(history):
            with st.expander(f"{timestamp} - {user_msg[:50]}..."):
                st.markdown(f"**You:** {user_msg}")
                st.markdown(f"**HealthMate:** {bot_resp}")
    else:
        st.info("No chat history yet")

# Footer
st.markdown("---")
st.caption("GPT-HealthMate © 2025 | Health Assistant Demo | Disclaimer: Information provided is for reference only and cannot replace professional medical advice.")