import pandas as pd
import pickle
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.metrics.pairwise import cosine_similarity
from google import genai
import os
from dotenv import load_dotenv

# Memuat variabel lingkungan dari file .env
load_dotenv()

# Konfigurasi Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY tidak ditemukan. Harap isi di file .env!")
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# --- MUAT MODEL & DATASET ---
print("Memuat Otak AI (Model & Dataset)...")
df = pd.read_csv("dataset_ithelpdesk_final.csv")

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)
with open("tfidf_matrix.pkl", "rb") as f:
    tfidf_matrix = pickle.load(f)
with open("intent_classifier.pkl", "rb") as f:
    clf = pickle.load(f)

# Siapkan Sastrawi untuk memproses chat dari user
factory = StemmerFactory()
stemmer = factory.create_stemmer()

def bersihkan_teks(teks):
    teks = str(teks).lower()
    teks = re.sub(r'[^\w\s]', '', teks)
    words = teks.split()
    return ' '.join([stemmer.stem(word) for word in words])

# --- LOGIKA PENCARIAN SOLUSI ---
def generate_jawaban_gemini(chat_user, intent_formatted, pertanyaan_terkait, solusi_baku):
    prompt = f"""Anda adalah AI IT Helpdesk bernama SolvIT.
Pengguna bertanya: "{chat_user}"

Referensi Solusi dari Database:
- Tipe Masalah: {intent_formatted}
- Pertanyaan Mirip: "{pertanyaan_terkait}"
- Solusi Baku: "{solusi_baku}"

Tugas Anda: Jawablah pertanyaan pengguna dengan ramah, natural, empati, dan profesional. Gunakan referensi solusi baku di atas sebagai acuan utama, tapi jabarkan dan perhalus bahasanya (jangan terlihat kaku). 
PENTING: Anda HANYA boleh menjawab pertanyaan seputar masalah IT (komputer, jaringan, software, hardware, dll) atau sapaan ramah. Jika pertanyaan pengguna SAMA SEKALI BUKAN TENTANG IT (misal: politik, resep masakan, dll), tolak dengan sopan dan ingatkan bahwa Anda adalah Asisten IT Helpdesk. Format teks Anda dengan HTML tags dasar Telegram (<b> untuk tebal, <i> untuk miring, <code> untuk command/perintah). Jika digunakan di web, Markdown standar seperti **tebal** dan *miring* juga diperbolehkan."""
    try:
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"⚙️ <b>Tipe Masalah:</b> {intent_formatted}\n\n🛠️ <b>Solusi AI:</b>\n{solusi_baku}\n\n<i>(Pesan ini dari fallback lokal karena Gemini Timeout: {str(e)})</i>"

def fallback_gemini(chat_user):
    prompt = f"""Anda adalah AI IT Helpdesk bernama SolvIT. Pengguna mengetik: "{chat_user}". 
Sistem kami belum menemukan kecocokan persis di database lokal. 
Tugas Anda: Respons pengguna ini layaknya ahli IT Helpdesk profesional yang ramah. Jika ini sapaan, sapa balik. Jika ini pertanyaan IT, berikan solusi umum atau panduan penyelesaian masalah. 
PENTING: Jika pengguna menanyakan hal yang SAMA SEKALI TIDAK ADA HUBUNGANNYA dengan dunia IT (misalnya resep makanan, film, sejarah, curhat pribadi, politik), Anda WAJIB MENOLAK menjawabnya dengan sopan. Beri tahu mereka bahwa Anda diciptakan khusus hanya untuk membantu masalah teknis IT.
Format dengan HTML atau Markdown."""
    try:
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return "Mohon maaf, AI SolvIT saat ini belum menemukan solusi spesifik dan server fallback sedang sibuk. Harap hubungi teknisi secara langsung."

def cari_solusi(chat_user):
    chat_bersih = bersihkan_teks(chat_user)
    vektor_user = vectorizer.transform([chat_bersih])
    
    prediksi_intent = clf.predict(vektor_user)[0]
    intent_formatted = str(prediksi_intent).replace('_', ' ').title()
    
    skor_kemiripan = cosine_similarity(vektor_user, tfidf_matrix)[0]
    indeks_sesuai_intent = df.index[df['intent'] == prediksi_intent].tolist()
    
    indeks_terbaik = -1
    skor_tertinggi = 0.0
    
    if len(indeks_sesuai_intent) > 0:
        for idx in indeks_sesuai_intent:
            if skor_kemiripan[idx] > skor_tertinggi:
                skor_tertinggi = skor_kemiripan[idx]
                indeks_terbaik = idx
    else:
        indeks_terbaik = skor_kemiripan.argmax()
        skor_tertinggi = skor_kemiripan[indeks_terbaik]
    
    if skor_tertinggi < 0.15:
        return fallback_gemini(chat_user)
    
    pertanyaan_terkait = df['pertanyaan'].iloc[indeks_terbaik]
    kategori = df['kategori'].iloc[indeks_terbaik]
    solusi = df['solusi'].iloc[indeks_terbaik]
    
    jawaban = generate_jawaban_gemini(chat_user, intent_formatted, pertanyaan_terkait, solusi)
    return jawaban
