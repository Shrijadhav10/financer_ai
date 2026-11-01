import os

import streamlit as st


def get_secret(name):
    value = os.getenv(name)
    if value:
        return value

    try:
        return st.secrets[name]
    except (KeyError, FileNotFoundError):
        return None


def get_secret_section(name):
    try:
        return st.secrets[name]
    except (KeyError, FileNotFoundError):
        return None
