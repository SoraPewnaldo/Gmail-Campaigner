import csv, os, time, random, base64, pickle, argparse, json
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def load_config():
    with open('config.json','r') as f:
        return json.load(f)

def gmail_authenticate():
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
        with open('token.pickle','wb') as token:
            pickle.dump(creds, token)
    return build('gmail','v1',credentials=creds)

def spintax(text):
    out, i = [], 0
    while i < len(text):
        if text[i] == '{':
            j = text.find('}', i)
            if j != -1:
                out.append(random.choice(text[i+1:j].split('|')))
                i = j+1
            else:
                out.append(text[i]); i+=1
        else:
            out.append(text[i]); i+=1
    return ''.join(out)

def personalize(template, row):
    t = template
    for k,v in row.items():
        t = t.replace('{{'+k+'}}', v)
    return spintax(t)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--campaign', required=True)
    parser.add_argument('--limit', type=int, default=10)
    args = parser.parse_args()

    cfg = load_config()
    svc = gmail_authenticate()

    with open('templates.txt','r',encoding='utf-8') as f:
        templates = [p.strip() for p in f.read().split('---') if p.strip()]

    with open('leads.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        sent = 0
        for row in reader:
            if sent >= args.limit:
                break
            email = row['email'].strip()
            subject = personalize(row.get('subject') or 'Video Content Ideas for {{first_name}}', row)
            body_html = personalize(random.choice(templates), row)
            body_html += f"<br><br><pre>{cfg['FOOTER_SIGNATURE']}</pre>"
            if cfg.get('TRACK_OPENS'):
                pixel = f'<img src="{cfg["WEBAPP_URL"]}?t=open&c={args.campaign}&e={email}" width="1" height="1" style="display:none;" />'
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
            time.sleep(random.randint(cfg['BATCH_DELAY_SECONDS_MIN'], cfg['BATCH_DELAY_SECONDS_MAX']))

if __name__ == '__main__':
    main()
