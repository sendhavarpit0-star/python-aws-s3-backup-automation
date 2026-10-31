# AWS S3 Automated Backup Script with Telegram Alerts

A production-ready Python automation tool designed to securely back up MySQL databases and web server directories, compress them into tar archives, upload them directly to an Amazon S3 bucket, and send real-time status alerts via Telegram Bot.

## 🚀 Features
- **Secure Configuration:** Uses environment variables (`.dotenv`) to prevent hardcoding sensitive credentials.
- **Database Dump:** Automatically generates a secure MySQL database backup using `mysqldump`.
- **Cloud Integration:** Uploads compressed backup archives directly to AWS S3 using `boto3`.
- **Instant Monitoring:** Sends real-time success or failure notifications via Telegram Bot API.
- **Auto Cleanup:** Removes temporary local backup files to save server storage.

## 🛠️ Tech Stack
- **Language:** Python
- **Cloud Storage:** AWS S3 (`boto3`)
- **Database:** MySQL / MariaDB
- **Notifications:** Telegram Bot API
