import streamlit as st
import random

# Import words
from words import words_dict

# Page configuration
st.set_page_config(
    layout="centered",
    menu_items={},
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
    <style>
    footer {visibility: hidden;}
    .book-container {
        background-color: #f9f7f1;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 2px rgba(0,0,0,0.1), 
                    0 8px 16px rgba(0,0,0,0.1);
        margin: 0;
        border-left: 15px solid #8B4513;
        max-width: 100%;
        box-sizing: border-box;
    }
    
    /* Responsive padding adjustments */
    @media (max-width: 768px) {
        .book-container {
            padding: 2.25rem;
            border-left-width: 10px;
        }
    }
    
    /* Further adjustments for very small screens */
    @media (max-width: 480px) {
        .book-container {
            padding: 2rem;
            border-left-width: 8px;
        }
    }
    
    .book-title {
        font-family: 'Georgia', serif;
        color: #8B4513;
        text-align: center;
        font-size: clamp(1.2rem, 4vw, 1.8rem);
        margin-bottom: 0.75rem;
    }
    
    .text {
        font-family: 'Georgia', serif;
        color: #444;
        text-align: center;
        margin-bottom: 1.5rem;
        font-style: italic;
        font-size: clamp(0.9rem, 3vw, 1rem);
    }
    
    .word-title {
        font-family: 'Georgia', serif;
        color: #444;
        text-align: center;
        border-bottom: 2px solid #8B4513;
        padding-bottom: 0.75rem;
        margin-bottom: 1.5rem;
        font-size: clamp(1.5rem, 5vw, 2.5rem);
    }
    
    .section-content {
        font-family: 'Georgia', serif;
        color: #444;
        margin: 0.75rem 0;
        padding: 0.5rem;
        border-bottom: 1px solid #ddd;
        font-size: clamp(0.9rem, 3vw, 1rem);
    }
            
    div.stButton > button {
        background-color: #8B4513;
        color: white;
        width: 100%;
        margin: 0 auto;
        display: block;
    }
    
    div.stButton > button:active, 
    div.stButton > button:focus,
    div.stButton > button:hover,
    div.stButton > button:active:hover {
        background-color: #8B4513 !important;
        color: white !important;
        border-color: #8B4513 !important;
        box-shadow: none !important;
    }
            
    div.stButton > button:hover {
        background-color: #A0522D;
    }
    
    div.stButton > button:active {
        background-color: #5C3317;
    }
    
    div.stSelectbox > div > div {
        background-color: #f9f7f1;
        border-color: #8B4513;
        color: #444;
        max-width: 100%;
    }
    
    /* Add container width control */
    .main .block-container {
        max-width: 100% !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        padding-top: 2rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'words_shown' not in st.session_state:
    st.session_state.words_shown = []
if 'remaining_words' not in st.session_state:
    st.session_state.remaining_words = list(words_dict.keys())
if 'current_word' not in st.session_state:
    st.session_state.current_word = None

def choose_new_word():
    if not st.session_state.remaining_words:
        # Reset if all words have been shown
        st.session_state.remaining_words = list(words_dict.keys())
        st.session_state.words_shown = []

    # Choose a new word
    new_word = random.choice(st.session_state.remaining_words)
    st.session_state.remaining_words.remove(new_word)
    st.session_state.words_shown.append(new_word)
    st.session_state.current_word = new_word

# Main app
def main():
    col1, col2, col3 = st.columns([1, 6, 1])

    with col2:
        # Create two columns for the buttons
        button_col1, button_col2 = st.columns(2)

        with button_col1:
            if st.button("🎲 TILFÆLDIGT ORD", use_container_width=True):
                choose_new_word()

        with button_col2:
            # Get the list of words and find the index of the current word
            options = sorted(words_dict.keys())
            if st.session_state.current_word in options:
                current_word_index = options.index(st.session_state.current_word)
            else:
                current_word_index = 0  # Default to the first word if current_word is None

            # Add dropdown to select specific word
            selected_word = st.selectbox(
                "Vælg et ord",
                options=options,
                index=current_word_index,
                key="word_selector",
                label_visibility="collapsed"
            )

            # Update current_word if a new word is selected
            if selected_word != st.session_state.current_word:
                st.session_state.current_word = selected_word

        # Initialize current word if none selected
        if st.session_state.current_word is None:
            choose_new_word()

        word = st.session_state.current_word
        word_info = words_dict[word]

        # Display word details
        if word == "no CAP":
            content = f"""
                <div class="book-container">
                    <div class="book-title">IM's Zoomer Ordbog</div>
                    <div class="text">Til yndlingskollegaen. 30 er det nye 20! (no cap 🧢)</div>
                    <div class="word-title">{word.capitalize()}</div>
                    <div class="section-content"><strong>Ordklasse</strong><br>{word_info["ordklasse"]}</div>
                    <div class="section-content"><strong>Betydninger</strong><br>{word_info["betydninger"]}</div>
                    <div class="section-content"><strong>Eksempler</strong><br><em>{word_info["eksempler"]}</em></div>
                    <div class="section-content"><strong>Synonymer</strong><br>{", ".join(word_info["synonymer"])}</div>
                </div>
            """
        else:
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

if __name__ == "__main__":
    main()
