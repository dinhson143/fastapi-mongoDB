import logging
import os
from datetime import datetime

from app.external_services.aws_s3 import upload_log_to_s3


class S3LoggingHandler(logging.Handler):
    def __init__(self, log_file_path: str, s3_key: str):
        super().__init__()
        self.log_file_path = log_file_path
        self.s3_key = s3_key
        self.is_uploading = False

        log_dir = os.path.dirname(log_file_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

    def emit(self, record):
        try:
            log_entry = self.format(record)
            with open(self.log_file_path, 'a') as log_file:
                log_file.write(log_entry + '\n')

            if not self.is_uploading:
                self.is_uploading = True
                self.upload_log()
                self.is_uploading = False

        except Exception as e:
            print(f"Failed to log and upload to S3: {e}")

    def upload_log(self):
        try:
            upload_log_to_s3(self.log_file_path, self.s3_key)
        except Exception as e:
            print(f"Failed to upload log to S3 service: {e}")


def setup_logger(s3_log_key: str):
    log_file_path = "logs/app.log"

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if not any(isinstance(h, S3LoggingHandler) for h in logger.handlers):
        s3_handler = S3LoggingHandler(log_file_path=log_file_path, s3_key=s3_log_key)
        s3_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        s3_handler.setFormatter(formatter)

        logger.addHandler(s3_handler)

    return logger


S3_LOG_KEY = f"logs/book_store"
logger = setup_logger(S3_LOG_KEY)