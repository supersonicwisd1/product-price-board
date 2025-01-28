# product_price_board/app/services/notification.py
from fastapi_mail import FastMail, MessageSchema
from app.core.config import settings

class NotificationService:
    def __init__(self):
        self.fastmail = FastMail(settings.mail_config.dict())  # Use dict() to pass the configuration

    async def send_notification(self, email: str, subject: str, body: str) -> None:
        message = MessageSchema(
            subject=subject,
            recipients=[email],
            body=body,
            subtype="html"
        )
        await self.fastmail.send_message(message)

    def send_notification_background(self, background_tasks, email: str, subject: str, body: str) -> None:
        """
        Use BackgroundTasks to send the notification in the background.
        """
        background_tasks.add_task(self.send_notification, email, subject, body)
