import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- APP CONFIGURATION ---
st.set_page_config(page_title="MicroFin Track", layout="wide")

# --- CUSTOM CSS FOR MOBILE LOOK ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #007bff; color: white; }
    .card { padding: 15px; border-radius: 10px; background-color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- MOCK DATA (Simulating your Excel Sheet) ---
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame({
        'Staff': ['Nandlal', 'Dhiraj', 'Nandlal'],
        'Centre': ['Salarpur', 'Ashapur', 'Sandaha'],
        'Client': ['Kiran', 'Basanti', 'Meena'],
        'Loan_Amount': [12000, 6000, 12000],
        'Paid_So_Far': [2400, 1200, 0],
        'Last_Day_Paid': [12, 6, 0]
    })

# --- APP NAVIGATION ---
menu = ["Dashboard", "Collection", "Add Client", "Reports"]
choice = st.sidebar.selectbox("Navigation", menu)

# --- DASHBOARD ---
if choice == "Dashboard":
    st.title("Field Officer Dashboard")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Target", "₹24,000")
    with col2:
        st.metric("Collected Today", "₹4,200", delta="18%")
    
    st.subheader("Your Schedule Today")
    for centre in st.session_state.data['Centre'].unique():
        with st.expander(f"📍 Centre: {centre}"):
            st.write(f"Clients pending: {len(st.session_state.data[st.session_state.data['Centre']==centre])}")
            if st.button(f"Start {centre} Meeting"):
                st.session_state.active_centre = centre

# --- COLLECTION MODULE (The Excel Replacement) ---
elif choice == "Collection":
    st.title("Daily Collection Ledger")
    staff_filter = st.selectbox("Select Staff", ["Nandlal", "Dhiraj"])
    centre_filter = st.selectbox("Select Centre", st.session_state.data['Centre'].unique())
    
    clients = st.session_state.data[
        (st.session_state.data['Staff'] == staff_filter) & 
        (st.session_state.data['Centre'] == centre_filter)
    ]
    
    for index, row in clients.iterrows():
        st.markdown(f"""
        <div class="card">
            <strong>Client: {row['Client']}</strong><br>
            Loan: ₹{row['Loan_Amount']} | Day: {row['Last_Day_Paid']}/60<br>
            Expected Today: ₹200
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        if c1.button(f"Mark Paid (₹200)", key=f"pay_{index}"):
            st.success(f"Collected from {row['Client']}")
        if c2.button(f"No Payment", key=f"miss_{index}"):
            st.warning("Marked as Missed")

# --- REPORTS ---
elif choice == "Reports":
    st.title("Pivot Summary")
    st.write("Current Loan Status by Centre")
    pivot = st.session_state.data.pivot_table(index='Centre', values='Loan_Amount', aggfunc='sum')
    st.bar_chart(pivot)
    st.table(st.session_state.data)