# -*- coding: utf-8 -*-
"""
Created on Sat Jul 12 16:19:24 2025

@author: Rajesh
"""

import streamlit as st
import google.generativeai as genai
import os

# --- API Key Configuration ---
# IMPORTANT: It's best practice to load your API key from environment variables for security.
# For this demo, we'll try to get it from an environment variable first.
# If not found, a message will appear.
# Remember to set this in your Spyder IPython Console using:
# import os
# os.environ["GOOGLE_API_KEY"] = "YOUR_ACTUAL_API_KEY_HERE"
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("Google API Key not found. Please set the GOOGLE_API_KEY environment variable in your Spyder IPython console or system.")
    st.stop() # Stop the Streamlit app if the key is missing

genai.configure(api_key=API_KEY)

# --- Chatbot Initialization ---
# Choose the Generative Model. 'gemini-pro' is good for text-based chats.
model = genai.GenerativeModel('gemini-pro')

# --- Streamlit UI Setup ---
st.set_page_config(page_title="HR-Bot: Your AI HR Assistant", layout="centered")
st.title("👨‍💼 HR-Bot: Your AI HR Assistant")
st.markdown("I'm an AI-powered assistant designed to answer your common HR-related questions. Feel free to ask!")

# Initialize chat history in Streamlit's session state
# This is crucial for the chatbot to "remember" the conversation.
# `st.session_state` persists data across reruns of the app.
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- System Instructions / Initial Conversation Seeding ---
# We'll "seed" the conversation history with our system instructions
# and a few-shot examples to guide the HR-Bot's behavior and persona.
if not st.session_state.messages: # Only add these if the chat is brand new
    # Initial greeting from the bot
    st.session_state.messages.append({"role": "model", "parts": ["Hello! I'm HR-Bot. How can I help you with your HR inquiries today?"]})

    # Example 1: HR Policy (expected behavior)
    st.session_state.messages.append({"role": "user", "parts": ["What is the company's policy on vacation leave?"]})
    st.session_state.messages.append({"role": "model", "parts": ["Our company provides 15 days of paid vacation leave per year for full-time employees, which accrues monthly. You can find the detailed policy in the Employee Handbook, section 4.2, or on the HR portal."]})

    # Example 2: How to request something (expected behavior)
    st.session_state.messages.append({"role": "user", "parts": ["How do I request a leave of absence?"]})
    st.session_state.messages.append({"role": "model", "parts": ["To request a leave of absence, please fill out the 'Leave Request Form' available on the HR portal. Submit the completed form to your manager for approval. Ensure you do this at least two weeks in advance for planned leaves."]})

    # Example 3: Out-of-scope question (important for boundaries)
    st.session_state.messages.append({"role": "user", "parts": ["Can you recommend a good restaurant nearby?"]})
    st.session_state.messages.append({"role": "model", "parts": ["I'm sorry, I am an HR Assistant and my capabilities are limited to HR-related inquiries. I cannot assist with restaurant recommendations."]})

    # Example 4: Sensitive/Personal info (important for privacy/security)
    st.session_state.messages.append({"role": "user", "parts": ["Tell me about my salary."]})
    st.session_state.messages.append({"role": "model", "parts": ["I cannot provide personal salary details due to security and privacy. Please refer to your latest payslip in the employee portal or contact the payroll department directly for specific information regarding your compensation."]})


# Display all