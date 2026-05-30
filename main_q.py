import streamlit as st
import base64
import requests
import asyncio
from streamlit_lottie import st_lottie
import streamlit.components.v1 as components
from st_on_hover_tabs import on_hover_tabs
import openai
from openai import OpenAI
import edge_tts

# -----------------------------
# Configuration & Global Setup
# -----------------------------
st.set_page_config(layout="wide")

# Load CSS via Relative Path
try:
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    st.error("⚠️ style.css not found. Please ensure it is uploaded to your GitHub repository.")

# Centralized Function to Convert Image to Base64
def get_base64_from_file(file_path):
    try:
        with open(file_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        st.error(f"⚠️ Image file not found: {file_path}. Ensure it is uploaded to GitHub.")
        return None
    except Exception as e:
        st.error(f"⚠️ Error loading image: {e}")
        return None

# Load Images using Relative Paths
image_base64 = get_base64_from_file("image.jpg")
bg_image_base64 = get_base64_from_file("background.jpg")

# Initialize OpenAI via Streamlit Secrets
# You will need to add OPENAI_API_KEY in your Streamlit Cloud Advanced Settings
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    client = None
    st.warning("⚠️ OpenAI API Key not found in st.secrets. AI explanations will not work.")

# -----------------------------
# Sidebar Navigation
# -----------------------------
with st.sidebar:
    tabs = on_hover_tabs(
        tabName=['Home', 'Quran Recitation', 'Surah Explanation', 'Stories of Prophets'],
        iconName=['home', 'headphones','arrow_right', 'history_edu'],
        styles={
            'navtab': {
                'background-color': '#111',
                'color': '#818181',
                'font-size': '12px',
                'transition': '.3s',
                'white-space': 'nowrap',
            },
            'tabStyle': {
                ':hover :hover': {
                    'color': 'red',
                    'cursor': 'pointer'
                },
                'list-style-type': 'none',
                'margin-bottom': '30px',
                'padding-left': '30px'
            },
            'iconStyle': {
                'position': 'fixed',
                'left': '7.5px',
                'text-align': 'left'
            },
        },
        key="1"
    )

# -----------------------------
# Tab 1: Home
# -----------------------------
if tabs == 'Home':
    if image_base64:
        st.markdown(f"""
            <style>
                .stApp {{
                    background-image: url("data:image/jpeg;base64,{image_base64}");
                    background-size: cover;
                    background-position: center;
                    background-attachment: fixed;
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }}
                .intro-container {{
                    background: rgba(0, 0, 0, 0.85); 
                    padding: 30px;
                    width: 90%;
                    max-width: 600px;
                    border-radius: 12px;
                    box-shadow: 0px 4px 10px rgba(255, 255, 255, 0.2);
                    text-align: center;
                }}
                .intro-text {{
                    color: white;
                    font-size: 14px;
                    line-height: 1.6;
                    font-family: Arial, sans-serif;
                }}
                .intro-title {{
                    font-size: 20px;
                    font-weight: bold;
                    color: white;
                    margin-bottom: 15px;
                }}
                .emoji {{
                    font-size: 12px;
                }}
            </style>
        """, unsafe_allow_html=True)

    def load_lottie_url(url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None
        
    lottie_url = "https://lottie.host/713e9554-ee5f-41b8-a6ac-423cc61b12f6/FX5BAKwcuR.json"
    lottie_animation = load_lottie_url(lottie_url)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
            <div class="intro-container">
                <div class="intro-title">Welcome to the Quran & Islam Explorer App</div>
                <div class="intro-text">
                    I poured my heart into every single line of code in this app. It’s not just a blend of customized CSS styles combined with AI-powered features—it’s also a journey of learning and faith for me as a Muslim. 
                    <br><br>
                    With every update, I find myself deepening my understanding of the Quran and Islam.
                    <b>What You’ll Find in This App:</b><br>
                    <span class="emoji">📖</span> Curated Quran Recitations – Handpicked recitations from my favorite Qaris.<br>
                    <span class="emoji">🧠</span> AI-Powered Explanations – Get an AI-generated breakdown of each Surah, along with live Arabic audio explanations.<br>
                    <span class="emoji">🌟</span> Stories of Our Greatest Prophets – A section dedicated to learning about our five highest prophets.<br>
                    <br><br>
                    <b>Enough explaining—start exploring! JazakumAllahu Khairan.</b>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        if lottie_animation:
            st_lottie(lottie_animation, height=450, key="animation")
        else:
            st.error("⚠️ Failed to load animation. Please check the Lottie URL.")

# -----------------------------
# Tab 2: Quran Recitation
# -----------------------------
elif tabs == 'Quran Recitation':
    RECITERS = {
        "Islam Sobhi": "https://server14.mp3quran.net/islam/Rewayat-Hafs-A-n-Assem/",
        "Raad Kurdi": "https://server6.mp3quran.net/kurdi/",
        "Hazza Al Balushi": "https://server11.mp3quran.net/hazza/",
        "Mishary Alafasi": "https://server8.mp3quran.net/afs/",
        "Maher Al Meaqli": "https://server12.mp3quran.net/maher/",
        "Abdulbasit Abdulsamad": "https://server7.mp3quran.net/basit/"
    }

    def get_quran_surahs():
        try:
            response = requests.get("https://api.quran.com/api/v4/chapters?language=en", timeout=25)
            if response.status_code == 200:
                return response.json()["chapters"]
            else:
                st.error(f"Failed to fetch Surah list. Status code: {response.status_code}")
                return []
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to Quran API: {e}")
            return []

    if image_base64:
        st.markdown(f"""
            <style>
                .stApp {{
                    background-image: url("data:image/jpeg;base64,{image_base64}");
                    background-size: cover;
                    background-position: center;
                    font-family: Arial, sans-serif;
                }}
            </style>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <style>
            .stButton > button { background-color: rgba(0, 0, 0, 0.9) !important; color: white !important; border-radius: 10px !important; padding: 12px 20px !important; border: 1px solid white !important; font-weight: bold !important; }
            .stButton > button:hover { background-color: rgba(50, 50, 50, 0.9) !important; }
            .stSelectbox label { font-weight: bold; color: white !important; font-size: 18px; }
            .left-subheader { text-align:left; font-size: 19px; font-weight: bold; color: white; margin-bottom: 10px; }
            .stExpander { background-color: rgba(0, 0, 0, 0.9) !important; color: white !important; border-radius: 10px !important; padding: 10px !important; border: 1px solid white !important; }
            .stExpanderHeader { font-size: 18px !important; font-weight: bold !important; }
            .expander-content { font-size: 14px; color: white !important; padding: 10px; }
            .video-container { text-align: center; margin-top: 10px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='left-subheader'>Listen to the beautiful recitation of the Holy Quran by your favorite Qaris.</div>", unsafe_allow_html=True)

    surahs = get_quran_surahs()
    surah_options = {surah['name_simple']: surah['id'] for surah in surahs} if surahs else {}

    if surah_options:
        col1, col2 = st.columns(2)
        with col1:
            surah_name = st.selectbox("Select Surah", list(surah_options.keys()), key="surah_select")
        with col2:
            reciter_name = st.selectbox("Select Reciter", list(RECITERS.keys()), key="reciter_select")

        surah_number = surah_options[surah_name]
        reciter_url_base = RECITERS[reciter_name]
        surah_number_str = str(surah_number).zfill(3)
        audio_url = f"{reciter_url_base}{surah_number_str}.mp3"
        st.audio(audio_url, format="audio/mp3", start_time=0)
    else:
        st.error("Failed to load Surah list. Please check your internet connection and try again later.")

    st.markdown("<div class='left-subheader'>Enjoy peaceful Quran recitations curated by </div>", unsafe_allow_html=True)

    with st.expander("🎙️ Abdullah Mosaad"):
        st.markdown("<div class='expander-content'>Abdullah Mosaad is known for his deeply emotional and heart-touching Quran recitations. His voice brings serenity and peace to listeners worldwide.</div>", unsafe_allow_html=True)
        st.markdown("""
            <div class="video-container">
                <iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/inBCxCUW_vA?si=I6Kty1oKGe-HnQX3" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>            
            </div>
        """, unsafe_allow_html=True)

    with st.expander("🎙️ Abdulrahman Almajed"):
        st.markdown("<div class='expander-content'>Abdulrahman Almajed's recitation style is known for its clarity, precision, and soothing tone, making it a perfect choice for deep spiritual reflection.</div>", unsafe_allow_html=True)
        st.markdown("""
            <div class="video-container">
                <iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/l3ZuhJOatRM?si=b-_LpZA2ddbNJ9_6" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
            </div>
        """, unsafe_allow_html=True)

# -----------------------------
# Tab 3: Surah Explanation
# -----------------------------
elif tabs == 'Surah Explanation':
    def get_quran_surahs_cloud():
        try:
            response = requests.get("http://api.alquran.cloud/v1/surah", timeout=5)
            if response.status_code == 200:
                return response.json()["data"]
            return []
        except:
            return []

    def get_surah_brief_description(surah_name):
        if not client: return "OpenAI API Key not configured."
        prompt = f"Provide a very brief and simple explanation of the Surah {surah_name} from the Quran in English. Keep it concise."
        response = client.chat.completions.create(model="gpt-4", messages=[{"role": "system", "content": prompt}], max_tokens=150)
        return response.choices[0].message.content

    def get_surah_arabic_explanation(surah_name):
        if not client: return "OpenAI API Key not configured."
        prompt = f"Provide a brief and clear explanation of Surah {surah_name} from the Quran in Arabic. The explanation should be concise and easy to understand. Limit to 3-4 sentences."
        response = client.chat.completions.create(model="gpt-4", messages=[{"role": "system", "content": prompt}], max_tokens=300)
        return response.choices[0].message.content

    if image_base64:
        st.markdown(f"""
            <style>
                .stApp {{ background-image: url("data:image/jpeg;base64,{image_base64}"); background-size: cover; background-position: center; font-family: Arial, sans-serif; }}
                .stSelectbox label {{ font-weight: bold; color: white !important; font-size: 18px; }}
                .stNumberInput label {{ font-weight: bold; color: white !important; font-size: 18px; }}
            </style>
        """, unsafe_allow_html=True)

    async def generate_arabic_audio(text, file_path):
        try:
            tts = edge_tts.Communicate(text, voice="ar-AE-FatimaNeural")
            await tts.save(file_path)
            return file_path
        except edge_tts.exceptions.NoAudioReceived:
            return None

    st.markdown("<div style='text-align:left; color:white; font-size:30px; font-weight:bold;'>📖 Live Meaning of Each Surah</div>", unsafe_allow_html=True)

    surahs = get_quran_surahs_cloud()
    surah_options = {surah['englishName']: surah['number'] for surah in surahs} if surahs else {}

    if surah_options:
        selected_surah = st.selectbox("Select Surah", list(surah_options.keys()), key="surah_dropdown")
        
        col1, col3, col2 = st.columns([2,1,1])
        with col1:
            if st.button("📜 Show Brief Surah Description"):
                brief_description = get_surah_brief_description(selected_surah)
                st.markdown(f"<div style='background-color: rgba(255, 255, 255, 0.9); padding: 1rem; border-left: 5px solid #17a2b8; border-radius: 8px;'><b>{selected_surah} Summary:</b><br>{brief_description}</div>", unsafe_allow_html=True)

        st.write("")
        st.write("")
        st.markdown("<div style='text-align:left; color:white; font-size:30px; font-weight:bold;'>🔉Live Arabic Explanation of Each Surah</div>", unsafe_allow_html=True)
        
        col11, col33, col22, col44 = st.columns([2,1,2,3])
        with col11:
            surahss = st.selectbox("Select Surah for Audio", list(surah_options.keys()), key='arabic_surah_dropdown')
        if st.button("🎙️ Explain in Arabic"):
            with st.spinner("Generating Arabic audio, please wait..."):
                arabic_text = get_surah_arabic_explanation(surahss)
                audio_file = f"{surahss}_arabic_explanation.mp3"
                if asyncio.run(generate_arabic_audio(arabic_text, audio_file)):
                    st.audio(audio_file, format="audio/mp3")
                else:
                    st.error("❌ Failed to generate Arabic audio. Please try again.")
    else:
        st.error("Failed to load Surah list. Please try again later.")

# -----------------------------
# Tab 4: Stories of Prophets
# -----------------------------
elif tabs == 'Stories of Prophets':
    if bg_image_base64:
        custom_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Prophets of Islam</title>
            <style>
                body {{
                    background: url("data:image/jpeg;base64,{bg_image_base64}") no-repeat center center fixed;
                    background-size: cover;
                    font-family: Arial, sans-serif;
                    color: white;
                    text-align: center;
                    margin: 0;
                    padding: 0;
                    height: 100vh;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                }}
                .container {{ display: flex; justify-content: center; align-items: center; flex-wrap: wrap; margin-top: 20px; }}
                .circle-btn {{
                    width: 150px; height: 130px; background-color: rgba(0, 0, 0, 0.7);
                    color: white; font-size: 18px; font-weight: bold; border-radius: 50%;
                    text-align: center; line-height: 120px; margin: 15px; cursor: pointer;
                    transition: transform 0.3s ease-in-out, background 0.3s;
                }}
                .circle-btn:hover {{ background-color: rgba(255, 255, 255, 0.3); transform: scale(1.1); }}
                .story {{ display: none; background: rgba(0, 0, 0, 0.85); padding: 20px; border-radius: 10px; margin-top: 20px; width: 70%; }}
                .visible {{ display: block !important; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="circle-btn" onclick="showStory(1)">Nuh A.S.</div>
                <div class="circle-btn" onclick="showStory(2)">Ibrahim A.S.</div>
                <div class="circle-btn" onclick="showStory(3)">Musa A.S.</div>
                <div class="circle-btn" onclick="showStory(4)">Isa A.S.</div>
                <div class="circle-btn" onclick="showStory(5)">Muhammad ﷺ</div>
            </div>
            
            <div id="story1" class="story">
                <h2>Prophet Nuh (Noah) – The Ark of Salvation</h2>
                <p>For 950 years, Prophet Nuh preached to his people, warning them of Allah’s command. They mocked him, but he remained patient.</p>
                <p>Allah commanded him to build a great ark, and when the flood came, only Nuh and the believers were saved. The ark rested on Mount Judi, marking a new beginning for humanity.</p>
            </div>
            <div id="story2" class="story">
                <h2>Prophet Ibrahim (Abraham) – The Friend of Allah</h2>
                <p>Born in a land of idol worship, Ibrahim questioned his people: <b>"Why worship these statues? They cannot hear or help us!"</b></p>
                <p>To prove idol worship false, he destroyed the idols. King Nimrod ordered him to be burned, but Allah made the fire cool for him.</p>
                <p>Later, he built the Kaaba with his son Ismail and was tested to sacrifice him. Allah replaced Ismail with a ram, proving Ibrahim’s unwavering faith.</p>
            </div>
            <div id="story3" class="story">
                <h2>Prophet Musa (Moses) – The Splitter of the Sea</h2>
                <p>Prophet Musa was placed in a basket as a baby and found by Pharaoh’s wife. He later fled Egypt but returned when Allah spoke to him from a burning bush.</p>
                <p>Pharaoh refused to believe, even after seeing miracles. When the Israelites escaped, Musa struck his staff, and the Red Sea split, saving them and drowning Pharaoh’s army.</p>
            </div>
            <div id="story4" class="story">
                <h2>Prophet Isa (Jesus) – The Spirit of Allah</h2>
                <p>Born to Maryam (Mary) without a father, Prophet Isa spoke as a baby: <b>"I am a servant of Allah! He gave me a book and made me a prophet!"</b></p>
                <p>He healed the sick, gave sight to the blind, and brought the dead back to life—all by Allah’s will. But people plotted against him.</p>
                <p>Allah raised Isa to the heavens, and he will return before the Day of Judgment.</p>
            </div>
            <div id="story5" class="story">
                <h2>Prophet Muhammad ﷺ – The Seal of Prophets</h2>
                <p>Born in Mecca, Muhammad was known as *Al-Amin (The Trustworthy)*. At age 40, Angel Jibreel came to him and said, <b>"Read!"</b></p>
                <p>Thus began the revelation of the Qur’an. He faced persecution, migrated to Medina, and later conquered Mecca peacefully.</p>
                <p>One night, he ascended to the heavens, met previous prophets, and was given the gift of Salah (prayer). Through patience and wisdom, Islam spread worldwide.</p>
            </div>
            <script>
                function showStory(num) {{
                    document.querySelectorAll('.story').forEach(story => story.classList.remove('visible'));
                    document.getElementById('story' + num).classList.add('visible');
                }}
            </script>
        </body>
        </html>
        """
        components.html(custom_html, height=800)
    else:
        st.error("Background image failed to load. Please verify your files.")
