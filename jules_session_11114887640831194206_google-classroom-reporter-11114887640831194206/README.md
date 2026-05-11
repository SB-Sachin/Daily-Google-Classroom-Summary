# Google Classroom Reporter

This tool automatically fetches announcements and coursework from your Google Classroom courses to provide a daily summary of what was done and what homework is upcoming.

## Prerequisites

1.  **Google Cloud Project**: You need a Google Cloud project with the Google Classroom API enabled.
2.  **OAuth 2.0 Credentials**:
    - Go to the [Google Cloud Console](https://console.cloud.google.com/).
    - Create OAuth 2.0 Client ID for a **Desktop Application**.
    - Download the JSON file and save it as `credentials.json` in this directory.

## Setup

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  Run the script for the first time to authorize:
    ```bash
    python3 classroom_reporter.py
    ```
    This will open a browser for you to sign in to your school account. After authorization, a `token.json` file will be created, and you won't need to sign in again until the token expires.

## Automation

To run this at 2:30 PM every school day (Monday to Friday), you can add a cron job:

1.  Open your crontab:
    ```bash
    crontab -e
    ```

2.  Add the following line (replace `/path/to/directory` with the actual path):
    ```cron
    30 14 * * 1-5 /bin/bash /path/to/directory/classroom_scheduler.sh
    ```

The reports will be saved in the `reports/` directory.
