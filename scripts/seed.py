import asyncio
import os
import sys

# Ensure app is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.db import AsyncSessionLocal
from app.models.workflow import Workflow
from app.models.integration import Integration

async def seed_data():
    async with AsyncSessionLocal() as session:
        # Clear existing for fresh seed if needed, but for now just add new ones
        
        # 1. Integrations
        slack_integration = Integration(
            name="Demo Slack Workspace",
            integration_type="slack",
            config={"webhook_url": "https://api.slack.com/your-webhook-placeholder"}
        )
        email_integration = Integration(
            name="Demo SendGrid",
            integration_type="email",
            config={
                "api_key": "SG.mock_key_replace_me",
                "from_email": "demo@example.com"
            }
        )
        session.add(slack_integration)
        session.add(email_integration)
        await session.commit()
        await session.refresh(slack_integration)
        await session.refresh(email_integration)

        # 2. Workflows
        w1 = Workflow(
            name="Lead Triage & Alert",
            trigger_type="webhook",
            is_active=True,
            steps=[
                {
                    "name": "Classify Lead Intent",
                    "action": "ai.classify",
                    "params": {
                        "text": "{message}",
                        "categories": "Hot, Warm, Cold",
                        "fallback_value": "Warm"
                    }
                },
                {
                    "name": "Alert Sales Team",
                    "action": "slack.send",
                    "params": {
                        "integration_id": slack_integration.id,
                        "message": "🔥 *New Lead Alert!*\n*Name:* {name}\n*Email:* {email}\n*Intent Classification:* {Classify Lead Intent}"
                    }
                },
                {
                    "name": "Send Welcome Email",
                    "action": "email.send",
                    "params": {
                        "integration_id": email_integration.id,
                        "to": "{email}",
                        "subject": "Welcome to our platform, {name}!",
                        "body": "Hi {name},\n\nWe received your message:\n'{message}'\n\nOur team will get back to you shortly."
                    }
                }
            ]
        )

        w2 = Workflow(
            name="Support Ticket Summary",
            trigger_type="webhook",
            is_active=True,
            steps=[
                {
                    "name": "Summarize Issue",
                    "action": "ai.summarize",
                    "params": {
                        "text": "{issue_description}"
                    }
                },
                {
                    "name": "Create Generic Ticket",
                    "action": "http.request",
                    "params": {
                        "method": "POST",
                        "url": "https://jsonplaceholder.typicode.com/posts",
                        "json": {
                            "title": "New Support Ticket",
                            "body": "User: {email}\nSummary: {Summarize Issue}"
                        }
                    }
                }
            ]
        )

        w3 = Workflow(
            name="Manual Auto-Reply Generator",
            trigger_type="manual",
            is_active=True,
            steps=[
                {
                    "name": "Draft Reply",
                    "action": "ai.generate_reply",
                    "params": {
                        "context": "{incoming_email_text}",
                        "tone": "professional and empathetic"
                    }
                },
                {
                    "name": "Send Draft to Slack for Review",
                    "action": "slack.send",
                    "params": {
                        "integration_id": slack_integration.id,
                        "message": "Draft reply for {customer_name}:\n\n{Draft Reply}"
                    }
                }
            ]
        )

        session.add_all([w1, w2, w3])
        await session.commit()

        print("Successfully seeded 2 integrations and 3 workflows!")

if __name__ == "__main__":
    asyncio.run(seed_data())
