import asyncio
from postmarker.core import PostmarkClient
from typing import List, Dict

class AsyncPostmarkEmailService:
    def __init__(self, server_token: str, from_email: str):
        self.client = PostmarkClient(server_token=server_token)
        self.from_email = from_email

    async def send_single(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        text_body: str = None
    ):
        """Send a single transactional email asynchronously"""
        return await asyncio.to_thread(
            self.client.emails.send,
            From=self.from_email,
            To=to_email,
            Subject=subject,
            HtmlBody=html_body,
            TextBody=text_body or html_body
        )

    async def send_bulk(self, emails: List[Dict]):
        """
        Send multiple emails asynchronously.
        Each dict should have: to_email, subject, html_body, optional text_body
        """
        tasks = [
            self.send_single(
                to_email=e["to_email"],
                subject=e["subject"],
                html_body=e["html_body"],
                text_body=e.get("text_body")
            )
            for e in emails
        ]
        return await asyncio.gather(*tasks)


    async def send_with_template(
        self,
        to_email: str,
        template_alias: str,
        template_model: Dict
    ):
        """Send an email using a Postmark template asynchronously"""
        return await asyncio.to_thread(
            self.client.emails.send_with_template,
            From=self.from_email,
            To=to_email,
            TemplateAlias=template_alias,
            TemplateModel=template_model
        )
