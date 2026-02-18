import streamlit as st
import pandas as pd
import openpyxl

# --- CONFIG ---
st.set_page_config(page_title="Sandaha Microfinance", layout="wide")

FILE_NAME = "Backup2 file Sandaha detail.xlsx"

@st.cache_data
def load_data():
    return pd.read_excel(FILE_NAME, sheet_name="Sheet1")

def save_data(dataframe):
    dataframe.to_excel(FILE_NAME, sheet_name="Sheet1", index=False)
    st.sidebar.success("✅ Excel File Updated!")

try:
    # Load data into session state so it stays updated during the session
    if 'df' not in st.session_state:
        st.session_state.df = load_data()

    st.sidebar.title("App Menu")
    page = st.sidebar.radio("Navigate", ["Collection Ledger", "Analytics"])

    if page == "Collection Ledger":
        st.title("💸 Field Collection")
        
        # 1. Staff & Centre Selection
        staff = st.selectbox("Staff Name", st.session_state.df['Staff'].unique())
        centres = st.session_state.df[st.session_state.df['Staff'] == staff]['Centre'].unique()
        centre = st.selectbox("Select Centre", centres)

        # 2. Show Clients
        mask = (st.session_state.df['Staff'] == staff) & (st.session_state.df['Centre'] == centre)
        clients_idx = st.session_state.df[mask].index

        for idx in clients_idx:
            client = st.session_state.df.loc[idx]
            # Identify which 'Day' column to fill based on 'Pending Period Days'
            current_day_col = f"Day {int(client['Pending Period Days'])}"
            
            with st.expander(f"👤 {client['Client Name ']} (Day {int(client['Pending Period Days'])})"):
                amt = st.