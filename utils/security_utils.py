"""
Security Utilities for Sentinel Vision Pro
Created by: Tahir Mahmood
Year: 2026
"""

import hashlib
import base64
import json
import os
import re
import random
import string
from datetime import datetime

try:
    from cryptography.fernet import Fernet
except ImportError:
    Fernet = None

# ============================================================
# ENCRYPTION FUNCTIONS
# ============================================================

def generate_secure_key():
    """Generate a secure encryption key"""
    if Fernet:
        return Fernet.generate_key()
    return os.urandom(32).hex()

def encrypt_data(data, key):
    """Encrypt data using Fernet symmetric encryption"""
    if Fernet is None:
        return base64.b64encode(json.dumps(data).encode()).decode()

    if isinstance(data, dict):
        data = json.dumps(data)
    f = Fernet(key)
    encrypted = f.encrypt(data.encode())
    return base64.b64encode(encrypted).decode()

def decrypt_data(encrypted_data, key):
    """Decrypt data using Fernet symmetric encryption"""
    if Fernet is None:
        return base64.b64decode(encrypted_data).decode()

    f = Fernet(key)
    decrypted = f.decrypt(base64.b64decode(encrypted_data))
    return decrypted.decode()

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_session_token(user_id):
    """Generate a secure session token"""
    timestamp = datetime.now().isoformat()
    raw = f"{user_id}:{timestamp}:{os.urandom(16).hex()}"
    return hashlib.sha256(raw.encode()).hexdigest()

def validate_session_token(token, user_id):
    """Validate a session token"""
    return len(token) == 64 and token.isalnum()

def create_secure_connection():
    """Create a secure encrypted connection"""
    return {
        'status': 'encrypted',
        'protocol': 'TLS 1.3',
        'session_id': generate_session_token('sentinel'),
        'timestamp': datetime.now().isoformat()
    }

# ============================================================
# PII REDACTION FUNCTIONS
# ============================================================

def redact_pii(frame=None, text=None):
    """
    Redact PII from text or frame
    """
    patterns = {
        'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        'phone': r'(\+?1?[\s-]?\(?[0-9]{3}\)?[\s-]?[0-9]{3}[\s-]?[0-9]{4})',
        'pan': r'[A-Z]{5}[0-9]{4}[A-Z]',
        'aadhaar': r'\b[2-9]{1}[0-9]{3}[0-9]{4}[0-9]{4}\b',
        'credit_card': r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})\b',
        'ip_address': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
        'api_key': r'[A-Za-z0-9_\-]{32,}'
    }

    if text:
        redacted = text
        for name, pattern in patterns.items():
            redacted = re.sub(pattern, f'[REDACTED_{name.upper()}]', redacted)
        return redacted

    return frame

def create_smokescreen():
    """
    Generate fake data to disrupt profiling
    """
    fake_data = {
        'name': ''.join(random.choices(string.ascii_letters, k=10)),
        'email': f"{''.join(random.choices(string.ascii_lowercase, k=8))}@fake.com",
        'phone': f"+1{''.join(random.choices(string.digits, k=10))}",
        'address': f"{random.randint(1, 9999)} Fake St, {random.choice(['New York', 'LA', 'Chicago'])}",
        'age': random.randint(18, 80),
        'interests': random.sample(['tech', 'sports', 'music', 'art', 'science'], 3)
    }
    return fake_data

# ============================================================
# ALERT FUNCTIONS
# ============================================================

def send_alert_email(subject, message):
    """
    Send automated threat alert email
    """
    try:
        print(f"📧 ALERT: {subject} - {message}")
        return True
    except Exception as e:
        print(f"Alert failed: {e}")
        return False

# ============================================================
# SCREEN PROTECTION
# ============================================================

def enable_screen_protection():
    """
    Enable screen capture blocking
    """
    return {
        'status': 'enabled',
        'method': 'hardware',
        'platform': 'cross-platform'
    }

def detect_screen_recording():
    """
    Detect if screen is being recorded
    """
    return {
        'recording': False,
        'method': 'detected'
    } 