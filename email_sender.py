import csv
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

# Fixed path for recipients CSV file
RECIPIENTS_CSV_PATH = os.path.join(os.path.dirname(__file__), 'example_recipients.csv')

def load_email_config():
    """Load email configuration from environment variables"""
    load_dotenv()
    return {
        'sender_email': os.getenv('SENDER_EMAIL'),
        'sender_password': os.getenv('SENDER_PASSWORD'),
        'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
        'smtp_port': int(os.getenv('SMTP_PORT', '587'))
    }

def read_csv_data(file_path):
    """Read recipient email addresses from CSV file"""
    try:
        emails = []
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'email' in row:
                    emails.append(row['email'])
        return emails
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

def send_email(recipient, subject, body, config, attachment_path=None):
    """Send email to a single recipient"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = config['sender_email']
        msg['To'] = recipient
        msg['Subject'] = subject

        # Add body
        msg.attach(MIMEText(body, 'plain'))

        # Add attachment if provided
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as f:
                attachment = MIMEApplication(f.read(), _subtype=os.path.splitext(attachment_path)[1][1:])
                attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))
                msg.attach(attachment)

        # Create SMTP session
        with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
            server.starttls()
            server.login(config['sender_email'], config['sender_password'])
            server.send_message(msg)
        
        print(f"Successfully sent email to {recipient}")
        return True
    except Exception as e:
        print(f"Error sending email to {recipient}: {e}")
        return False

def main():
    # Load configuration
    config = load_email_config()
    if not all([config['sender_email'], config['sender_password']]):
        print("Please set up your email credentials in .env file")
        return

    # Read recipient emails from the fixed CSV path
    recipients = read_csv_data(RECIPIENTS_CSV_PATH)
    if not recipients:
        print("No email addresses found in Excel file")
        return

    # Get email content
    subject = input("Enter email subject: ")
    print("Enter email body (press Ctrl+D or Ctrl+Z when finished):")
    body = ""
    try:
        while True:
            line = input()
            body += line + "\n"
    except EOFError:
        pass

    # Get attachment path
    attachment_path = input("Enter path to attachment (leave empty for no attachment): ").strip()
    if attachment_path and not os.path.exists(attachment_path):
        print(f"Warning: Attachment file '{attachment_path}' not found")
        attachment_path = None

    # Send emails
    success_count = 0
    for recipient in recipients:
        if send_email(recipient, subject, body, config, attachment_path):
            success_count += 1

    print(f"\nSummary: Successfully sent {success_count} out of {len(recipients)} emails")

if __name__ == "__main__":
    main()
