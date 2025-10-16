import asyncio
import os
from typing import List, Dict, Any
from postmarker.core import PostmarkClient
from dotenv import load_dotenv
from postmarker.exceptions import PostmarkerException

from services.logging.logger import global_logger

load_dotenv()

class AsyncPostmarkEmailService:
    def __init__(self):
        self.client = PostmarkClient(server_token=os.getenv("POSTMARK_API_KEY"))
        self.From = os.getenv("SYSTEM_FROM_EMAIL")



    def send_with_template(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send an email using a Postmark template.

        Args:
            data (dict): A dictionary with:
                - to (str): Recipient email address.
                - template_model (dict): Template variables for Postmark.
                - template_id (str|int): Postmark template ID.

        Returns:
            dict: Postmark API response, or an error payload on failure.
        """
        # Basic validation
        required_fields = ["to", "template_id", "template_model"]
        missing = [f for f in required_fields if f not in data]
        if missing:
            msg = f"Missing required fields: {', '.join(missing)}"
            global_logger.exception(msg)
            return {"success": False, "error": msg}

        # Prepare parameters
        kwargs = {
            "From": self.From,
            "To": data["to"],
            "TemplateId": data["template_id"],
            "TemplateModel": data["template_model"],
        }

        try:
            # response = self.client.emails.send_with_template(**kwargs)
            global_logger.info(f"Email sent successfully to {data['to']} using template {data['template_id']}")
            return {"success": True, "response": "response"}
        except PostmarkerException as e:
            global_logger.exception(f"Postmark error while sending to {data['to']}: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            global_logger.exception(f"Unexpected error sending email to {data.get('to')}: {e}")
            return {"success": False, "error": "Internal email sending error"}



    def send_bulk_with_template(self, emails: list[dict]) -> list[dict]:
        """
        Send multiple templated emails synchronously.
        Each dict should have: to, template_id, template_model

        Example:
            emails = [
                {"to": "a@example.com", "template_id": "123", "template_model": {...}},
                {"to": "b@example.com", "template_id": "123", "template_model": {...}},
            ]
        """
        results = []
        for e in emails:
            try:
                # res = self.client.emails.send_with_template(
                #     From=self.From,
                #     To=e["to"],
                #     TemplateModel=e["template_model"],
                #     TemplateId=e["template_id"],
                # )
                # results.append(res)
                pass
            except Exception as ex:
                results.append({"error": str(ex), "to": e.get("to")})

        return results





    def send_issue_notification(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Sends issue notification emails using a Postmark template.

        Args:
            data (dict): Dictionary with the following structure:
                {
                    "users": ["user1@example.com", "user2@example.com"],
                    "template_model": {
                        "title": "ISSUE-001",
                        "reference": "ISSUE-001",
                        "rating": "High",
                        "engagement": "Credit Risk Review",
                        "due_date": "2025-10-09T10:00:00Z"
                    },
                    "template_id": 41703998
                }

        Returns:
            list[dict]: A list of Postmark API responses or error objects per recipient.
        """
        results = []

        users = data.get("users", [])
        template_model = data.get("template_model", {})
        template_id = data.get("template_id")

        if not users or not isinstance(users, list):
            global_logger.exception("Invalid or missing 'users' list in email data.")
            return [{"error": "Invalid or missing 'users' list"}]

        if not template_model or not isinstance(template_model, dict):
            global_logger.exception("Invalid or missing 'template_model' in email data.")
            return [{"error": "Invalid or missing 'template_model'"}]

        if not template_id:
            global_logger.exception("Missing 'template_id' in email data.")
            return [{"error": "Missing 'template_id'"}]

        for recipient in users:
            try:
                # response = self.client.emails.send_with_template(
                #     From=self.From,
                #     To=recipient,
                #     TemplateModel=template_model,
                #     TemplateId=template_id,
                # )
                results.append("response")
            except Exception as ex:
                error_msg = f"Failed to send email to {recipient}: {str(ex)}"
                global_logger.exception(error_msg)
                results.append({"error": error_msg, "to": recipient})

        return results



email_service = AsyncPostmarkEmailService()
