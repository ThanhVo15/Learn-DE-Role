import os
import pandas as pd
from logging_utils import get_logger

logger = get_logger("CSVWriter")

class CSVWriter:
    @staticmethod
    def write_posts_per_user(counter: dict, path: str):
        df = pd.DataFrame([{"userId": k, "post_count": v} for k, v in counter.items()])
        df.sort_values(["post_count", "userId"], ascending=[False, True], inplace=True)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.to_csv(path, index=False, encoding="utf-8-sig")
        logger.info(f"Wrote aggregated CSV to {path}")
