import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)


async def send_confirmation_email(recipient: str, code: str, smtp_config: dict):
    """Отправляет email с кодом подтверждения"""
    msg = MIMEMultipart()
    msg["Subject"] = "Код подтверждения"
    msg["From"] = smtp_config['SMTP_USER']
    msg["To"] = recipient

    msg.attach(MIMEText(f"Ваш код подтверждения: {code}", "plain", "utf-8"))

    try:
        with smtplib.SMTP(smtp_config['SMTP_SERVER'], smtp_config['SMTP_PORT']) as server:
            server.starttls()
            server.login(smtp_config['SMTP_USER'], smtp_config['SMTP_PASSWORD'])
            server.sendmail(smtp_config['SMTP_USER'], recipient, msg.as_string())
        return True
    except Exception as e:
        logger.error(f"SMTP error: {e}")
        return False