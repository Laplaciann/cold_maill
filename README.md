# Automated Email Sender

This Python script allows you to send emails automatically to multiple recipients using email addresses from a CSV file. You can also attach files (like resumes or PDFs) to your emails.

## Setup

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file by copying `.env.example`:
   ```
   cp .env.example .env
   ```

3. Edit the `.env` file with your email credentials:
   - For Gmail, you'll need to use an App Password instead of your regular password
   - To generate an App Password:
     1. Go to your Google Account settings
     2. Navigate to Security
     3. Enable 2-Step Verification if not already enabled
     4. Go to App Passwords
     5. Generate a new app password for "Mail"

## CSV File Format

The script uses `example_recipients.csv` in the same directory. Make sure this file has a column named 'email' containing recipient email addresses.

## Usage

### Complete Setup and Run Commands

```bash
# Clone the repository (if you haven't already)
git clone <repository-url>
cd cold\ mail

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment file
cp .env.example .env
# Edit .env with your email credentials

# Run the script
python email_sender.py
```

Follow the prompts to:
1. Enter the email subject
2. Enter the email body (press Ctrl+D or Ctrl+Z when finished)
3. Optionally enter the path to a file attachment (like a resume or PDF)

The script will automatically use the email addresses from `example_recipients.csv` in the same directory.
