import os
import telebot
import google.generativeai as genai
from PIL import Image

# API ve Bot Ayarları
TELEGRAM_TOKEN = '8674530415:AAFUW9TCaH2VlmsiSAup4qeS10t2V8vvtsM'
GEMINI_API_KEY = 'AQ.Ab8RN6J1MqFzpQJCJMJyNhKToME0T5CFM39oqoATu4I5wu96Rg'

genai.configure(api_key=GEMINI_API_KEY)
bot = telebot.TeleBot(TELEGRAM_TOKEN)

def send_long_message(chat_id, text, max_length=3000):
    for i in range(0, len(text), max_length):
        bot.send_message(chat_id, text[i:i+max_length])

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message, 
        "⚽ Merhaba Fatih!\n\n"
        "Canlı maç analiz botuna hoş geldin. Maç esnasında aldığın İSTATİSTİK EKRAN GÖRÜNTÜSÜNÜ bana fotoğraf olarak gönder, anında objektif ve mantıklı analiz çıkarayım!"
    )

@bot.message_handler(content_types=['photo'])
def handle_photo_analysis(message):
    bot.reply_to(message, "📊 Ekran görüntüsü inceleniyor, istatistikler rasyonel olarak analiz ediliyor...")
    
    photo_path = "temp_match_stats.jpg"
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        with open(photo_path, 'wb') as new_file:
            new_file.write(downloaded_file)
            
        img = Image.open(photo_path)

        prompt = """
        Sen disiplinli, objektif ve matematiğe dayalı çalışan profesyonel bir canlı maç ve korner analistisin.
        Görseldeki maç istatistik ekranını (SofaScore / FlashScore vb.) dikkatlice oku.

        ÇOK ÖNEMLİ KURALLAR:
        - ASLA HAYAL SATMA VE TEMELSİZ TAHMİNLERDE BULUNMA.
        - Eğer maç kısır geçiyorsa, hücum temposu düşükse veya şut/pas sayıları yetersizse açıkça "Maçta korner veya gol potansiyeli DÜŞÜK, riske girmeyin" de.
        - Sadece ve sadece görseldeki SAYISAL VERİLERE (ceza sahası içi şutlar, engellenen şutlar, kilit paslar, topa sahip olma, kornerler) dayanarak mantıklı sonuç çıkar.

        Lütfen şu başlıklarda net ve objektif bir rapor hazırla:

        1. MAÇIN MEVCUT DURUMU:
           - Takımlar, Skor, Maçın Dakikası / Devresi.

        2. VERİYE DAYALI SAHA GERÇEĞİ:
           - Şut kalitesi (Ceza sahası içi/dışı, engellenen şutlar), kilit paslar ve baskı durumuna göre sahada gerçekten ne oluyor? Hangi takım somut baskı kuruyor?

        3. RASYONEL KORNER VE TEMPO DEĞERLENDİRMESİ:
           - Mevcut korner sayısı ve takımların kanat/ceza sahası zorlama verilerine göre maçta korner temposu var mı yoksa maç kilit mi?

        4. EN MANTIKLI VE GERÇEKÇİ TAHMİN:
           - En Yüksek İhtimalli Bahis/Tavsiye (Risk durumuna göre: Pas Geç, Alt, Üst veya Taraf Korneri)
           - Gerçekçi Güven Oranı (%) ve Matematiksel Mantığı

        Not: Özel karakterler (*, _, #) kullanma, sade ve anlaşılır Türkçe yaz.
        """

        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([prompt, img])

        send_long_message(message.chat.id, response.text)

    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Görsel analiz edilirken bir hata oluştu: {str(e)}")
    finally:
        if os.path.exists(photo_path):
            os.remove(photo_path)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    bot.reply_to(message, "📸 Lütfen analizi yapılacak canlı maçın İSTATİSTİK EKRAN GÖRÜNTÜSÜNÜ (fotoğraf olarak) gönderin!")

if __name__ == '__main__':
    print("Bot basariyla baslatildi...")
    bot.infinity_polling()
  
