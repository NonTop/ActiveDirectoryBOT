import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)

async def send_confirmation_email(recipient: str, code: str) -> bool:
    """Отправляет email с кодом подтверждения"""
    try:
        SMTP_SERVER = "smtp.office365.com"
        SMTP_PORT = 587
        SMTP_USER = "name_account"  # Изменить на свой
        SMTP_PASSWORD = "password"  # Изменить на свой

        msg = MIMEMultipart()
        msg["Subject"] = "Код подтверждения"
        msg["From"] = SMTP_USER
        msg["To"] = recipient

        body = f"""
        Ваш код подтверждения: {code}
        Код действителен в течение 10 минут.
        """
        msg.attach(MIMEText(body, "plain", "utf-8"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)

        logger.info(f"Письмо отправлено: {recipient}")
        return True

    except smtplib.SMTPAuthenticationError:
        logger.error("Ошибка аутентификации: неверные учетные данные")
    except Exception as e:
        logger.error(f"Ошибка отправки: {str(e)}")

    return False