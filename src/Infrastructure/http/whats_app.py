import os
from twilio.rest import Client

# Configurações do Twilio (substitua pelas suas credenciais ou use variáveis de ambiente)
TWILIO_SID = os.getenv('TWILIO_ACCOUNT_SID', 'your_twilio_sid')
TWILIO_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', 'your_twilio_token')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')  # Número do Twilio para WhatsApp
TO_NUMBER = os.getenv('MY_PERSONAL_NUMBER', '+5511948402764')

client = Client(TWILIO_SID, TWILIO_TOKEN)

def send_activation_code(code):
    """
    Envia o código de ativação via WhatsApp usando Twilio.
    """
    try:
        message = client.messages.create(
            body=f"Seu código de ativação é: {code}",
            from_=TWILIO_WHATSAPP_NUMBER,
            to=f"whatsapp:{TO_NUMBER}" 
        )
        print(f"Código enviado para {TO_NUMBER}: {message.sid}")
    except Exception as e:
        print(f"Erro ao enviar WhatsApp: {e}", flush=True)