# SolvIT - NLP IT Helpdesk Telegram Bot

Proyek ini adalah sistem chatbot berbasis **Natural Language Processing (NLP)** yang dirancang untuk menyelesaikan masalah IT Helpdesk secara otomatis melalui platform Telegram. Bot ini menggunakan pendekatan *Machine Learning* (TF-IDF & Multinomial Naive Bayes) dan diintegrasikan dengan Generative AI (Google Gemini 2.5 Flash) menggunakan arsitektur **Retrieval-Augmented Generation (RAG)** untuk memberikan jawaban yang natural, ramah, dan profesional.

## Fitur Utama
1. **Klasifikasi Intent:** Mendeteksi niat atau tipe masalah pengguna (misal: *Network Issue*, *Hardware Error*, *Greeting*) menggunakan model `MultinomialNB`.
2. **Pencarian Solusi (Cosine Similarity):** Mencari solusi paling relevan dari *database* (CSV) berdasarkan perhitungan kemiripan TF-IDF.
3. **Integrasi LLM (Gemini RAG):** Alih-alih memberikan teks baku dari database, bot mengirimkan konteks masalah ke Google Gemini untuk diproses ulang menjadi jawaban yang sangat luwes dan berempati.
4. **Out-of-Domain Guardrail:** Bot telah dilindungi oleh *prompting system* ketat agar **menolak** menjawab pertanyaan di luar topik IT (seperti politik, resep masakan, dll).
5. **Smart Fallback:** Jika pengguna menanyakan masalah IT yang tidak ada di dalam *database* lokal, Gemini akan menggunakan pengetahuannya sebagai "Asisten IT" untuk tetap memberikan panduan umum yang bermanfaat.

## Struktur Direktori
* `bot.py` : Skrip utama aplikasi Telegram Bot.
* `dataset_ithelpdesk_final.csv` : Dataset berisi berbagai permasalahan IT dan solusi bakunya.
* `vectorizer.pkl` & `tfidf_matrix.pkl` : Model TF-IDF yang telah dilatih untuk ekstraksi fitur teks.
* `intent_classifier.pkl` : Model klasifikasi berbasis *Naive Bayes*.
* `Pelatihan_NLP_solvitbot_.ipynb` : *Jupyter Notebook / Google Colab* berisi proses prapemrosesan data, pelatihan model, dan evaluasi.

## Prasyarat & Instalasi
Pastikan Anda menggunakan Python versi 3.9 atau lebih baru.
1. Clone repositori ini:
   ```bash
   git clone [URL_GITHUB_ANDA]
   cd SolvIT_Bot_NLP
   ```
2. Install semua dependensi yang dibutuhkan:
   ```bash
   pip install -r requirements.txt
   ```

## Konfigurasi
Sebelum menjalankan bot, Anda harus mengubah kredensial di dalam file `bot.py`:
1. `TOKEN`: Ganti dengan Token Bot Telegram Anda (didapatkan dari [@BotFather](https://t.me/botfather)).
2. `GEMINI_API_KEY`: Ganti dengan API Key Google Gemini Anda (didapatkan dari [Google AI Studio](https://aistudio.google.com/)).

## Cara Menjalankan Aplikasi
Buka terminal/CMD di dalam folder project, lalu jalankan perintah:
```bash
python bot.py
```
Setelah muncul tulisan `Bot SolvIT Berjalan`, Anda bisa membuka aplikasi Telegram, mencari bot Anda, dan mulai berinteraksi (contoh: *"Halo min, wifi di lantai 2 putus terus solusinya gimana ya?"*).

---
*Proyek ini dikembangkan untuk memenuhi Ujian Akhir Semester Mata Kuliah Natural Language Processing.*
