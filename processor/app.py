import os
import requests
import threading
from flask import Flask, request
from pypdf import PdfReader
from io import BytesIO

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
OLLAMA_URL = "http://ollama:11434/api/generate"

def process_pdf_background(file_id, chat_id, webhook_url):
    try:
        # 1. Telegram'dan dosya yolunu al
        file_info_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getFile?file_id={file_id}"
        file_info = requests.get(file_info_url).json()
        file_path = file_info['result']['file_path']

        # 2. PDF'i indir
        download_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"
        pdf_response = requests.get(download_url)
        
        # 3. Metni çıkar
        pdf_file = BytesIO(pdf_response.content)
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"

        # Çok uzun PDF'leri sınırla (Ollama bellek taşmasını önlemek için ilk 10.000 karakter)
        text = text[:10000]

        # 4. Ollama'ya özetlet (llama3 modelini kullanıyoruz)
        prompt = f"Lütfen aşağıdaki metnin ana fikrini ve önemli noktalarını Türkçe olarak özetle:\n\n{text}"
        ollama_payload = {
            "model": "qwen2:0.5b",
            "prompt": prompt,
            "stream": False
        }
        ollama_res = requests.post(OLLAMA_URL, json=ollama_payload).json()
        summary = ollama_res.get('response', 'Özet çıkarılırken bir hata oluştu.')

    except Exception as e:
        summary = f"Bir hata oluştu: {str(e)}"

    # 5. Sonucu Huginn'e geri gönder
    huginn_payload = {
        "chat_id": chat_id,
        "summary": summary
    }
    requests.post(webhook_url, json=huginn_payload)

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    file_id = data.get('file_id')
    chat_id = data.get('chat_id')
    webhook_url = data.get('webhook_url')

    if not file_id or not webhook_url:
        return "Eksik parametre", 400

    # İşlemi arka planda başlat ve Huginn'e hemen "Aldım" yanıtı dön
    threading.Thread(target=process_pdf_background, args=(file_id, chat_id, webhook_url)).start()
    return "İşlem başlatıldı", 202

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)