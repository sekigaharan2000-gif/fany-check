import requests
import json
import smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText

URL = "https://ticket.fany.lol/search/event?keywords=&from=&to=&prefectures=0&genre=0&search_type=form"

KEYWORDS = ["マヂカルラブリー", "ななまがり"]

DB_FILE = "sent.json"

def load_sent():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_sent(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

def send_mail(body):
    msg = MIMEText(body)
    msg["Subject"] = "【よしもと公演通知】"
    msg["From"] = "sekigaharan.2000@gmail.com"
    msg["To"] = "sekigaharan.2000@gmail.com"

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("sekigaharan.2000@gmail.com", "Tokuko1600")
        smtp.send_message(msg)

def main():
    sent = load_sent()

    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")

    text = soup.get_text()

    new_hits = []

    for keyword in KEYWORDS:
        if keyword in text and keyword not in sent:
            new_hits.append(keyword)

    if new_hits:
        send_mail("新規公演が見つかりました:\n" + "\n".join(new_hits))
        sent.extend(new_hits)
        save_sent(sent)

if __name__ == "__main__":
    main()
