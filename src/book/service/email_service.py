import os
import smtplib
from email.message import EmailMessage

from src.book.entity.book_entity import Book


class EmailNotifier:
    def __init__(
        self,
        enabled: bool | None = None,
        host: str | None = None,
        port: int | None = None,
        sender: str | None = None,
        recipient: str | None = None,
    ):
        self.enabled = enabled if enabled is not None else os.environ.get("book_EMAIL_ENABLED") == "true"
        self.host = host or os.environ.get("book_EMAIL_HOST", "127.0.0.1")
        self.port = port or int(os.environ.get("book_EMAIL_PORT", "1025"))
        self.sender = sender or os.environ.get("book_EMAIL_FROM", "book-api@example.local")
        self.recipient = recipient or os.environ.get("book_EMAIL_TO", "library@example.local")

    def send_book_created(self, book: Book) -> bool:
        if not self.enabled:
            return False

        message = EmailMessage()
        message["Subject"] = f"New book added: {book.title}"
        message["From"] = self.sender
        message["To"] = self.recipient
        message.set_content(
            "\n".join(
                [
                    "A new book was added.",
                    "",
                    f"Title: {book.title}",
                    f"Author: {book.author.full_name}",
                    f"Publisher: {book.publisher.name}",
                    f"Publication year: {book.publication_year or 'unknown'}",
                ]
            )
        )

        try:
            with smtplib.SMTP(self.host, self.port, timeout=5) as smtp:
                smtp.send_message(message)
            return True
        except (OSError, smtplib.SMTPException):
            return False


email_notifier = EmailNotifier()
