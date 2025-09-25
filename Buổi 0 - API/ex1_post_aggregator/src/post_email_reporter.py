import os
import smtplib
from email.message import EmailMessage
from datetime import datetime
from logging_utils import get_logger
from post_aggregator import PostAggregator

logger = get_logger("EmailReporter")

class EmailReporter:
    def __init__(self, from_addr: str, to_addrs: list, smtp_host: str, smtp_port: int, user: str, password: str):
        self.from_addr = from_addr
        self.to_addrs = [a.strip() for a in to_addrs if a.strip()]
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.user = user
        self.password = password

    def build_summary(self, counter: dict) -> str:
        total_users = len(counter)
        total_posts = sum(counter.values())
        top3 = PostAggregator.top_n(counter, 3)
        lines = [
            f"Post Aggregation Summary ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})",
            f"Total users with posts: {total_users}",
            f"Total posts: {total_posts}",
            "",
            "Top 3 users by number of posts:"
        ]
        for user_id, count in top3:
            lines.append(f"- User {user_id}: {count} posts")
        return "\n".join(lines)

    def send(self, subject: str, body: str, attachments: list = None) -> bool:
        if not (self.user and self.password and self.to_addrs):
            logger.info("SMTP config incomplete or no recipient; printing instead.")
            print("----- EMAIL SUMMARY -----")
            print("Subject:", subject)
            print(body)
            if attachments:
                print("Attachments:", attachments)
            print("-------------------------")
            return True

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.from_addr
        msg["To"] = ", ".join(self.to_addrs)
        msg.set_content(body)

        if attachments:
            for p in attachments:
                try:
                    with open(p, "rb") as f:
                        data = f.read()
                    msg.add_attachment(data, maintype="application", subtype="octet-stream", filename=os.path.basename(p))
                except Exception as e:
                    logger.warning(f"Failed to attach {p}: {e}")

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=10) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(self.user, self.password)
                smtp.send_message(msg)
                logger.info(f"Email sent to {self.to_addrs}")
                return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
