import pandas as pd
import os
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# ================= CONFIG =================
FROM_EMAIL = "demo_email@gmail.com"   # dummy (not used for sending)
ATTACHMENT_PATH = "sample.pdf"
LOG_FILE = "logs.csv"
DELAY = 1   # faster for demo

# ==========================================

# Load HTML Template
def load_template():
    with open("template.html", "r") as file:
        return file.read()

def personalize_template(template, name, interest):
    return template.replace("{{name}}", name).replace("{{interest}}", interest)

# Attach File
def attach_file(msg):
    if not os.path.exists(ATTACHMENT_PATH):
        print("Attachment not found, skipping...")
        return
    
    with open(ATTACHMENT_PATH, "rb") as file:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(file.read())
    
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename={os.path.basename(ATTACHMENT_PATH)}"
    )
    msg.attach(part)
# Logging
def log_status(name, email, status):
    df = pd.DataFrame(
        [[name, email, status, datetime.now()]],
        columns=["Name", "Email", "Status", "Time"]
    )
    
    if not os.path.exists(LOG_FILE):
        df.to_csv(LOG_FILE, index=False)
    else:
        df.to_csv(LOG_FILE, mode='a', header=False, index=False)

# Main Logic

def send_emails():
    data = pd.read_csv("abc.csv")
    template = load_template()

    success = 0
    failed = 0

    print(" Starting Email Simulation...\n")

    for i in range(len(data)):
        name = data.loc[i, "name"]
        email = data.loc[i, "email"]
        interest = data.loc[i, "interest"]

        msg = MIMEMultipart() #create email
        msg["From"] = FROM_EMAIL
        msg["To"] = email
        msg["Subject"] = "Personalized Email"

        body = personalize_template(template, name, interest)
        msg.attach(MIMEText(body, "html"))

        attach_file(msg)

        try:
            # No real sending
            print(f"[SIMULATED] Email sent to {name} ({email})")

            # Optional preview (first 100 chars)
            print("Preview:", body[:100].replace("\n", " "), "...\n")

            log_status(name, email, "Sent (Simulated)")
            success += 1

        except Exception as e:
            print(f"Failed for {email} | {e}")
            log_status(name, email, "Failed")
            failed += 1

        time.sleep(DELAY)

    print("\nSummary:")
    print(f"Total: {len(data)}")
    print(f"Sent: {success}")
    print(f"Failed: {failed}")

if __name__ == "__main__":
    send_emails()