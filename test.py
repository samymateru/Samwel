import smtplib
from email.message import EmailMessage

# Email details
sender_email = "samymateru1999@gmail.com"
receiver_email = "swaicatherine26@gmail.com"
subject = "Hello from Python!"
body = "Punguza umbea binti"

# Create the email
email = EmailMessage()
email['From'] = sender_email
email['To'] = receiver_email
email['Subject'] = subject
email.set_content(body)

# Send the email
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, "eqdi kxuv vwmq fnth")  # Replace with your password
        smtp.send_message(email)
        print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
