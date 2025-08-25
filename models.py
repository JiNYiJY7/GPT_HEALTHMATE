import random
from datetime import datetime

def get_health_advice(symptom):
    """
    根据症状提供专业的健康建议
    """
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
    
    # 默认回复
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

def ask_healthmate(user_input):
    """
    根据用户输入提供健康建议
    """
    # 急症关键词检测
    emergency_keywords = ['chest pain', 'difficulty breathing', 'fainting', 'severe bleeding', 'stroke', 'severe headache']
    if any(keyword in user_input.lower() for keyword in emergency_keywords):
        return "⚠️ Possible emergency detected! Please seek immediate medical attention. This assistant cannot handle emergencies, please call emergency services or go to the nearest hospital."
    
    # 症状关键词映射
    symptom_keywords = {
        'fever': ['fever', 'temperature', 'hot', 'sweating'],
        'headache': ['headache', 'head pain', 'migraine'],
        'cough': ['cough', 'coughing', 'phlegm'],
        'sore throat': ['sore throat', 'throat pain', 'swallowing pain'],
        'fatigue': ['tired', 'fatigue', 'exhausted', 'low energy'],
        'nausea': ['nausea', 'sick', 'vomit', 'queasy']
    }
    
    # 检测症状关键词
    detected_symptom = None
    for symptom, keywords in symptom_keywords.items():
        if any(keyword in user_input.lower() for keyword in keywords):
            detected_symptom = symptom
            break
    
    # 获取建议
    if detected_symptom:
        advice = get_health_advice(detected_symptom)
        
        # 构建响应
        response = f"**About {detected_symptom}:**\n\n{advice['description']}\n\n"
        response += "**Recommended actions:**\n"
        for i, item in enumerate(advice['advice'], 1):
            response += f"{i}. {item}\n"
        
        response += f"\n**When to see a doctor:**\n{advice['when_to_see_doctor']}\n\n"
    else:
        # 通用建议
        response = "Based on your description, here are some general health recommendations:\n\n"
        response += "1. Rest and allow your body time to recover\n"
        response += "2. Stay hydrated by drinking plenty of fluids\n"
        response += "3. Eat a balanced diet with plenty of fruits and vegetables\n"
        response += "4. Monitor your symptoms and note any changes\n"
        response += "5. Consider over-the-counter remedies if appropriate for your symptoms\n\n"
        response += "If your symptoms persist or worsen, it's important to consult with a healthcare professional for proper diagnosis and treatment.\n\n"
    
    # 添加免责声明
    response += "---\n"
    response += "⚠️ **Disclaimer:** This information is for educational purposes only and is not a substitute for professional medical advice. Always consult with a healthcare provider for proper diagnosis and treatment."
    
    return response

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
    
    # 根据日期选择小贴士，确保每天相同
    day_of_year = datetime.now().timetuple().tm_yday
    return tips[day_of_year % len(tips)]