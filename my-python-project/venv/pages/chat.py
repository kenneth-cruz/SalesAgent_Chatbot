import streamlit as st
from groq import Groq

# Initialize Groq client
client = Groq(api_key=st.secrets['GROQ_API_KEY'])

# Session State Initialization
if "default_model" not in st.session_state:
    st.session_state['default_model'] = "llama3-8b-8192"

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'insights' not in st.session_state:
    st.session_state.insights = []  # To store generated insights

# Sidebar Menu
st.sidebar.title('Chat Navigation')
sales_insights = "Sales Insights"
saved_insights = "Saved Insights"
nav_option = st.sidebar.radio(
    "Choose an option:",
    ["Chat", sales_insights, saved_insights]
)

# Page Content Based on Navigation
if nav_option == "Chat":
    # Chat Header
    st.title('Chatbot Home')
    st.write("This page allows users to view and manage their chats. Chatbot powered by Groq.")
    st.divider()

    # Display Chat Messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input Section
    if prompt := st.chat_input():
        # Add the user's message to the session state
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        # Display user message
        with st.chat_message('user'):
            st.markdown(prompt)

        # Generate assistant response
        with st.chat_message("assistant"):
            response_text = st.empty()
            completion = client.chat.completions.create(
                model=st.session_state.default_model,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            full_response = ''
            for chunk in completion:
                full_response += chunk.choices[0].delta.content or ''
                response_text.markdown(full_response)

            # Save assistant's response to the session state
            st.session_state.messages.append({"role": "assistant", "content": full_response})

elif nav_option == sales_insights:
    # Sales Insights Header
    st.title(sales_insights)
    st.write("Provide the necessary details to generate meaningful insights for your sales strategy.")
    st.divider()

    # Input Section for Sales Rep
    with st.form("sales_inputs"):
        product_name = st.text_input("Product Name", help="What product are you selling?")
        company_url = st.text_input("Company URL", help="Enter the URL of the target company.")
        product_category = st.text_input(
            "Product Category",
            help="Provide a short description or category of the product (e.g., Data Warehousing)."
        )
        competitors = st.text_area(
            "Competitors (URLs)",
            help="Enter URLs of competitors, one per line."
        )
        value_proposition = st.text_area(
            "Value Proposition",
            help="Summarize your product’s value in one sentence."
        )
        target_customer = st.text_input(
            "Target Customer",
            help="Who are you trying to sell this product to?"
        )
        product_overview = st.file_uploader(
            "Upload Product Overview",
            type=["pdf", "docx", "txt"],
            help="Optionally upload a product overview document for additional insights."
        )

        # Submit Button
        submitted = st.form_submit_button("Generate Insights")

        if submitted:
            st.write("### Submitted Sales Data")
            st.write(f"**Product Name:** {product_name}")
            st.write(f"**Company URL:** {company_url}")
            st.write(f"**Product Category:** {product_category}")
            st.write(f"**Competitors:**\n{competitors}")
            st.write(f"**Value Proposition:** {value_proposition}")
            st.write(f"**Target Customer:** {target_customer}")
            
            # Process Uploaded File
            if product_overview:
                st.write(f"Uploaded File: {product_overview.name}")
                st.write("Processing uploaded file for insights...")

            # Example: Send the data to the LLM for analysis
            sales_prompt = f"""
            Provide sales insights for the following:
            Product: {product_name}
            Company: {company_url}
            Category: {product_category}
            Competitors: {competitors}
            Value Proposition: {value_proposition}
            Target Customer: {target_customer}
            """
            if product_overview:
                sales_prompt += "\nAdditional Information: Parsed content from the uploaded file."

            st.write("### Generating Insights...")
            with st.spinner("Analyzing..."):
                try:
                    completion = client.chat.completions.create(
                        model=st.session_state.default_model,
                        messages=[{"role": "user", "content": sales_prompt}]
                    )
                    response_content = completion.choices[0].message.content

                    # Save insights to session state
                    st.session_state.insights.append({
                        "Product Name": product_name,
                        "Company URL": company_url,
                        "Category": product_category,
                        "Value Proposition": value_proposition,
                        "Insight": response_content
                    })

                    st.write("### Insights:")
                    st.write(response_content)

                except Exception as e:
                    st.error(f"An error occurred: {e}")

elif nav_option == saved_insights:
    # Saved Insights Page
    st.title(saved_insights)
    st.write("Review all previously generated insights here.")
    st.divider()

    if st.session_state.insights:
        for idx, insight in enumerate(st.session_state.insights, start=1):
            with st.expander(f"Insight #{idx}: {insight['Product Name']}"):
                st.write(f"**Product Name:** {insight['Product Name']}")
                st.write(f"**Company URL:** {insight['Company URL']}")
                st.write(f"**Category:** {insight['Category']}")
                st.write(f"**Value Proposition:** {insight['Value Proposition']}")
                st.write(f"**Insight:** {insight['Insight']}")
    else:
        st.info("No insights saved yet.")
