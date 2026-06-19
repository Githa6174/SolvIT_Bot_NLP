import streamlit as st
from nlp_engine import cari_solusi
import time

st.set_page_config(page_title="SolvIT AI Helpdesk", page_icon="🤖", layout="centered")

st.title("🤖 SolvIT AI Helpdesk")
st.caption("Asisten IT Cerdas Anda yang siap membantu masalah teknis 24/7.")

# Inisialisasi history chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Pesan pembuka dari AI
    st.session_state.messages.append({"role": "assistant", "content": "Halo! Saya AI Helpdesk SolvIT. 🤖\nSilakan ketik kendala IT Anda (contoh: 'internet mati' atau 'layar laptop biru')."})

# Tampilkan history chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Hapus tag HTML <b> dan <i> karena Streamlit menggunakan Markdown
        # nlp_engine memproduksi HTML untuk Telegram. Kita replace basic HTML to Markdown
        content = message["content"]
        content = content.replace("<b>", "**").replace("</b>", "**")
        content = content.replace("<i>", "*").replace("</i>", "*")
        st.markdown(content)

# Input user
if prompt := st.chat_input("Ketik kendala IT Anda di sini..."):
    # Tampilkan input user di layar
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Tampilkan loading AI sedang berpikir
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("⏳ AI sedang menganalisis masalah Anda...")
        
        # Panggil logika NLP
        try:
            jawaban = cari_solusi(prompt)
            # Konversi HTML bot Telegram ke Markdown Streamlit
            jawaban = jawaban.replace("<b>", "**").replace("</b>", "**")
            jawaban = jawaban.replace("<i>", "*").replace("</i>", "*")
            
            message_placeholder.markdown(jawaban)
            st.session_state.messages.append({"role": "assistant", "content": jawaban})
        except Exception as e:
            error_msg = f"Mohon maaf, terjadi kesalahan sistem: {e}"
            message_placeholder.markdown(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
