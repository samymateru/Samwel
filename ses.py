import boto3

# Configure AWS SES client
ses_client = boto3.client("ses", region_name="us-east-1")

# Email details
SENDER = "samymateru1999@gmail.com"  # Must be a verified email
RECIPIENT = "bngonde@capstone.co.tz"
SUBJECT = "Test Email from Amazon SES"
BODY_TEXT = "This is a test email sent using Amazon SES via Boto3."
BODY_HTML = """<html><body><h1>Hello!</h1><p>This is a test email from Amazon SES.</p></body></html>"""

# Send email
response = ses_client.send_email(
    Source=SENDER,
    Destination={"ToAddresses": [RECIPIENT]},
    Message={
        "Subject": {"Data": SUBJECT},
        "Body": {
            "Text": {"Data": BODY_TEXT},
            "Html": {"Data": BODY_HTML}
        }
    }
)

print("Email sent! Message ID:", response["MessageId"])
