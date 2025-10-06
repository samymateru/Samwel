import asyncio
import os
from typing import List, Dict
from postmarker.core import PostmarkClient
from dotenv import load_dotenv

load_dotenv()

class AsyncPostmarkEmailService:
    def __init__(self):
        self.client = PostmarkClient(server_token=os.getenv("POSTMARK_API_KEY"))
        self.From = os.getenv("SYSTEM_FROM_EMAIL")



    def send_with_template(self, data: dict) -> dict:
        """
        Send an email using a Postmark template (synchronous version).

        Args:
            data (dict): {
                "to": "recipient@example.com",
                "template_model": {...},
                "template_id": "your-template-id"
            }

        Returns:
            dict: API response from Postmark.
        """
        kwargs = {
            "From": self.From,
            "To": data["to"],
            "TemplateModel": data["template_model"],
            "TemplateId": data["template_id"]
        }

        # Call the Postmark SDK synchronously
        #return self.client.emails.send_with_template(**kwargs)
        return {}



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



    def send_issue_notification(self, data: dict) -> list[dict]:
        """
        Send templated issue notification emails synchronously.
        data should include:
            - users: list of email addresses
            - TemplateModel: dict
            - TemplateId: str
        """
        results = []

        for email in data["users"]:
            try:
                res = self.client.emails.send_with_template(
                    From=self.From,
                    To=email,
                    TemplateModel=data["TemplateModel"],
                    TemplateId=data["TemplateId"],
                )
                results.append(res)
            except Exception as ex:
                results.append({"error": str(ex), "to": email})

        return results


email_service = AsyncPostmarkEmailService()
