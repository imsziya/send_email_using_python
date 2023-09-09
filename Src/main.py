from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

app = Flask(__name__)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = '*********@gmail.com'
SMTP_PASSWORD = '********'
SENDER_EMAIL = '****************'

@app.route('/api/send_email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()
        recipient_email = data.get('recipient_email')
        subject = data.get('subject')
        message = data.get('message')
        attachment_path = data.get('attachment_path')

        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        if attachment_path:
            with open(attachment_path, 'rb') as attachment_file:
                part = MIMEApplication(attachment_file.read(), Name='attachment.pdf')
            part['Content-Disposition'] = f'attachment; filename="attachment.pdf"'
            msg.attach(part)

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        server.quit()
        return jsonify({'message': 'Email sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)