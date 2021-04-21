import json
import smtplib
from email.message import EmailMessage

def apply():
    with open("data/cleaned_output.json", "r") as cleaned_json:
        data = json.loads(cleaned_json.read())
        for data_item in data:
            if(data_item['email']):
                subject = 'Job postings on Hackernews'
                position = data_item['position']
                text = f'Greetings,\n\nThis letter is to express my interest in your posting on HackerNews for a {position} position.\n\nI am a junior backend developer at a fintech startup called AndSystems, where we developed an application that issues personal loans to under-served customers. As one of the lead developers who migrated the monolithic application into microservices, I have acquired hands-on experience with system design and AWS.\n\nYour listed requirements closely match my background and skills. A few I would like to highlight that would enable me to contribute to your bottom line are:\n\n- Highly skilled in designing, testing, and developing loosely coupled systems\n- Thorough understanding of AWS features\n- Hands-on experience with microservices\n- Passion for automation (CI/CD)\n- 3 year experience of writing production-level code\n\nI’ve attached a copy of my resume that includes the details of my projects and experience in software development.\n\nThank you for your time and consideration. I look forward to speaking with you about this opportunity.\n\nSincerely,\nChintushig Ochirsukh'
                email = data_item['email']
                
                send_email(subject, text, email)

def send_email(subject, text, email):
    with open("email-credentials.json", "r") as credentials_json:
        credentials = json.loads(credentials_json.read())
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        #This is where you would replace your password with the app password
        server.login(credentials['email'], credentials['app_password'])
        msg = EmailMessage()

        message = f'{text}\n'
        msg.set_content(message)
        msg['Subject'] = subject
        msg['From'] = 'tushig.tushig@gmail.com'
        msg['To'] = 'tushig.tushig@gmail.com'
        with open('CHINTUSHIG_OCHIRSUKH_RESUME.pdf', 'rb') as content_file:
            content = content_file.read()
            msg.add_attachment(content, maintype='application', subtype='pdf', filename='CHINTUSHIG_OCHIRSUKH_RESUME.pdf')
        server.send_message(msg)
apply()