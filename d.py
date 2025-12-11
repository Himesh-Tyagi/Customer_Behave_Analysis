

import streamlit as st
from pathlib import Path
import pandas as pd
import base64

st.set_page_config(page_title="Customer Behaviour Analysis Project", layout="wide")

# --- CONFIG: your existing paths & Power BI link (Option A) ---
POWER_BI_URL = "https://app.powerbi.com/view?r=eyJrIjoiNDNmZTJhNzQtNzkxNS00ODBjLTk1YmEtNDY4NjEwYTEwZTE3IiwidCI6IjFiMmQ3ZTFlLTEyOWQtNDMxYS1hY2U3LWE2YzdmZmU0MTg5ZSJ9"

IMG1 = "C:/Users/DELL PC/OneDrive/Pictures/Screenshots/Screenshot 2025-12-06 113328.png"
IMG2 = "C:/Users/DELL PC/Music/project/Screenshot 2025-12-06 104433.png"

PDF_PATH = "C:/Users/DELL PC/Music/Customer Behave Dashboard.pdf"
PPTX_PATH = "C:/Users/DELL PC/Downloads/Customer-Shopping-Behavior-Analysis.pptx"
EXCEL_PATH = "C:/Users/DELL PC/Music/updated_file.xlsx"
PYTHON_PATH = "C:/Users/DELL PC/Music/Project.ipynb"  # will display raw JSON/text
SQL_PATH = "C:/Users/DELL PC/Music/SQL/Customer_Purchase.sql"

# --- Utilities ---
def exists(path):
    return Path(path).exists()

def load_bytes(path):
    try:
        return Path(path).read_bytes()
    except Exception:
        return None

def read_text(path):
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None

def render_pdf_bytes(pdf_bytes, height=700):
    if not pdf_bytes:
        st.error("No PDF bytes to render.")
        return
    b64 = base64.b64encode(pdf_bytes).decode("utf-8")
    pdf_display = f"<embed src='data:application/pdf;base64,{b64}' width='100%' height='{height}' type='application/pdf'>"
    st.components.v1.html(pdf_display, height=height, scrolling=True)

# Navigation
if "page" not in st.session_state:
    st.session_state.page = "home"

def home_page():
    st.title("📊 Customer Behaviour Analysis Project")
    st.markdown("A comprehensive analysis of customer behaviour and purchasing trends.")
    st.subheader("Summary :-")
    st.write("This project analyzes customer behaviour using real-world shopping data, focusing on spending patterns, purchase frequency, and product preferences. It identifies key trends that influence customer decisions and overall shopping habits. The insights generated help businesses improve strategies, enhance customer targeting, and boost performance.")

    col1, col2 = st.columns([2,1])
    with col1:
        st.write("")
    with col2:
        if exists(IMG1):
            st.image(IMG1, caption="Project DashBoard Page 1", width=300)
            st.download_button("Download Image ", load_bytes(IMG1), file_name=Path(IMG1).name)
        else:
            st.info("Image 1 not found at configured path.")

    st.write("---")
    st.subheader("Dataset Image")
    if exists(IMG2):
        st.image(IMG2, caption="Dataset snapshot", width=220)
        st.download_button("Download Image", load_bytes(IMG2), file_name=Path(IMG2).name)
    else:
        st.info("Snapshot image not found at configured path.")

    st.write("---")
    if st.button("➡ Go to Resources Page", use_container_width=True):
        st.session_state.page = "resources"
        st.rerun()

def resources_page():
    st.title("📁 Project Resources Center")
    st.write("Click **View** to preview in the app, or **Download** to save the file locally.")

    # Layout with cards
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Dashboards & Reports")
        # Power BI (open in new tab)
        st.markdown("**Power BI Dashboard**")
        st.write("Open the live Power BI dashboard in a new tab.")
        if st.button("Open Power BI Dashboard (new tab)"):
            st.markdown(f"[Open Power BI Dashboard]({POWER_BI_URL})", unsafe_allow_html=True)

        st.write("")

        # PDF: view + download
        st.markdown("**PDF Report**")
        if exists(PDF_PATH):
            pdf_bytes = load_bytes(PDF_PATH)
            if st.button("View PDF Report"):
                render_pdf_bytes(pdf_bytes, height=750)
            st.download_button("Download PDF Report", pdf_bytes, file_name=Path(PDF_PATH).name)
        else:
            st.info("PDF not found at configured path.")

        st.write("")
        st.markdown("**Presentation (PPTX)**")
        if exists(PPTX_PATH):
            pptx_bytes = load_bytes(PPTX_PATH)
            st.write("Preview PPTX inside Streamlit is not built-in. Use Download to get the file.")
            st.download_button("Download PPTX", pptx_bytes, file_name=Path(PPTX_PATH).name)
        else:
            st.info("PPTX not found at configured path.")

    with col_right:
        st.subheader("Data & Code Files")
        # Excel: view + download
        st.markdown("**Excel Dataset**")
        if exists(EXCEL_PATH):
            if st.button("View Excel (table)"):
                try:
                    df = pd.read_excel(EXCEL_PATH)
                    st.dataframe(df, use_container_width=True)
                except Exception as e:
                    st.error(f"Error reading Excel: {e}")
            excel_bytes = load_bytes(EXCEL_PATH)
            st.download_button("Download Excel", excel_bytes, file_name=Path(EXCEL_PATH).name)
        else:
            st.info("Excel file not found at configured path.")

        st.write("")
        # Python code (notebook) view + download
        st.markdown("**Python / Notebook**")
        if exists(PYTHON_PATH):
            if st.button("View Python/Notebook (raw)"):
                txt = read_text(PYTHON_PATH)
                if txt:
                    st.code(txt[:100000], language="json")  # display up to first 100k chars
                else:
                    st.error("Could not read file.")
            py_bytes = load_bytes(PYTHON_PATH)
            st.download_button("Download Notebook / Code", py_bytes, file_name=Path(PYTHON_PATH).name)
        else:
            st.info("Python file not found at configured path.")

        st.write("")
        # SQL view + download
        st.markdown("**SQL Query**")
        if exists(SQL_PATH):
            if st.button("View SQL Query"):
                sql_txt = read_text(SQL_PATH)
                if sql_txt:
                    st.code(sql_txt, language="sql")
                else:
                    st.error("Could not read SQL file.")
            sql_bytes = load_bytes(SQL_PATH)
            st.download_button("Download SQL", sql_bytes, file_name=Path(SQL_PATH).name)
        else:
            st.info("SQL file not found at configured path.")

    st.write("---")
    if st.button("⬅ Back to Home Page", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()

# Router
if st.session_state.page == "home":
    home_page()
else:
    resources_page()

    
