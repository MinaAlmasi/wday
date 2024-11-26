import streamlit as st
import random
from datetime import datetime

# import words
from words import words_dict

# Page configuration to hide the menu bar and set centered layout
st.set_page_config(
    layout="centered",
    menu_items={},
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .book-container {
        background-color: #f9f7f1;
        border-radius: 10px;
        padding: 2rem 2rem;  /* Increased padding */
        box-shadow: 0 4px 2px rgba(0,0,0,0.1), 
                    0 8px 16px rgba(0,0,0,0.1);
        margin: 0;
        border-left: 15px solid #8B4513;
        max-width: 100&;  /* Added max-width */
    }
    .book-title {
        font-family: 'Georgia', serif;
        color: #8B4513;
        text-align: center;
        font-size: 1.8rem;
        margin-bottom: 1rem;
    }
    
    .text {
        font-family: 'Georgia', serif;
        color: #444;
        text-align: center;
        margin-bottom: 2rem;
        margin-top: 0rem;
        font-style: italic;
        }
            
    .word-title {
        font-family: 'Georgia', serif;
        color: #444;
        text-align: center;
        border-bottom: 2px solid #8B4513;
        padding-bottom: 1rem;
        margin-bottom: 2rem;
        font-size: 2.5rem;
    }
    .section-content {
        font-family: 'Georgia', serif;
        color: #444;
        margin: 1rem 0;
        padding: 0.5rem;
        border-bottom: 1px solid #ddd;
    }
    button {
        margin-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_word' not in st.session_state:
    st.session_state.current_word = None
if 'last_update' not in st.session_state:
    st.session_state.last_update = None
if 'words_shown' not in st.session_state:
    st.session_state.words_shown = []

def get_word_of_the_day(words):
    today = datetime.now().date()
    if (st.session_state.last_update != today or 
        st.session_state.current_word is None):
        # Calculate the set of remaining words
        remaining_words = list(set(words.keys()) - set(st.session_state.words_shown))
        if not remaining_words:
            # All words have been shown; reset the list
            st.session_state.words_shown = []
            remaining_words = list(words.keys())
        # Choose a new word and update the session state
        st.session_state.current_word = random.choice(remaining_words)
        st.session_state.words_shown.append(st.session_state.current_word)
        st.session_state.last_update = today
    return st.session_state.current_word

def main():
    col1, col2, col3 = st.columns([1, 6, 1])
    
    with col2:
        # Get today's word
        word = get_word_of_the_day(words_dict)
        word_info = words_dict[word]
        
        # Book container with all content
        st.container()
        content = f"""
            <div class="book-container">
                <div class="book-title">IM's Zoomer Ordbog</div>
                <div class="text">Til yndlingskollegaen. 30 er det nye 20!</div>
                <div class="word-title">{word.capitalize()}</div>
                <div class="section-content"><strong>Ordklasse</strong><br>{word_info["ordklasse"]}</div>
                <div class="section-content"><strong>Betydninger</strong><br>{word_info["betydninger"]}</div>
                <div class="section-content"><strong>Eksempler</strong><br><em>{word_info["eksempler"]}</em></div>
                <div class="section-content"><strong>Synonymer</strong><br>{", ".join(word_info["synonymer"])}</div>
            </div>
        """
        st.markdown(content, unsafe_allow_html=True)
        
        # Button below the book container
        if st.button("📖 Lær et nyt ORD", use_container_width=True):
            st.session_state.current_word = random.choice(list(words_dict.keys()))
            st.rerun()

if __name__ == "__main__":
    main()