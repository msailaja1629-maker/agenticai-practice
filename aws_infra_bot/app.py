import streamlit as st
from agent import InfraAgent

st.set_page_config(page_title="AWS Infra Bot", page_icon="🤖")

st.title("🛡️ Agentic AI Infrastructure Bot")
st.markdown("Your AI assistant for AWS Inventory, Compliance, and Cost Optimization.")

# Initialize the Agent
if "agent" not in st.session_state:
    st.session_state.agent = InfraAgent()

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about your AWS resources..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing infrastructure..."):
            response = st.session_state.agent.ask(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})