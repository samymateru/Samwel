from email.message import EmailMessage
import asyncio
from aiosmtplib import SMTP

# Email config
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = "samymateru1999@gmail.com"
SENDER_PASSWORD = "eqdi kxuv vwmq fnth"  # App password

# Shared async queue
email_queue = asyncio.Queue()


# --- Email Worker ---
async def smtp_worker():
    smtp = SMTP(hostname=SMTP_SERVER, port=SMTP_PORT, use_tls=True)
    await smtp.connect()
    await smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
    print("✅ SMTP connected.")

    try:
        while True:
            email_data = await email_queue.get()

            msg = EmailMessage()
            msg['From'] = SENDER_EMAIL
            msg['To'] = email_data["to"]
            msg['Subject'] = email_data["subject"]
            msg.set_content(email_data["body"])

            try:
                await smtp.send_message(msg)
                print(f"✅ Email sent to {email_data['to']}")
            except Exception as e:
                print(f"❌ Failed to send to {email_data['to']}: {e}")

            await asyncio.sleep(1)
            email_queue.task_done()
    finally:
        await smtp.quit()
