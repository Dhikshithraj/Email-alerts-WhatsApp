import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta
import random
import imaplib
import email
from email.header import decode_header
import base64

# Set page configuration
st.set_page_config(
    page_title="Email Alerts on WhatsApp",
    page_icon="📧",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #25D366;
        text-align: center;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #128C7E;
        border-bottom: 2px solid #25D366;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    .email-card {
        background-color: #f0f2f6;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .whatsapp-card {
        background-color: #dcf8c6;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #25D366;
    }
    .log-entry {
        font-family: monospace;
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
    }
    .success { color: #25D366; }
    .error { color: #ff4b4b; }
    .info { color: #1f77b4; }
    .warning { color: #ffa500; }
    .config-box {
        background-color: #f9f9f9;
        border-radius: 0.5rem;
        padding: 1.5rem;
        border: 1px solid #ddd;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.markdown('<h1 class="main-header">📧 Email Alerts on WhatsApp</h1>', unsafe_allow_html=True)
st.markdown("""
This application demonstrates how email notifications can be forwarded to WhatsApp using Twilio as a middleware platform.
The actual implementation uses Twilio's WhatsApp API and IMAP email protocols to provide real-time notifications.
""")

# Introduction
with st.expander("ℹ️ About This Project"):
    st.write("""
    ### Project Overview
    This system connects your email account to WhatsApp, allowing you to receive email notifications directly on WhatsApp. 
    It uses IMAP to monitor your email account and the WhatsApp Business API (via Twilio) to send notifications.
    
    ### How It Works
    1. The system periodically checks your email account using IMAP protocol
    2. When new emails are detected, they are processed and formatted for WhatsApp
    3. Using Twilio's WhatsApp API, notifications are sent to your WhatsApp number
    4. The system handles authentication, security, and error handling
    
    ### Technology Stack
    - **Email Protocol**: IMAP for receiving emails
    - **Middleware**: Twilio WhatsApp API
    - **Backend**: Python
    - **Frontend**: Streamlit for demonstration
    """)

# Configuration section
st.markdown('<h2 class="sub-header">⚙️ System Configuration</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="config-box">', unsafe_allow_html=True)
    st.markdown("**📧 Email Configuration**")
    email_provider = st.selectbox(
        "Email Provider",
        ["Gmail", "Outlook", "Yahoo", "Custom IMAP"]
    )
    
    email_address = st.text_input("Email Address", "your.email@example.com")
    
    check_frequency = st.slider(
        "Check Frequency (minutes)",
        min_value=1,
        max_value=60,
        value=5
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="config-box">', unsafe_allow_html=True)
    st.markdown("**💬 WhatsApp Configuration**")
    whatsapp_number = st.text_input("Your WhatsApp Number", "+1234567890")
    
    notification_preferences = st.multiselect(
        "Notify for",
        ["Primary emails", "Social notifications", "Promotions", "Updates", "Forums"],
        default=["Primary emails", "Updates"]
    )
    
    st.info("In the actual implementation, Twilio API credentials would be securely stored here")
    st.markdown('</div>', unsafe_allow_html=True)

if st.button("🔄 Save Configuration", use_container_width=True):
    st.success("Configuration saved successfully!")
    st.info("In the actual implementation, these settings would be stored in a secure database")

# Main content - two columns
st.markdown('<h2 class="sub-header">📋 System Overview</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**📥 Email Processing**")
    st.write("""
    1. Connects to email server via IMAP
    2. Checks for new emails periodically
    3. Extracts sender, subject, and preview
    4. Formats for WhatsApp notification
    """)
    
    st.markdown("**🔐 Security Features**")
    st.write("""
    - Encrypted credential storage
    - Secure IMAP connection
    - Twilio API authentication
    - Error handling and logging
    """)

with col2:
    st.markdown("**📤 WhatsApp Integration**")
    st.write("""
    1. Uses Twilio WhatsApp Sandbox/API
    2. Sends formatted notifications
    3. Handles delivery status
    4. Manages rate limiting
    """)
    
    st.markdown("**⚡ Real-time Processing**")
    st.write("""
    - Background email monitoring
    - Instant notification triggering
    - Status tracking and logging
    - Failure recovery机制
    """)

# Simulation section
st.markdown('<h2 class="sub-header">🎯 Live Simulation</h2>', unsafe_allow_html=True)

# Sample email data
sample_emails = [
    {
        "sender": "Twitter <info@twitter.com>",
        "subject": "New login to your account",
        "time": "2 minutes ago",
        "preview": "We noticed a new login to your Twitter account from a new device.",
        "category": "Updates"
    },
    {
        "sender": "Amazon <orders@amazon.com>",
        "subject": "Your order has been shipped",
        "time": "15 minutes ago",
        "preview": "Your order #1234567890 has been shipped and is on its way.",
        "category": "Primary emails"
    },
    {
        "sender": "LinkedIn <newsletter@linkedin.com>",
        "subject": "Weekly job recommendations",
        "time": "1 hour ago",
        "preview": "Based on your profile, here are jobs you might be interested in.",
        "category": "Promotions"
    }
]

# Simulation controls
sim_col1, sim_col2 = st.columns(2)

with sim_col1:
    if st.button("🔍 Check for New Emails", use_container_width=True):
        with st.spinner("Checking for new emails..."):
            time.sleep(2)
            
            # Simulate finding a new email
            new_email = {
                "sender": "EPRA Journal <journal@epra.org>",
                "subject": "Your paper has been published",
                "time": "Just now",
                "preview": "We are pleased to inform you that your paper has been accepted for publication.",
                "category": "Primary emails"
            }
            
            sample_emails.insert(0, new_email)
            st.success("Found 1 new email!")

with sim_col2:
    if st.button("📤 Send to WhatsApp", use_container_width=True):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            progress_bar.progress(i + 1)
            if i < 25:
                status_text.text("Connecting to Twilio API...")
            elif i < 50:
                status_text.text("Authenticating with WhatsApp...")
            elif i < 75:
                status_text.text("Sending message...")
            else:
                status_text.text("Finalizing...")
            time.sleep(0.02)
        
        status_text.text("✅ Message sent to WhatsApp!")
        st.balloons()

# Display sample emails
st.markdown("#### 📧 Recent Emails")
for email in sample_emails:
    if email["category"] in notification_preferences:
        with st.container():
            st.markdown(f"""
            <div class="email-card">
                <b>{email['sender']}</b>
                <p style="margin: 0.2rem 0; font-weight: bold;">{email['subject']}</p>
                <p style="margin: 0.2rem 0; color: #555;">{email['preview']}</p>
                <p style="margin: 0; font-size: 0.8rem; color: #777;">{email['time']} • {email['category']}</p>
            </div>
            """, unsafe_allow_html=True)

# System status and logs
st.markdown('<h2 class="sub-header">📊 System Status</h2>', unsafe_allow_html=True)

status_col1, status_col2, status_col3 = st.columns(3)

with status_col1:
    st.metric("Emails Processed", "24", "3 today")
    
with status_col2:
    st.metric("WhatsApp Messages Sent", "18", "2 today")
    
with status_col3:
    st.metric("System Uptime", "99.8%", "0.2% from last week")

# Logs section
st.markdown("#### 📝 Recent Activity Logs")
log_container = st.container()

with log_container:
    st.markdown("""
    <div class="log-entry info">2024-12-28 11:23:09,228 [INFO] Checking for new emails...</div>
    <div class="log-entry info">2024-12-28 11:23:11,962 [DEBUG] Processing email: Subject='Work From Home Opportunity', Sender='Bandigari Harichandana'</div>
    <div class="log-entry info">2024-12-28 11:23:12,306 [INFO] Connecting to Twilio API...</div>
    <div class="log-entry success">2024-12-28 11:23:13,526 [INFO] WhatsApp message sent: SMfdbc6b45f97be0</div>
    <div class="log-entry info">2024-12-28 11:23:13,527 [INFO] Email processed successfully</div>
    <div class="log-entry warning">2024-12-28 11:38:41,734 [WARNING] Network connectivity issue</div>
    <div class="log-entry info">2024-12-28 11:40:41,735 [INFO] Connection restored</div>
    """, unsafe_allow_html=True)

# Implementation details
with st.expander("🔧 Technical Implementation Details"):
    st.write("""
    ### Actual Implementation (Not shown in demo)
    
    The real system consists of several components:
    
    1. **IMAP Email Client**
    ```python
    import imaplib
    import email
    
    # Connect to IMAP server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(email_user, email_pass)
    mail.select("inbox")
    ```
    
    2. **Twilio WhatsApp Integration**
    ```python
    from twilio.rest import Client
    
    # Initialize Twilio client
    client = Client(account_sid, auth_token)
    
    # Send WhatsApp message
    message = client.messages.create(
        body="New email from {sender}: {subject}",
        from_='whatsapp:+14155238886',
        to='whatsapp:+1234567890'
    )
    ```
    
    3. **Background Processing**
    ```python
    import time
    import threading
    
    # Run email checks in background
    def check_emails_periodically():
        while True:
            check_new_emails()
            time.sleep(300)  # Check every 5 minutes
    
    # Start background thread
    email_thread = threading.Thread(target=check_emails_periodically)
    email_thread.daemon = True
    email_thread.start()
    ```
    
    4. **Security Measures**
    - Environment variables for API credentials
    - Encrypted credential storage
    - Secure IMAP connections with SSL
    - Input validation and sanitization
    """)

# Footer
st.divider()
st.caption("""
This is a demonstration of the Email Alerts on WhatsApp project. 
The actual implementation uses Twilio's WhatsApp API and IMAP email protocols but cannot be fully shown in this public demo for security reasons.
""")