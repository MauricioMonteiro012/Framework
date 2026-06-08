import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

class WhatsApp:

    @staticmethod
    def whats_app(code):
        # Puxa as credenciais corretas que o Docker Compose está injetando
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_ = os.getenv("TWILIO_WHATSAPP_NUMBER")
        
        # Puxa o seu número fixo configurado no docker-compose (MY_PERSONAL_NUMBER)
        # Se por acaso não achar no ambiente, usa a string do seu número como garantia
        my_number = os.getenv("MY_PERSONAL_NUMBER", "+5511948402764")

        # Garante que o formato final seja 'whatsapp:+5511948402764' como o Twilio exige
        if my_number and not my_number.startswith("whatsapp:"):
            to_whatsapp = f"whatsapp:{my_number}"
        else:
            to_whatsapp = my_number

        client = Client(account_sid, auth_token)

        client.messages.create(
            body=f"Seu código de ativação é: {code}",
            from_=from_,        # 'whatsapp:+14155238886' (Sandbox)
            to=to_whatsapp      # Sempre enviará para o seu celular!
        )