"""
Gmail Campaigner - Personalized email outreach tool using Gmail API.

This script sends personalized HTML emails from a CSV of leads using Gmail API.
Features include template rotation, spintax support, open tracking, and unsubscribe links.
"""
import csv
import os
import time
import random
import base64
import pickle
import argparse
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def load_config():
    """Load configuration from config.json file."""
    if not os.path.exists('config.json'):
        raise FileNotFoundError(
            "config.json not found. Please copy config.sample.json to config.json and update it with your settings."
        )
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config.json: {e}")
    except Exception as e:
        raise RuntimeError(f"Error reading config.json: {e}")


def gmail_authenticate():
    """Authenticate with Gmail API using OAuth2."""
    if not os.path.exists('credentials.json'):
        raise FileNotFoundError(
            "credentials.json not found. Please download it from Google Cloud Console."
        )

    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)


def spintax(text):
    """Process spintax syntax {option1|option2} and choose random option."""
    out, i = [], 0
    while i < len(text):
        if text[i] == '{':
            j = text.find('}', i)
            if j != -1:
                out.append(random.choice(text[i+1:j].split('|')))
                i = j + 1
            else:
                out.append(text[i])
                i += 1
        else:
            out.append(text[i])
            i += 1
    return ''.join(out)


def personalize(template, row):
    """Personalize template by replacing {{key}} placeholders with values from row."""
    t = template
    for k, v in row.items():
        t = t.replace('{{'+k+'}}', v)
    return spintax(t)


def main():
    """Main function to send personalized Gmail campaigns."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--campaign', required=True)
    parser.add_argument('--limit', type=int, default=10)
    args = parser.parse_args()

    try:
        cfg = load_config()
        svc = gmail_authenticate()

        # Load and validate templates
        if not os.path.exists('templates.txt'):
            raise FileNotFoundError(
                "templates.txt not found. Please copy templates_sample.txt to templates.txt and update it."
            )

        with open('templates.txt', 'r', encoding='utf-8') as f:
            templates = [p.strip() for p in f.read().split('---') if p.strip()]

        if not templates:
            raise ValueError("No templates found in templates.txt. Please add at least one template.")

        # Load and validate leads
        if not os.path.exists('leads.csv'):
            raise FileNotFoundError(
                "leads.csv not found. Please copy leads_sample.csv to leads.csv and update it with your leads."
            )

        with open('leads.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # Validate required columns
            required_columns = ['email', 'first_name']
            if not all(col in reader.fieldnames for col in required_columns):
                missing = [col for col in required_columns if col not in reader.fieldnames]
                raise ValueError(f"Missing required columns in leads.csv: {missing}")

            sent = 0
            for row in reader:
                if sent >= args.limit:
                    break

                email = row['email'].strip()
                if not email:
                    print(f"Skipping row with empty email: {row}")
                    continue

                subject = personalize(
                    row.get('subject') or 'Video Content Ideas for {{first_name}}',
                    row
                )
                body_html = personalize(random.choice(templates), row)
                body_html += f"<br><br><pre>{cfg['FOOTER_SIGNATURE']}</pre>"

                if cfg.get('TRACK_OPENS'):
                    pixel_url = f'{cfg["WEBAPP_URL"]}?t=open&c={args.campaign}&e={email}'
                    pixel = f'<img src="{pixel_url}" width="1" height="1" style="display:none;" />'
                    body_html += pixel

                unsub_link = f'{cfg["WEBAPP_URL"]}?t=unsub&c={args.campaign}&e={email}'
                body_html += f'<p style="font-size:12px;"><a href="{unsub_link}">{cfg["UNSUB_TEXT"]}</a></p>'

                msg = MIMEMultipart('alternative')
                msg['From'] = formataddr((cfg['FROM_NAME'], cfg['FROM_EMAIL']))
                msg['To'] = email
                msg['Subject'] = subject
                msg.attach(MIMEText(body_html, 'html'))

                raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
                svc.users().messages().send(userId='me', body={'raw': raw}).execute()

                sent += 1
                print(f"Sent email {sent}/{args.limit} to {email}")

                time.sleep(random.randint(
                    cfg['BATCH_DELAY_SECONDS_MIN'],
                    cfg['BATCH_DELAY_SECONDS_MAX']
                ))

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
