import streamlit as st
import os
import io
from engine.translator import BrailleTranslator
from io_handlers.input_handler import InputHandler
from io_handlers.output_handler import OutputHandler

# ──────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Multilingual Braille Converter",
    page_icon="⠃",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# Custom CSS
# ──────────────────────────────────────────────
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .main {
        background-color: #0f1117;
    }
    .app-title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6c63ff, #48cae4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }
    .app-subtitle {
        font-size: 1.05rem;
        color: #9ca3af;
        margin-bottom: 32px;
    }
    .braille-box {
        font-family: 'Segoe UI Symbol', 'DejaVu Sans', monospace;
        font-size: 2.4rem;
        background: linear-gradient(135deg, #1e1e2e, #2a2a3e);
        color: #e0e7ff;
        padding: 28px;
        border-radius: 16px;
        border: 1px solid #3b3b5c;
        box-shadow: 0 8px 32px rgba(108,99,255,0.15);
        min-height: 160px;
        line-height: 1.4;
        word-break: break-all;
        letter-spacing: 0.1em;
    }
    .stat-card {
        background: #1e1e2e;
        padding: 16px 20px;
        border-radius: 12px;
        border: 1px solid #3b3b5c;
        text-align: center;
    }
    .stat-label {
        font-size: 0.75rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #a78bfa;
    }
    .section-label {
        font-size: 0.85rem;
        color: #6c63ff;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 10px;
    }
    .stDownloadButton > button {
        background: linear-gradient(135deg, #6c63ff, #48cae4) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 12px 20px !important;
        width: 100%;
        transition: opacity 0.2s;
    }
    .stDownloadButton > button:hover {
        opacity: 0.85 !important;
    }
    .stTextArea textarea {
        background: #1e1e2e !important;
        color: #e0e7ff !important;
        border: 1px solid #3b3b5c !important;
        border-radius: 12px !important;
        font-size: 1.05rem !important;
    }
    .stRadio label { color: #9ca3af; }
    .stFileUploader { border-radius: 12px; }
    div[data-testid="stSidebar"] {
        background-color: #1a1a2e;
    }
    </style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────
st.markdown('<p class="app-title">⠃ Multilingual Braille Converter</p>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">Convert Marathi, Hindi, and English into standardised Bharati Braille — instantly.</p>', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ About")
    st.info(
        "This engine uses a **manual, rule-based** approach based on the "
        "**Bharati Braille Standard** (NIEPVD, Govt. of India). "
        "No external Braille libraries like Liblouis are used."
    )
    st.markdown("---")
    st.markdown("**Supported Scripts**")
    st.markdown("- 🇮🇳 Devanagari (Hindi & Marathi)\n- 🔤 English (Grade 1)\n- 🔢 Numerals")
    st.markdown("---")
    st.markdown("**Conjunct Rules Active**")
    st.code("ष्ट्र → ⠯⠞⠗\nत्र  → ⠞⠗\nज्ञ  → ⠚⠒\nक्ष  → ⠅⠯", language=None)

# ──────────────────────────────────────────────
# Initialize Handlers
# ──────────────────────────────────────────────
translator = BrailleTranslator()
output_handler = OutputHandler()

# ──────────────────────────────────────────────
# Main Layout
# ──────────────────────────────────────────────
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="section-label">📥 Source Input</div>', unsafe_allow_html=True)
    input_type = st.radio(
        "Input Method", ["✏️ Manual Text", "📂 Upload PDF / TXT"],
        horizontal=True, label_visibility="collapsed"
    )

    input_text = ""
    if input_type == "✏️ Manual Text":
        input_text = st.text_area(
            "Enter text (Marathi / Hindi / English)",
            height=260,
            placeholder="Type or paste text here...\nउदाहरण: महाराष्ट्र, हिंदी, Hello World"
        )
    else:
        uploaded_file = st.file_uploader(
            "Drop a PDF or TXT file", type=["pdf", "txt"],
            label_visibility="collapsed"
        )
        if uploaded_file:
            temp_path = f"_tmp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            with st.spinner("Extracting text..."):
                input_text = InputHandler.read_file(temp_path)
            os.remove(temp_path)
            st.success(f"✅ Loaded: **{uploaded_file.name}**")
            with st.expander("Preview extracted text"):
                st.text(input_text[:2000] + ("..." if len(input_text) > 2000 else ""))

with col2:
    st.markdown('<div class="section-label">⠿ Braille Output</div>', unsafe_allow_html=True)

    if input_text and input_text.strip():
        with st.spinner("Translating..."):
            braille_output = translator.translate(input_text)

        # Stats row
        s1, s2, s3 = st.columns(3)
        with s1:
            st.markdown(f'<div class="stat-card"><div class="stat-label">Input Chars</div><div class="stat-value">{len(input_text)}</div></div>', unsafe_allow_html=True)
        with s2:
            st.markdown(f'<div class="stat-card"><div class="stat-label">Braille Cells</div><div class="stat-value">{len([c for c in braille_output if "\u2800" <= c <= "\u28ff"])}</div></div>', unsafe_allow_html=True)
        with s3:
            st.markdown(f'<div class="stat-card"><div class="stat-label">Words</div><div class="stat-value">{len(input_text.split())}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Braille Output Box
        st.markdown(f'<div class="braille-box">{braille_output}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # ── Export Options ──
        st.markdown('<div class="section-label">📤 Export Options</div>', unsafe_allow_html=True)

        # 1. Unicode Text
        st.download_button(
            label="📄 Download Unicode Braille (.txt)",
            data=braille_output.encode("utf-8"),
            file_name="braille_output.txt",
            mime="text/plain",
            use_container_width=True
        )

        # 2. Braille PDF
        pdf_buf = io.BytesIO()
        pdf_path = "_tmp_braille.pdf"
        output_handler.generate_braille_pdf(braille_output, pdf_path)
        with open(pdf_path, "rb") as pf:
            pdf_bytes = pf.read()
        os.remove(pdf_path)
        st.download_button(
            label="📁 Download Braille PDF (.pdf)",
            data=pdf_bytes,
            file_name="braille_output.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        # 3. Word DOCX
        docx_path = "_tmp_braille.docx"
        output_handler.generate_docx(braille_output, docx_path)
        with open(docx_path, "rb") as df:
            docx_bytes = df.read()
        os.remove(docx_path)
        st.download_button(
            label="📝 Download Word Document (.docx)",
            data=docx_bytes,
            file_name="braille_output.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )

    else:
        st.markdown(
            '<div class="braille-box" style="display:flex;align-items:center;justify-content:center;'
            'font-size:1rem;color:#4b5563;">Enter text or upload a file on the left to see the Braille translation.</div>',
            unsafe_allow_html=True
        )

st.markdown("---")
st.caption("Built for accessibility · Rule-based Bharati Braille Engine · Marathi · Hindi · English")
