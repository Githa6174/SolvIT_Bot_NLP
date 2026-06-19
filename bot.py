import telebot
import os
from dotenv import load_dotenv
from nlp_engine import cari_solusi

# Memuat variabel lingkungan dari file .env
load_dotenv()

# --- KONFIGURASI BOT ---
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN tidak ditemukan. Harap isi di file .env!")
bot = telebot.TeleBot(TOKEN)

# --- ROUTING PESAN TELEGRAM ---
@bot.message_handler(commands=['start', 'help'])
def kirim_salam(message):
    pesan_salam = "Halo! Saya AI Helpdesk SolvIT. 🤖\nSilakan ketik kendala IT Anda (contoh: 'internet mati' atau 'layar laptop biru')."
    bot.reply_to(message, pesan_salam)

@bot.message_handler(func=lambda message: True)
def respon_keluhan(message):
    bot.reply_to(message, "⏳ AI sedang menganalisis masalah Anda...")
    jawaban = cari_solusi(message.text)
    bot.send_message(message.chat.id, jawaban, parse_mode="HTML")

# --- MENJALANKAN BOT ---
if __name__ == "__main__":
    print("✅ Bot SolvIT Berjalan. Silakan buka Telegram dan uji coba chat dengan bot Anda!")
    bot.infinity_polling()