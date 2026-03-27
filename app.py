import streamlit as st
from config import GEMINI_API_KEY, GEMINI_MODEL, MAX_OUTPUT_TOKENS
from google import genai
from personas.sherlock import SHERLOCK
from personas.yoda import YODA
from personas.lady_whistledown import LADY_WHISTLEDOWN
from personas.phil import PHIL
from personas.barney import BARNEY
from prompts.system_prompt import build_system_prompt
from rag import load_pdf, split_into_chunks, create_collection, search_collection
from agent import search_web, needs_web_search

PERSONAS = {
    "Sherlock Holmes 🔍": SHERLOCK,
    "Yoda 🌿": YODA,
    "Lady Whistledown 📜": LADY_WHISTLEDOWN,
    "Phil Dunphy 🏡": PHIL,
    "Barney Stinson 👔": BARNEY,
}
st.set_page_config(page_title="AI Persona Engine", page_icon="🎭")
st.title("🎭 AI Persona Roleplay Engine")

# Sidebar
with st.sidebar:
    st.header("Choose Your Character")
    persona_name = st.selectbox("Select a persona", list(PERSONAS.keys()))
    persona = PERSONAS[persona_name]
    
    st.divider()
    
    uploaded_file = st.file_uploader("Upload a PDF (optional)", type="pdf")
    # Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "collection" not in st.session_state:
    st.session_state.collection = None

if "current_persona" not in st.session_state:
    st.session_state.current_persona = persona_name
    # Handle persona switch - clear chat if persona changes
if st.session_state.current_persona != persona_name:
    st.session_state.messages = []
    st.session_state.current_persona = persona_name

# Handle PDF upload
if uploaded_file and st.session_state.collection is None:
    with st.spinner("Loading PDF..."):
        import tempfile, os
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        text = load_pdf(tmp_path)
        chunks = split_into_chunks(text)
        st.session_state.collection = create_collection(chunks)
        os.unlink(tmp_path)
    st.sidebar.success(f"✅ PDF loaded!")
    # Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
user_input = st.chat_input(f"Chat with {persona_name}...")

if user_input:
    # Show user message
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
# Build conversation for Gemini
    client = genai.Client(api_key=GEMINI_API_KEY)
    system_prompt = build_system_prompt(persona)
    
    conversation_history = []
    for msg in st.session_state.messages:
        role = "model" if msg["role"] == "assistant" else "user"
        conversation_history.append({
            "role": role,
            "parts": [{"text": msg["content"]}]
        })

    # Check RAG or Agent
    if st.session_state.collection:
        relevant_chunks = search_collection(st.session_state.collection, user_input)
        context = "\n\n".join(relevant_chunks)
        augmented_input = f"Context from document:\n{context}\n\nUser question: {user_input}"
    elif needs_web_search(user_input, client):
        with st.spinner("🔍 Searching the web..."):
            web_results = search_web(user_input)
        augmented_input = f"Current information from web:\n{web_results}\n\nUser question: {user_input}"
    else:
        augmented_input = user_input

    conversation_history[-1]["parts"][0]["text"] = augmented_input

    # Get response
    with st.spinner("Thinking..."):
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=conversation_history,
            config={
                "system_instruction": system_prompt,
                "max_output_tokens": MAX_OUTPUT_TOKENS
            }
        )
    
    reply = response.text
    
    # Show assistant response
    with st.chat_message("assistant"):
        st.write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})