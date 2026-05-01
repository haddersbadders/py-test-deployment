import streamlit as st
import gspread
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file if running locally
load_dotenv()

st.set_page_config(page_title="Dashboard Tester", layout="wide")

st.title("📊 Google Sheets Dashboard Tester")

@st.cache_resource
def get_gspread_client():
    """Authenticates with Google using environment variables."""
    try:
        project_id = os.environ.get("GCP_PROJECT_ID")
        
        # Robustly parse the private key
        private_key = os.environ.get("GCP_PRIVATE_KEY", "")
        if private_key.startswith('"') and private_key.endswith('"'):
            private_key = private_key[1:-1]
        elif private_key.startswith("'") and private_key.endswith("'"):
            private_key = private_key[1:-1]
            
        # Replace literal \n with actual newlines
        private_key = private_key.replace("\\n", "\n")

        credentials_dict = {
            "type": "service_account",
            "project_id": project_id,
            "private_key_id": os.environ.get("GCP_PRIVATE_KEY_ID"),
            "private_key": private_key,
            "client_email": os.environ.get("GCP_CLIENT_EMAIL"),
            "client_id": os.environ.get("GCP_CLIENT_ID"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": os.environ.get("GCP_CLIENT_X509_CERT_URL"),
            "universe_domain": "googleapis.com"
        }
        gc = gspread.service_account_from_dict(credentials_dict)
        return gc
    except Exception as e:
        st.error(f"Error authenticating with Google: {e}")
        st.info("Make sure all GCP_* environment variables are set correctly in your .env file.")
        return None

@st.cache_data(ttl=600)
def load_data():
    """Loads data from the configured Google Sheet."""
    gc = get_gspread_client()
    if not gc:
        return None
    
    sheet_url = os.environ.get("SPREADSHEET_URL")
    if not sheet_url:
        st.error("SPREADSHEET_URL environment variable is not set.")
        return None
        
    try:
        sh = gc.open_by_url(sheet_url)
        worksheet = sh.sheet1
        records = worksheet.get_all_records()
        return pd.DataFrame(records)
    except Exception as e:
        st.error(f"Error reading Google Sheet: {e}")
        st.info("Make sure the Service Account email has been added as a Viewer to the Google Sheet.")
        return None

# Sidebar controls
st.sidebar.header("Controls")
if st.sidebar.button("🔄 Refresh Data"):
    load_data.clear()
    st.success("Data cache cleared! Rerunning...")

# Load data
with st.spinner("Loading data from Google Sheets..."):
    df = load_data()

# Main area
if df is not None:
    if df.empty:
        st.warning("The connected Google Sheet is empty.")
    else:
        # Simple interactive element: Text filter
        search_query = st.text_input("🔍 Search data across all columns:")
        
        if search_query:
            # Filter the dataframe based on search query
            mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False, na=False).any(), axis=1)
            filtered_df = df[mask]
        else:
            filtered_df = df
            
        st.write(f"Showing {len(filtered_df)} of {len(df)} rows:")
        st.dataframe(filtered_df, use_container_width=True)
else:
    st.warning("Could not load data. Please check your configuration.")
