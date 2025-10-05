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


    # async def send_issue_notification(service, template_id, template_model, users):
    #     """Send templated emails concurrently with graceful error handling."""
    #
    #     async def send_email(email: str):
    #         try:
    #             await service.send_with_template(
    #                 to=email,
    #                 template_id=template_id,
    #                 template_model=template_model,
    #             )
    #
    #         except Exception as _:
    #             global_logger.exception("Failed While Tying To Send Issue Notifications")
    #
    #     await asyncio.gather(*(send_email(email) for email in users))


email_service = AsyncPostmarkEmailService()
