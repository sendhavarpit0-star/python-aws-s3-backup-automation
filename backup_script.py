import os
import subprocess
import boto3
import requests
from datetime import datetime
from dotenv import load_dotenv

# --- `.env` File Load Karein ---
load_dotenv()

# --- CONFIGURATION (Environment variables se load hoga) ---
DB_NAME = os.getenv("DB_NAME", "your_database_name")
DB_USER = os.getenv("DB_USER", "your_db_user")
DB_PASS = os.getenv("DB_PASS", "your_db_password")
APP_DIR = os.getenv("APP_DIR", "/var/www/html")  
BACKUP_DIR = "/tmp/backups"

# AWS Credentials
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "sumit-backup-storage-2026")
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_TELEGRAM_CHAT_ID")

def send_telegram_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram error: {e}")

def run_backup():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = f"backup_{timestamp}.tar.gz"
    backup_filepath = os.path.join(BACKUP_DIR, backup_filename)
    
    db_dump_path = os.path.join(BACKUP_DIR, f"db_{timestamp}.sql")

    try:
        # 1. Database Dump
        print("Taking database dump...")
        dump_cmd = f"mysqldump -u {DB_USER} -p'{DB_PASS}' {DB_NAME} > {db_dump_path}"
        subprocess.run(dump_cmd, shell=True, check=True)

        # 2. Compress files
        print("Compressing files...")
        tar_cmd = f"tar -czf {backup_filepath} -C {BACKUP_DIR} {os.path.basename(db_dump_path)} -C {os.path.dirname(APP_DIR)} {os.path.basename(APP_DIR)}"
        subprocess.run(tar_cmd, shell=True, check=True)

        # 3. Upload to AWS S3
        print("Uploading to AWS S3...")
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION
        )
        s3_client.upload_file(backup_filepath, S3_BUCKET_NAME, backup_filename)

        # 4. Cleanup local files
        if os.path.exists(db_dump_path):
            os.remove(db_dump_path)
        if os.path.exists(backup_filepath):
            os.remove(backup_filepath)

        success_msg = f"🟢 *Backup Successful!*\n\nFile: `{backup_filename}` uploaded to S3 bucket `{S3_BUCKET_NAME}` successfully."
        send_telegram_alert(success_msg)
        print("Backup completed and alert sent!")

    except Exception as e:
        error_msg = f"🔴 *Backup Failed!*\n\nError: `{str(e)}`"
        send_telegram_alert(error_msg)
        print(f"Backup failed: {e}")

if __name__ == "__main__":
    run_backup()