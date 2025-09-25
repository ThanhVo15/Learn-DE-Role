import os
import asyncio
from datetime import datetime
from post_client import PostClient
from post_aggregator import PostAggregator
from writer import CSVWriter
from post_email_reporter import EmailReporter
from config import OUTPUT_DIR, EMAIL_FROM, EMAIL_TO, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD
from logging_utils import get_logger

logger = get_logger("Orchestrator")

async def handle_client(client_id: str):
    logger.info(f"Client {client_id} start")
    try:
        posts = await PostClient.get_posts()
        counter = PostAggregator.count_per_user(posts)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = os.path.join(OUTPUT_DIR, f"posts_per_user_{client_id}_{ts}.csv")
        CSVWriter.write_posts_per_user(counter, csv_path)

        reporter = EmailReporter(
            from_addr=EMAIL_FROM,
            to_addrs=EMAIL_TO.split(",") if EMAIL_TO else [],
            smtp_host=SMTP_HOST,
            smtp_port=SMTP_PORT,
            user=SMTP_USER,
            password=SMTP_PASSWORD,
        )
        summary = reporter.build_summary(counter)
        subject = f"[Client {client_id}] Post Aggregation Report"
        reporter.send(subject=subject, body=summary, attachments=[csv_path])

        top3 = PostAggregator.top_n(counter, 3)
        logger.info(f"Client {client_id} top3: {top3}")
        return {"client_id": client_id, "top3": top3}
    except Exception as e:
        logger.error(f"Client {client_id} error: {e}")
        return {"client_id": client_id, "error": str(e)}

async def simulate_many_clients(n_clients: int = 3):
    tasks = [handle_client(f"client_{i+1}") for i in range(n_clients)]
    results = await asyncio.gather(*tasks)
    return results
