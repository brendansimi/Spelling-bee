import streamlit as st
import io
import random
import time

# --- SAFETY CHECK FOR AUDIO ---
# This prevents the app from crashing if gTTS isn't installed yet
try:
    from gtts import gTTS
    has_audio = True
except ImportError:
    has_audio = False

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="3rd Grade Spelling Bee", page_icon="🐝")

st.markdown("""
    <style>
    .big-font { font-size:30px !important; color: #E07A5F; font-weight: bold; }
    .def-font { font-size:20px !important; color: #3D405B; }
    .stButton>button { background-color: #81B29A; color: white; font-size: 18px; border-radius: 10px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- WORD LIST ---
original_words = [
    {"word": "unicorn", "type": "noun", "def": "An imaginary animal with a horse body and single horn."},
    {"word": "faraway", "type": "adjective", "def": "Distant in space."},
    {"word": "heater", "type": "noun", "def": "A device that gives off warmth."},
    {"word": "pirates", "type": "plural noun", "def": "Robbers on the high seas."},
    {"word": "understand", "type": "verb", "def": "To comprehend."},
    {"word": "wooden", "type": "adjective", "def": "Lacking in ease, grace, or charm; awkward or stiff."},
    {"word": "leaning", "type": "verb", "def": "Casting one's weight by inclining to one side."},
    {"word": "breakfast", "type": "noun", "def": "The first meal of the day."},
    {"word": "window", "type": "noun", "def": "An opening in a wall that lets light and air in."},
    {"word": "acrobat", "type": "noun", "def": "One who performs gymnastic feats."},
    {"word": "message", "type": "noun", "def": "A written or oral communication sent to someone."},
    {"word": "chocolate", "type": "noun", "def": "A candy made from roasted cacao beans."},
    {"word": "forepaw", "type": "noun", "def": "The foot of a quadruped on a front leg."},
    {"word": "elephant", "type": "noun", "def": "A large mammal with a trunk and tusks."},
    {"word": "hedgehog", "type": "noun", "def": "A small mammal with spines that rolls into a ball."},
    {"word": "recipe", "type": "noun", "def": "A list of ingredients and instructions for making food."},
    {"word": "garbage", "type": "noun", "def": "Trash of any kind."},
    {"word": "surprise", "type": "noun", "def": "Something unexpected or astonishing."},
    {"word": "mermaid", "type": "noun", "def": "Imaginary sea creature: half woman, half fish."},
    {"word": "bombarded", "type": "verb", "def": "Attacked vigorously or persistently."},
    {"word": "disability", "type": "noun", "def": "A physical or mental condition that incapacitates."},
    {"word": "incredible", "type": "adjective", "def": "Hard to believe real or true."},
    {"word": "leather", "type": "noun", "def": "Animal skin prepared for use."},
    {"word": "countess", "type": "noun", "def": "A woman with the rank of earl."},
    {"word": "nervous", "type": "adjective", "def": "Fearful of what may be coming."},
    {"word": "peppercorn", "type": "noun", "def": "A dried berry of the Piper plant."},
    {"word": "cartwheel", "type": "noun", "def": "A sideways handspring."},
    {"word": "raise", "type": "verb", "def": "To lift higher."},
    {"word": "weather", "type": "noun", "def": "Atmospheric conditions (rain, sun, wind)."},
    {"word": "zooming", "type": "verb", "def": "Moving with a loud low hum or buzz."},
    {"word": "attacked", "type": "verb", "def": "Began to injure, damage, or eat."},
    {"word": "turnout", "type": "noun", "def": "A gathering of people for a special purpose."},
    {"word": "eaten", "type": "adjective", "def": "Taken in through the mouth as food."},
    {"word": "streetlights", "type": "plural noun", "def": "Electric lamps along a public road."},
    {"word": "journey", "type": "noun", "def": "An act of traveling from one place to another."},
    {"word": "courtyard", "type": "noun", "def": "An enclosure attached to a house or castle."},
    {"word": "shouting", "type": "noun", "def": "Speaking in a loud voice."},
    {"word": "asleep", "type": "adjective", "def": "Lacking sensation or feeling; numb."},
    {"word": "curious", "type": "adjective", "def": "Interested in finding out information."},
    {"word": "dinosaur", "type": "noun", "def": "A member of a group of extinct reptiles."},
    {"word": "brilliant", "type": "adjective", "def": "Showing great intelligence."},
    {"word": "vacuum", "type": "verb", "def": "To clean by suction."},
    {"word": "gorgeous", "type": "adjective", "def": "Dazzlingly beautiful."},
    {"word": "monsoon", "type": "noun", "def": "The season of heavy rainfall in India."},
    {"word": "dangerous", "type": "adjective", "def": "Involving risk; unsafe."},
    {"word": "avocado", "type": "noun", "def": "Green fruit, also called alligator pear."},
    {"word": "valentine", "type": "noun", "def": "Something sent to a sweetheart on Feb 14."},
    {"word": "February", "type": "noun", "def": "The second month of the year."},
    {"word": "formation", "type": "noun", "def": "A group of troops arranged in order."},
    {"word": "especially", "type": "adverb", "def": "In particular."},
]

# --- SESSION STATE SETUP ---
if 'word_list' not in st.session_state:
    st.session_state.word_list = original_words.copy()
if 'word_index' not in st.session_state:
    st.session_state.word_index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'quiz_complete' not in st.session_state:
    st.session_state.quiz_complete = False  # Tracks if the current word was answered correctly

# --- AUDIO FUNCTION ---
def text_to_speech(text):
    if not has_audio:
        return None
    try:
        tts = gTTS(text=text, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        return fp
    except:
        return None

# --- SIDEBAR ---
st.sidebar.title("🐝 Spelling Bee App")
mode = st.sidebar.radio("Choose a Mode:", ["📖 Study Words", "✍️ Spelling Quiz"])
st.sidebar.write("---")

if st.sidebar.button("🔀 Shuffle Words"):
    random.shuffle(st.session_state.word_list)
    st.session_state.word_index = 0
    st.session_state.quiz_complete = False
    st.sidebar.success("Words shuffled!")

# --- MAIN LOGIC ---
# Safety check for index range
if st.session_state.word_index >= len(st.session_state.word_list):
    st.session_state.word_index = 0

current_word = st.session_state.word_list[st.session_state.word_index]

# --- MODE: STUDY ---
if mode == "📖 Study Words":
    st.title("📖 Let's Learn!")
    st.write(f"Word {st.session_state.word_index + 1} of {len(st.session_state.word_list)}")
    
    st.markdown(f'<p class="big-font">{current_word["word"]}</p>', unsafe_allow_html=True)
    st.markdown(f"**Part of Speech:** *{current_word['type']}*")
    st.info(f"**Definition:** {current_word['def']}")

    if st.button("🔊 Play Sound"):
        sound = text_to_speech(current_word["word"])
        if sound:
            st.audio(sound, format='audio/mp3')
        else:
            st.warning("Audio not available (check requirements.txt).")

    st.markdown("---")
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("⬅️ Previous"):
            st.session_state.word_index = max(0, st.session_state.word_index - 1)
            st.rerun()
    with c2:
        if st.button("Next ➡️"):
            st.session_state.word_index = min(len(st.session_state.word_list) - 1, st.session_state.word_index + 1)
            st.rerun()

# --- MODE: QUIZ ---
elif mode == "✍️ Spelling Quiz":
    st.title("✍️ Spelling Quiz")
    st.write(f"**Score:** {st.session_state.score} ⭐")
    
    # Progress bar
    progress = (st.session_state.word_index) / len(st.session_state.word_list)
    st.progress(progress)

    st.markdown(f"### Word #{st.session_state.word_index + 1}")
    st.info(f"**Definition:** {current_word['def']}")
    
    if st.button("🔊 Hear Word"):
        sound = text_to_speech(current_word["word"])
        if sound:
            st.audio(sound, format='audio/mp3')
        else:
            st.warning("Audio not available.")

    # If the user hasn't answered correctly yet, show the input box
    if not st.session_state.quiz_complete:
        user_spelling = st.text_input("Type the word here:", key=f"input_{st.session_state.word_index}")
        
        if st.button("Check Spelling ✅"):
            if user_spelling.strip().lower() == current_word["word"].lower():
                st.balloons()
                st.success(f"🎉 Correct! The word is **{current_word['word']}**.")
                st.session_state.score += 1
                st.session_state.quiz_complete = True # Set flag to show Next button
                st.rerun()
            else:
                st.error("Not quite! Try again.")
                st.write(f"Hint: Starts with **{current_word['word'][0]}** and ends with **{current_word['word'][-1]}**.")

    # If the user answered correctly, show the success message and the Next button
    else:
        st.success(f
