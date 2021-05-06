import json
import smtplib
from email.message import EmailMessage

def apply():
    with open("data/cleaned_output.json", "r") as cleaned_json:
        data = json.loads(cleaned_json.read())
        for data_item in data:
            if(data_item['email']):
                email = data_item['email']
                position = data_item['position']
                intro = create_intro(data_item)
                text = f'{intro},\n\nThis letter is to express my interest in your posting on HackerNews for a {position} position.\n\nI am a software engineer at a fintech startup called AND Systems, where we developed an application that issues personal loans to under-served customers. As one of the lead developers who migrated the monolithic application into microservices, I have acquired hands-on experience with system design and AWS.\n\nYour listed requirements closely match my background and skills. A few I would like to highlight that would enable me to contribute to your bottom line are:\n\n- Highly skilled in designing, testing, and developing loosely coupled systems\n- Thorough understanding of AWS features\n- Hands-on experience with microservices\n- Passion for automation (CI/CD)\n- 3 year experience of writing production-level code\n\nI’ve attached a copy of my resume that includes the details of my projects and experience in software development.\n\nThank you for your time and consideration. I look forward to speaking with you about this opportunity.\n\nSincerely,\nChintushig Ochirsukh'
                confirm(email, text)                

def create_intro(data):
    skipping_keywords = ['career', 'employment', 'job', 'contact', 'talent', 'work', 'hiring', 'recruiting', 'info', 'hello', 'hackernews', 'hn']
    for key in skipping_keywords:
        if (data['email'].lower().find(key) != -1):
            name = data['company_name']
            return f'Dear hiring commitee at {name}'
    name = data['email'][:data['email'].lower().find('@')].replace('.', ' ').title()

    return f'Dear {name}'

# Copied from https://gist.github.com/gurunars/4470c97c916e7b3c4731469c69671d06
def confirm(email, text):
    """
    Ask user to enter Y or N (case-insensitive).
    :return: True if the answer is Y.
    :rtype: bool
    """
    answer = ""
    while answer not in ["y", "n"]:
        print('************************************************************')
        print(f'Address: {email}')

        print(text)
        print('************************************************************')
        answer = input("Send email [Y/N]? ").lower()
    if (answer == "y"):
        print(f'Sending an email to: {email}')
        send_email('Job postings on Hackernews', text, email)
    else:
        print(f'Skipping: {email}')

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
        msg['To'] = email
        with open('CHINTUSHIG_OCHIRSUKH_RESUME.pdf', 'rb') as content_file:
            content = content_file.read()
            msg.add_attachment(content, maintype='application', subtype='pdf', filename='CHINTUSHIG_OCHIRSUKH_RESUME.pdf')
        server.send_message(msg)
apply()