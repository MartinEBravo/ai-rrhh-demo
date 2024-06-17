import json
import dotenv
import streamlit as st
from openai import OpenAI

# Load environment variables
dotenv.load_dotenv()

# Initialize OpenAI client
client = OpenAI()

contacts = [
    {
        "name": "John Doe",
        "email": "john.doe@gmail.com",
        "phone": "123-456-7890",
        "role": "Software Engineer",
    },
    {
        "name": "Jane Smith",
        "email": "jane.smith@gmail.com",
        "phone": "234-567-8901",
        "role": "Product Manager",
    },
    {
        "name": "Alice Johnson",
        "email": "alice.johnson@gmail.com",
        "phone": "345-678-9012",
        "role": "UX Designer",
    },
    {
        "name": "Bob Brown",
        "email": "bob.brown@gmail.com",
        "phone": "456-789-0123",
        "role": "Data Scientist",
    },
    {
        "name": "Charlie Davis",
        "email": "charlie.davis@gmail.com",
        "phone": "567-890-1234",
        "role": "DevOps Engineer",
    },
    {
        "name": "Diana Evans",
        "email": "diana.evans@gmail.com",
        "phone": "678-901-2345",
        "role": "Marketing Specialist",
    },
    {
        "name": "Ethan Foster",
        "email": "ethan.foster@gmail.com",
        "phone": "789-012-3456",
        "role": "Sales Manager",
    },
    {
        "name": "Fiona Green",
        "email": "fiona.green@gmail.com",
        "phone": "890-123-4567",
        "role": "HR Manager",
    },
    {
        "name": "George Harris",
        "email": "george.harris@gmail.com",
        "phone": "901-234-5678",
        "role": "CTO",
    },
    {
        "name": "Helen Martin",
        "email": "helen.martin@gmail.com",
        "phone": "012-345-6789",
        "role": "CEO",
    },
]

def openai_generate_text(context, prompt, conversation):
    """
    Generate text using OpenAI's GPT-3 API
    
    Args:
    context (str): Context for the conversation
    prompt (str): Prompt for the model
    conversation (array): Conversation history

    Returns:
    response (str): Response from the model
    conversation (array): Updated conversation history
    """

    messages = [
        {"role": "system", "content": context},
    ] + conversation

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True
    )

    response = ""
    message_container = st.chat_message("assistant")
    for chunk in completion:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            response += content
            yield content

    conversation.append({"role": "assistant", "content": response})

st.title("AI Partners")
st.write("Welcome to AI Partners! I'm going to help you write emails to your contacts.")

# Sidebar for showing and adding contacts
st.sidebar.title("Contacts")
contact_names = [contact["name"] for contact in contacts]
selected_contact = st.sidebar.selectbox("Select a contact", contact_names)

# Display selected contact details
if selected_contact:
    contact = next((contact for contact in contacts if contact["name"] == selected_contact), None)
    if contact:
        st.sidebar.write(f"**Name:** {contact['name']}")
        st.sidebar.write(f"**Email:** {contact['email']}")
        st.sidebar.write(f"**Phone:** {contact['phone']}")
        st.sidebar.write(f"**Role:** {contact['role']}")

# Add new contact form
st.sidebar.title("Add New Contact")
with st.sidebar.form(key='add_contact_form'):
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    role = st.text_input("Role")
    submit_button = st.form_submit_button(label='Add Contact')

    if submit_button:
        new_contact = {
            "name": name,
            "email": email,
            "phone": phone,
            "role": role,
        }
        contacts.append(new_contact)
        st.sidebar.success(f"Contact {name} added successfully!")

# Main content for email generation
if selected_contact:
    context = f"Envía un Email a {contact['name']} de correo {contact['email']} o llamada {contact['phone']}"
    conversation = []

    if 'generated_text' not in st.session_state:
        st.session_state.generated_text = ""

    prompt = st.text_input("Enter your email content prompt:")
    if st.button("Generate Email"):
        st.session_state.generated_text = ""
        for text in openai_generate_text(context, prompt, conversation):
            st.session_state.generated_text += text

    st.write("Generated Email Content:")
    st.write(st.session_state.generated_text)
