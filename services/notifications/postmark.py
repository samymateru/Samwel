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


    async def send_with_template(self, data: Dict) -> dict:
        """Send an email using a Postmark template asynchronously."""
        kwargs = {
            "From": self.From,
            "To": data["to"],
            "TemplateModel": data["template_model"],
            "TemplateId": data["template_id"]
        }

        return await asyncio.to_thread(
            self.client.emails.send_with_template,
            **kwargs
        )



    async def send_bulk_with_template(
        self,
        emails: List[Dict]
    ) -> List[dict]:
        """
        Send multiple templated emails asynchronously.
        Each dict should have: to_email, template (alias or id), template_model
        """
        tasks = [ self.send_with_template(e) for e in emails ]

        return await asyncio.gather(*tasks)


    async def send_issue_notification(self, data: Dict):
        """Send templated emails concurrently with graceful error handling."""
        tasks = [ self.send_with_template({"to": e, "TemplateModel": data["TemplateModel"], "TemplateId": data["TemplateId"]}) for e in data.users]
        return await asyncio.gather(*tasks)


email_service = AsyncPostmarkEmailService()
