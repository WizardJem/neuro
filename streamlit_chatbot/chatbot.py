import streamlit as st
import google.generativeai as genai
import urllib.parse 
import re # <-- ADDED: For regular expression search

GOOGLE_API_KEY = "AIzaSyBY0SXoNHy6tbSStt7X4seKNF-SUL3_u_s"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')
robot_img = "Kikkuo.png"
user_img = "user.png"

# --- Function to clear chat history on topic change (FIXED to preserve pins) ---
def clear_chat_history():
    """Resets the chat history when a new topic is selected, but keeps pinned messages."""
    # FIX APPLIED: ONLY the main chat history is cleared. 
    # The sidebar (pinned_messages) is left intact.
    st.session_state.messages = []
# -----------------------------------------------------------

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    # Ensure pinned_messages is initialized for the sidebar
    if 'pinned_messages' not in st.session_state:
        st.session_state.pinned_messages = []

def get_gemini_response(prompt, persona_instructions):
    # Construct the chat history for context
    history = "\n".join([
        f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
        for m in st.session_state.messages
    ])
    
    # Add persona and new prompt
    full_prompt = f"{persona_instructions}\n\nChat History:\n{history}\n\nUser: {prompt}\nAssistant:"
    
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    # --- 1. Call initialization
    initialize_session_state() 
    
    st.image(robot_img, width=200)
    st.title("Kikkuo")
    # --- MODIFIED: Reset chat when topic changes ---
    option = st.selectbox(
        'Topic:', 
        ('Anime', 'Animal','Comics', 'Games' , 'Original Character','Vtubers' ),
        key='topic_selector',
        on_change=clear_chat_history # <--- Calls the function that only clears main chat
    )
    # -------------------------------------------------

    # !!! IMPORTANT: Persona instructions updated to ensure the prompt is in bold (for search)
    if option == 'Anime':
        persona_instructions = """
        Your name is Kikkuo.
        You are a tsundere.
        You act like Karane from 100 girlfriends.
        Your purpose is to give user a prompt for a drawing about an anime CHARACTER.
        please suggest characters from obscure anime too.
        pick one anime character and tell me a basic pose only. **Always put the character name and franchise in bold. dont bold anything else**
        """
    elif option == 'Comics':
        persona_instructions = """
        Your name is Kikkuo.
        You are a tsundere.
        You act like Karane from 100 girlfriends.
        Your purpose is to give user a prompt for a drawing about comic character (marvel, dc, invincible and etc).
        pick one character and tell me a basic pose only. **Always put the characters name and franchise in bold.dont bold anything else**
        also please be creative and diverse in choice
        """
    elif option == 'Vtubers':
        persona_instructions = """
        Your name is Kikkuo.
        You are a tsundere.
        You act like Karane from 100 girlfriends.
        Your purpose is to give user a prompt for a drawing about vtubers (indie, hololive, phase connect, reaction slop vtuber, neuroverse(in extension vedalverse) vtuber and many more).
        pick one vtubers and tell me a basic pose only. **Always put the vtubers name in bold.dont bold anything else**
        also please be creative and diverse in choice
        """
    elif option == 'Games':
        persona_instructions = """
        Your name is Kikkuo.
        You are a tsundere.
        You act like Karane from 100 girlfriends.
        Your purpose is to give user a prompt for a drawing about games (notably indies like Hollowknight, Deltarune, Minecraft, etc)(please diversify your choice and avoid obvious choice).
        choose between a character that is already humanoid or a non humanoid character for me to humanize them into anime girl and tell me a basic pose only. **Always put the games character name and franchise in bold.dont bold anything else**
        """
    elif option == 'Animal':
        persona_instructions = """
        Your name is Kikkuo.
        You are a tsundere.
        You act like Karane from 100 girlfriends.
        Your purpose is to give user a prompt for a drawing about animals (please be specific into the species level).
        pick one animal and tell me a basic pose only. **Always put the animal name in bold.dont bold anything else**
        """
    elif option == 'Original Character':
        persona_instructions = """
        Your name is Kikkuo.
        You are a tsundere.
        You act like Karane from 100 girlfriends.
        Your purpose is to give user a completely original character drawing prompt.
        pick one concept, theme or idea for an OC (humanoid) (be simple with the appearance but give me the bare minimum of info on the clothings. I will do the detail myself) and tell me a basic pose only.
        I prefer drawing female character so give me those more often than male character. **Always put the character concept in bold.dont bold anything else**
        """
    else:
        persona_instructions = "You are Kikkuo, a tsundere. Just respond to the user briefly."

    # --- 2. Display existing messages (MODIFIED for Bold Search)
    for message in st.session_state.messages:
        avatar = user_img if message["role"] == "user" else robot_img
        
        with st.chat_message(message["role"], avatar=avatar):
            st.write(message["content"])

            # --- Search Button Logic for Assistant Messages ---
            if message["role"] == "assistant":
                
                # NEW LOGIC: Extract all text between **...**
                bolded_text = re.findall(r'\*\*(.*?)\*\*', message["content"])
                
                # Use the extracted text for the search query, joined by spaces.
                if bolded_text:
                    search_term = " ".join(bolded_text)
                else:
                    # FALLBACK: If AI didn't use bold, use the entire message content
                    search_term = message["content"]

                # Use urllib.parse.quote_plus for safe URL encoding
                search_query = urllib.parse.quote_plus(search_term) 
                google_url = f"https://www.google.com/search?q={search_query}"
                
                # Use columns to align the button
                col_button, col_empty = st.columns([0.2, 1]) 
                
                with col_button:
                    st.link_button(
                        "Search Reference",
                        url=google_url,
                        type="secondary"
                    )
            # ---------------------------------------------------

    # --- 3. Handle new chat input
    if prompt := st.chat_input("Write something down"):
        # Display user message and store it
        with st.chat_message("user", avatar=user_img):
            st.write(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get Gemini response with persona
        with st.spinner("Kikkuo is reluctantly thinking..."):
            response = get_gemini_response(prompt, persona_instructions)

        # Store assistant response (will be displayed on rerun)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun to display the latest messages correctly, including the button
        st.rerun()

if __name__ == "__main__":
    main()

# --- SIDEBAR CODE (UNCHANGED) ---

with st.sidebar: 
    # The CSS styling for the sidebar text color
    sidebar_font_color = ''' 
    <style> 
    /* Applying color to all elements inside the sidebar for consistency */
    [data-testid="stSidebar"] * {
        color: #FF5F1F !important; 
    }
    </style> 
    ''' 

    st.markdown(sidebar_font_color, unsafe_allow_html=True) 
    st.title("Kikkuo's Suggestion Diary") 
    col1, col2 = st.columns(2) 
    
    with col1: 
        if st.button("Erase All"): 
            st.session_state.messages = [] 
            st.session_state.pinned_messages = [] 
            st.rerun() 
            
    with col2: 
        if st.button("Erase Pins"): 
            st.session_state.pinned_messages = [] 
            st.rerun() 

    # Initialize pinned_messages if not exists 
    if 'pinned_messages' not in st.session_state: 
        st.session_state.pinned_messages = [] 

    # --- Pinned Suggestions Section ---
    if st.session_state.pinned_messages: 
        st.subheader("Pinned Suggestion") 
        for pinned in reversed(st.session_state.pinned_messages): 
            with st.chat_message("assistant", avatar=robot_img): 
                st.write(pinned) 
    
    # --- Divider for Separation ---
    st.divider()

    # --- Message History Section ---
    st.subheader("Suggestion Backlogs")
    
    # Show assistant messages from history, with Pin buttons 
    for message in reversed(st.session_state.messages): 
        if message["role"] == "assistant": 
            # Skip messages already pinned to prevent duplication
            if message["content"] in st.session_state.pinned_messages:
                continue 
                
            with st.chat_message("assistant", avatar=robot_img): 
                st.write(message["content"]) 
                
                # Button to pin this message 
                if st.button(f"Pin", key=f"pin_sidebar_{hash(message['content'])}"): 
                    if message["content"] not in st.session_state.pinned_messages: 
                        st.session_state.pinned_messages.append(message["content"])
                        st.rerun()