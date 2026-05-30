from st_on_hover_tabs import on_hover_tabs
import streamlit as st

st.set_page_config(layout="wide")
st.markdown('<style>' + open("C:/Users/karim/OneDrive/Desktop/Content Creation/Qurans/style.css").read() + '</style>', unsafe_allow_html=True)

with st.sidebar:
    tabs = on_hover_tabs(
        tabName=['Home', 'Quran Recitation', 'Surah Explanation', 'Stories of Prophets'],
        iconName=['home', 'headphones','arrow_right', 'history_edu'],
        styles={
            'navtab': {
                'background-color': '#111',
                'color': '#818181',
                'font-size': '12px',  # ⬇️ Reduced from 13px
                'transition': '.3s',
                'white-space': 'nowrap',
            },
            'tabStyle': {
                ':hover :hover': {
                    'color': 'red',
                    'cursor': 'pointer'
                }
            },
            'tabStyle': {
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

if tabs == 'Home':
  import streamlit as st
  import base64
  import requests
  from streamlit_lottie import st_lottie
  # Convert Local Image to Base64
  def get_base64_from_file(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()
  # Load Background Image
  image_path = "C:/Users/karim/OneDrive/Desktop/Content Creation/Qurans/image.jpg"
  image_base64 = get_base64_from_file(image_path)
  # Custom CSS for Fullscreen Background, Centered Dark Square, and Layout
  st.markdown(f"""
    <style>
        /* Fullscreen Background */
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

        /* Centered Dark Square */
        .intro-container {{
            background: rgba(0, 0, 0, 0.85); /* Dark background */
            padding: 30px;
            width: 90%;
            max-width: 600px;
            border-radius: 12px;
            box-shadow: 0px 4px 10px rgba(255, 255, 255, 0.2);
            text-align: center;
        }}

        /* White Text */
        .intro-text {{
            color: white;
            font-size: 14px;
            line-height: 1.6;
            font-family: Arial, sans-serif;
        }}

        /* Bold & Larger Title */
        .intro-title {{
            font-size: 20px;
            font-weight: bold;
            color: white;
            margin-bottom: 15px;
        }}

        /* Emoji Styling */
        .emoji {{
            font-size: 12px;
        }}
    </style>
""", unsafe_allow_html=True)

  # Function to load Lottie animation
  def load_lottie_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Return JSON data
    else:
        return None
  lottie_url = "https://lottie.host/713e9554-ee5f-41b8-a6ac-423cc61b12f6/FX5BAKwcuR.json"
  lottie_animation = load_lottie_url(lottie_url)

  # Layout: Two Columns (Text on Left, Animation on Right)
  col1, col2 = st.columns([2, 1])

  with col1:
    # Display the Centered Introduction Section
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
    # Display Lottie Animation if loaded successfully
    if lottie_animation:
        st_lottie(lottie_animation, height=450, key="animation")
    else:
        st.error("⚠️ Failed to load animation. Please check the Lottie URL.")

elif tabs == 'Quran Recitation':
    # ----------------------------- Quran 1 -----------------------------
    import streamlit as st
    import requests
    import base64

    # Convert Local Image to Base64
    def get_base64_from_file(file_path):
        try:
            with open(file_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode()
        except FileNotFoundError:
            st.error(f"Image file not found at path: {file_path}")
            return None # Handle error gracefully
        except Exception as e:
            st.error(f"Error loading image: {e}")
            return None

    # Use local image instead of Freepik URL
    image_path = "C:/Users/karim/OneDrive/Desktop/Content Creation/Qurans/image.jpg"
    image_base64 = get_base64_from_file(image_path)

    # Quran Reciters Audio Mapping with Updated Links
    RECITERS = {
        "Islam Sobhi": "https://server14.mp3quran.net/islam/Rewayat-Hafs-A-n-Assem/",
        "Raad Kurdi": "https://server6.mp3quran.net/kurdi/",
        "Hazza Al Balushi": "https://server11.mp3quran.net/hazza/",
        "Mishary Alafasi": "https://server8.mp3quran.net/afs/",
        "Maher Al Meaqli": "https://server12.mp3quran.net/maher/",
        "Abdulbasit Abdulsamad": "https://server7.mp3quran.net/basit/"
    }

    # <<< FIX 1: Updated function to use the working quran.com API
    # Function to get Quran Surahs
    def get_quran_surahs():
        try:
            # Use the new, working API endpoint from quran.com
            response = requests.get("https://api.quran.com/api/v4/chapters?language=en", timeout=25)
            
            if response.status_code == 200:
                # The list of surahs is under the 'chapters' key
                return response.json()["chapters"]
            else:
                st.error(f"Failed to fetch Surah list. Status code: {response.status_code}")
                return []
        except requests.exceptions.RequestException as e:
            # Handle connection errors, timeouts, etc.
            st.error(f"Error connecting to Quran API: {e}")
            return []
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            return []

    # Custom CSS for Dark Selectboxes & Styled YouTube Section
    # Check if image was loaded successfully before trying to use it
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
    
    # Continue with the rest of the CSS
    st.markdown(f"""
        <style>
            /* Button Styling */
            .stButton > button {{
                background-color: rgba(0, 0, 0, 0.9) !important; /* Black background */
                color: white !important; /* White text */
                border-radius: 10px !important; /* Keep button corners rounded */
                padding: 12px 20px !important; /* Adjust button size */
                border: 1px solid white !important; /* Optional: White border */
                font-weight: bold !important;
            }}

            /* Button Hover Effect */
            .stButton > button:hover {{
                background-color: rgba(50, 50, 50, 0.9) !important; /* Slightly lighter black on hover */
            }}

            .stSelectbox label {{
                font-weight: bold;
                color: white !important;
                font-size: 18px;
            }}
            /* Centered Subheaders */
            .left-subheader {{
                text-align:left;
                font-size: 19px;
                font-weight: bold;
                color: white;
                margin-bottom: 10px;
            }}
            /* Expander Styling */
            .stExpander {{
                background-color: rgba(0, 0, 0, 0.9) !important; /* Change background to black */
                color: white !important; /* Ensure text inside expander is white */
                border-radius: 10px !important; /* Keep border-radius as it is */
                padding: 10px !important;
                border: 1px solid white !important; /* Optional: If you want a visible white border *
            }}
            .stExpanderHeader {{
                font-size: 18px !important;
                font-weight: bold !important;
            }}
            /* Expander Content Styling */
            .expander-content {{
                font-size: 14px;
                color: white !important;
                padding: 10px;
            }}
            /* Styled Video Containers */
            /* Centered Video */
            .video-container {{
                text-align: center;
                margin-top: 10px;
            }}
        </style>
    """, unsafe_allow_html=True)

    # Streamlit App Layout
    st.markdown("<div class='left-subheader'>Listen to the beautiful recitation of the Holy Quran by your favorite Qaris.</div>", unsafe_allow_html=True)

    # Fetch Surahs
    surahs = get_quran_surahs()
    
    # <<< FIX 2: Updated keys to match the new API's response
    # Use 'name_simple' for the name and 'id' for the number
    surah_options = {surah['name_simple']: surah['id'] for surah in surahs}

    if surah_options:
        # Select Surah & Reciter (Styled Selectboxes)
        col1, col2 = st.columns(2)

        with col1:
            surah_name = st.selectbox("Select Surah", list(surah_options.keys()), key="surah_select")
        with col2:
            reciter_name = st.selectbox("Select Reciter", list(RECITERS.keys()), key="reciter_select")

        surah_number = surah_options[surah_name]
        reciter_url_base = RECITERS[reciter_name]

        # Construct Audio URL
        surah_number_str = str(surah_number).zfill(3)  # Format number as 3 digits
        audio_url = f"{reciter_url_base}{surah_number_str}.mp3"

        # Display Audio Player
        st.audio(audio_url, format="audio/mp3", start_time=0)

    else:
        # This error message will now show if the API fails
        st.error("Failed to load Surah list. Please check your internet connection and try again later.")

    # Section: Calm and Relax the Soul
    st.markdown("<div class='left-subheader'>Enjoy peaceful Quran recitations curated by </div>", unsafe_allow_html=True)

    # Expander for Abdullah Mosaad
    with st.expander("🎙️ Abdullah Mosaad"):
        st.markdown("<div class='expander-content'>Abdullah Mosaad is known for his deeply emotional and heart-touching Quran recitations. His voice brings serenity and peace to listeners worldwide.</div>", unsafe_allow_html=True)
        
        # Embed YouTube Video for Abdullah Mosaad
        st.markdown("""
            <div class="video-container">
                <iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/inBCxCUW_vA?si=I6Kty1oKGe-HnQX3" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>            
            </div>
        """, unsafe_allow_html=True)

    # Expander for Salim Bahanan
    with st.expander("🎙️ Abdulrahman Almajed"):
        st.markdown("<div class='expander-content'>Abdulrahman Almajed's recitation style is known for its clarity, precision, and soothing tone, making it a perfect choice for deep spiritual reflection.</div>", unsafe_allow_html=True)
        
        # Embed YouTube Video for Salim Bahanan
        st.markdown("""
            <div class="video-container">
                <iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/l3ZuhJOatRM?si=b-_LpZA2ddbNJ9_6" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
            </div>
        """, unsafe_allow_html=True)

elif tabs == 'Surah Explanation':
    # ----------------------------- Quran 2 -----------------------------
    import streamlit as st
    import requests
    import openai
    from openai import OpenAI
    import edge_tts
    import asyncio
    import base64

    client = OpenAI()

    # Convert Local Image to Base64
    def get_base64_from_file(file_path):
        with open(file_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()

    # Use local image instead of Freepik URL
    image_path = "C:/Users/karim/OneDrive/Desktop/Content Creation/Qurans/image.jpg"
    image_base64 = get_base64_from_file(image_path)

    # Function to get Quran Surahs
    def get_quran_surahs():
        try:
            response = requests.get("http://api.alquran.cloud/v1/surah", timeout=5)
            if response.status_code == 200:
                return response.json()["data"]
            else:
                return []
        except:
            return []

    # Function to get brief English meaning using GPT API
    def get_surah_brief_description(surah_name):
        prompt = f"Provide a very brief and simple explanation of the Surah {surah_name} from the Quran in English. Keep it concise."
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message.content

    def get_surah_arabic_explanation(surah_name):
        prompt = f"Provide a brief and clear explanation of Surah {surah_name} from the Quran in Arabic. The explanation should be concise and easy to understand. Limit to 3-4 sentences."
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=300
        )
        return response.choices[0].message.content

    # Custom CSS (Only modifying the selectbox title)
    st.markdown(f"""
        <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{image_base64}");
                background-size: cover;
                background-position: center;
                font-family: Arial, sans-serif;
            }}
            .stSelectbox label {{
                font-weight: bold;
                color: white !important;
                font-size: 18px;
            }}
            .stNumberInput label {{
                font-weight: bold;
                color: white !important;
                font-size: 18px;
            }}
        </style>
    """, unsafe_allow_html=True)

    # Function to generate Arabic audio explanation using Edge TTS
    async def generate_arabic_audio(text, file_path):
        try:
            tts = edge_tts.Communicate(text, voice="ar-AE-FatimaNeural")
            await tts.save(file_path)
            return file_path
        except edge_tts.exceptions.NoAudioReceived:
            return None

    # Section: Live Meaning of Each Surah
    st.markdown("<div style='text-align:left; color:white; font-size:30px; font-weight:bold;'>📖 Live Meaning of Each Surah</div>", unsafe_allow_html=True)

    surahs = get_quran_surahs()
    surah_options = {surah['englishName']: surah['number'] for surah in surahs}

    if surah_options:
        selected_surah = st.selectbox("Select Surah", list(surah_options.keys()), key="surah_dropdown")
        surah_number = surah_options[selected_surah]
        
        # Layout: Two Columns for better spacing
        col1, col3, col2 = st.columns([2,1,1])
        
        with col1:
            # Display Brief English Description
            if st.button("📜 Show Brief Surah Description"):
                brief_description = get_surah_brief_description(selected_surah)
                st.markdown(f"<div style='background-color: rgba(255, 255, 255, 0.9); padding: 1rem; border-left: 5px solid #17a2b8; border-radius: 8px;'><b>{selected_surah} Summary:</b><br>{brief_description}</div>", unsafe_allow_html=True)

        st.write("")
        st.write("")
        st.markdown("<div style='text-align:left; color:white; font-size:30px; font-weight:bold;'>🔉Live Arabic Explanation of Each Surah</div>", unsafe_allow_html=True)
        # Arabic Explanation Button Logic (Keeping your original flow)
        col11, col33, col22, col44 = st.columns([2,1,2,3])
        with col11:
            surahss = st.selectbox("Select Surah", list(surah_options.keys()), key='arabic_surah_dropdown')
        if st.button("🎙️ Explain in Arabic"):
            with st.spinner("Generating Arabic audio, please wait..."):
                arabic_text = get_surah_arabic_explanation(surahss)
                audio_file = f"{selected_surah}_arabic_explanation.mp3"
                if asyncio.run(generate_arabic_audio(arabic_text, audio_file)):
                    st.audio(audio_file, format="audio/mp3")
                else:
                    st.error("❌ Failed to generate Arabic audio. Please try again.")
    else:
        st.error("Failed to load Surah list. Please try again later.")

elif tabs == 'Stories of Prophets':
    # ----------------------------- Quran 3 -----------------------------
    import streamlit as st
    import streamlit.components.v1 as components
    import base64

    # Convert Local Image to Base64
    def get_base64_from_file(file_path):
        with open(file_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()

    # Use local image instead of Freepik URL
    image_path = "C:/Users/karim/OneDrive/Desktop/Content Creation/Qurans/background.jpg" 
    image_base64 = get_base64_from_file(image_path)

    custom_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Prophets of Islam</title>
        <style>
            /* Fullscreen Background */
            body {{
                background: url("data:image/jpeg;base64,{image_base64}") no-repeat center center fixed;
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
            /* Container for buttons */
            .container {{
                display: flex;
                justify-content: center;
                align-items: center;
                flex-wrap: wrap;
                margin-top: 20px;
            }}
            /* Circular buttons */
            .circle-btn {{
                width: 150px;
                height: 130px;
                background-color: rgba(0, 0, 0, 0.7);
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 50%;
                text-align: center;
                line-height: 120px;
                margin: 15px;
                cursor: pointer;
                transition: transform 0.3s ease-in-out, background 0.3s;
            }}
            .circle-btn:hover {{
                background-color: rgba(255, 255, 255, 0.3);
                transform: scale(1.1);
            }}
            /* Hidden story content */
            .story {{
                display: none;
                background: rgba(0, 0, 0, 0.85);
                padding: 20px;
                border-radius: 10px;
                margin-top: 20px;
                width: 70%;
            }}
            /* Visible story */
            .visible {{
                display: block !important;
            }}
        </style>
    </head>
    <body>

        <div class="container">
            <div class="circle-btn" onclick="showStory(1)">Nuh A.S.</div>
            <div class="circle-btn" onclick="showStory(2)">Ibrahim A.S.</div>
            <div class="circle-btn" onclick="showStory(3)">Musa A.S.</div>
            <div class="circle-btn" onclick="showStory(4)">Isa A.S.</div>
            <div class="circle-btn" onclick="showStory(5)">Muhammad A.S.</div>
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

# elif tabs == 'Dua Collection':
#     # ----------------------------- Quran 4 -----------------------------
#     import streamlit as st
#     import streamlit.components.v1 as components
#     import base64

#     # Convert Local Image to Base64
#     def get_base64_from_file(file_path):
#         with open(file_path, "rb") as image_file:
#             return base64.b64encode(image_file.read()).decode()

#     # Use local image instead of Freepik URL
#     image_path = "C:/Users/karim/OneDrive/Desktop/Qurans/background.jpg"
#     image_base64 = get_base64_from_file(image_path)

#     custom_html = f"""
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">

#         <style>
#             /* Fullscreen Background */
#             body {{
#                 background: url("data:image/jpeg;base64,{image_base64}") no-repeat center center fixed;
#                 background-size: cover;
#                 background-attachment: fixed;
#                 font-family: Arial, sans-serif;
#                 text-align: center;
#                 margin: 0;
#                 padding: 0;
#                 height: 100vh;
#                 display: flex;
#                 flex-direction: column;
#                 justify-content: center;
#                 align-items: center;
#             }}


#             /* Button Container */
#             .container {{
#                 display: flex;
#                 flex-direction: column;
#                 align-items: center;
#                 width: 100%;
#                 gap: 15px;
#                 margin-top: 40px;
#             }}

#             /* Circle Buttons */
#             .circle-btn {{
#                 width: 200px;
#                 height: 60px;
#                 background: rgba(0, 0, 0, 0.8);
#                 color: white;
#                 font-size: 18px;
#                 font-weight: bold;
#                 text-align: center;
#                 cursor: pointer;
#                 display: flex;
#                 justify-content: center;
#                 align-items: center;
#                 border-radius: 30px;
#                 border: 2px solid white;
#                 transition: transform 0.3s ease-in-out, background 0.3s;
#             }}

#             /* Hover Effect */
#             .circle-btn:hover {{
#                 background: rgba(255, 255, 255, 0.3);
#                 transform: scale(1.05);
#                 color: black;
#             }}

#             /* Dua Content Container */
#             .dua-container {{
#                 background: rgba(0, 0, 0, 0.85);
#                 color: white;
#                 padding: 20px;
#                 border-radius: 12px;
#                 width: 80%;
#                 text-align: center;
#                 margin-top: 20px;
#                 display: none;
#                 box-shadow: 0px 4px 15px rgba(255, 255, 255, 0.3);
#                 animation: fadeIn 0.5s ease-in-out;
#             }}

#             /* Fade-in Animation */
#             @keyframes fadeIn {{
#                 0% {{ opacity: 0; transform: scale(0.95); }}
#                 100% {{ opacity: 1; transform: scale(1); }}
#             }}

#         </style>

#         <script>
#             function showDua(id) {{
#                 // Hide all other dua containers
#                 document.querySelectorAll('.dua-container').forEach(div => div.style.display = 'none');
                
#                 // Show the selected one
#                 document.getElementById(id).style.display = "block";
#             }}
#         </script>
#     </head>
#     <body>



#         <div class="container">
#             <div class="circle-btn" onclick="showDua('dua-kumayl')">Duʿā Kumayl</div>
#             <div class="circle-btn" onclick="showDua('dua-jawshan')">Duʿā al-Jawshan</div>
#             <div class="circle-btn" onclick="showDua('dua-hamza')">Duʿā Abī Ḥamza</div>
#         </div>

#         <div id='dua-kumayl' class='dua-container'>
#             <h2>Duʿā Kumayl</h2>
#             <p><strong>About:</strong> A heartfelt plea for God's mercy, seeking forgiveness, and expressing trust in His compassion.</p>
#             <p><em>"O Allah, You are the One whose mercy I seek, the One whose kindness I rely on. Forgive my mistakes and guide me back to You."</em></p>
#             <iframe width='560' height='315' src='https://www.youtube.com/embed/Za2PlRwn8TY' frameborder='0' allowfullscreen></iframe>
#         </div>

#         <div id='dua-jawshan' class='dua-container'>
#             <h2>Duʿā al-Jawshan al-Kabīr</h2>
#             <p><strong>About:</strong> A supplication invoking 1000 names of God, asking for divine protection and deliverance from harm.</p>
#             <p><em>"O You who respond to every cry of the distressed, protect me from harm and guide me by Your mercy."</em></p>
#             <iframe width='560' height='315' src='https://www.youtube.com/embed/aHyeh9-pE-Q' frameborder='0' allowfullscreen></iframe>
#         </div>

#         <div id='dua-hamza' class='dua-container'>
#             <h2>Duʿā Abī Ḥamza al-Thumālī</h2>
#             <p><strong>About:</strong> A supplication of humility, repentance, and longing for closeness to God.</p>
#             <p><em>"O Allah, if You turn me away, who else will have mercy on me? And if You refuse me, where else can I find shelter but with You?"</em></p>
#             <iframe width='560' height='315' src='https://www.youtube.com/embed/GRWjuqrvzbw' frameborder='0' allowfullscreen></iframe>
#         </div>

#     </body>
#     </html>
#     """

#     components.html(custom_html, height=800)
