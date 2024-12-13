import streamlit as st

#Sidebar menu x
st.sidebar.title("Navigation")
st.sidebar.page_link('./pages/chat.py', label='Chatbot Home')


# Header
st.title('Sales Assistant Agent 🤖')
st.markdown(
    """
    <div style='font-size:18px; line-height:1.5;'>
        <strong>Chatbot powered by Groq</strong><br>
        <em>Using the LLM llama3-8b-8192</em><br>
        <span>Perscholas 2024-01-AIPE, <b>Kenneth Cruz</b></span>
    </div>
    """,
    unsafe_allow_html=True
)
st.divider()

st.subheader('About this Project')
st.write('This')


