import config
import ssl
import smtplib
from smtplib import SMTPResponseException, SMTPAuthenticationError
from email.message import EmailMessage
from db.dao import field
from db.dao.collection import user, dispatch_program
from server.e_mail.e_mail_server import SMTP_SERVER
from logger.server_logger import SERVER_LOGGER


def execute_email_dispatch(dispatch_id):
    SERVER_LOGGER.info('Beginning email dispatch for ' + dispatch_id)
    program_message = dispatch_program.get_dispatch_program_message_for_dispatch(dispatch_id)
    # Pseudocode
    # statuses = []
    # user_emails = user.get_user_emails_for_dispatch(dispatch_id)
    # for e_mail in user_emails:
    #     statuses.append(send_email(e_mail, program_message))
    status = send_gmail(program_message)
    return field.STATUS_ERROR if status is field.STATUS_ERROR else field.STATUS_OK

def send_email(e_mail, program_message):
    SERVER_LOGGER.info('Sending email to account ' + e_mail)
    with SMTP_SERVER as server:
        # Build Email
        msg = EmailMessage()
        msg['To'] = e_mail
        msg['From'] = config.EMAIL_FROM_DEFAULT
        msg['Subject'] = config.EMAIL_SUBJECT_DEFAULT
        msg.set_content(program_message)
        # Send
        try:
            server.send_message(msg)
            SERVER_LOGGER.info('Message successfully sent')
            return field.STATUS_OK
        except SMTPResponseException as e:
            SERVER_LOGGER.info(e)
            SERVER_LOGGER.info('Email failed to send for ' + e_mail)
            return field.STATUS_ERROR

# Test method to hit gmail endpoint
def send_gmail(program_message):
    SERVER_LOGGER.info('Sending test email to gmail account')
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
        # Authenticate test account
        try:
            server.login(config.USAIN_EMAIL, config.USAIN_PWD)
        except SMTPAuthenticationError as e:
            SERVER_LOGGER.info(e)
            SERVER_LOGGER.info('Test account could not be signed onto')
            return field.STATUS_ERROR
        # Send
        try:
            server.sendmail(to_addrs=config.USAIN_EMAIL, msg=program_message, from_addr=config.EMAIL_FROM_DEFAULT)
            SERVER_LOGGER.info('Message successfully sent')
            return field.STATUS_OK
        except SMTPResponseException as e:
            SERVER_LOGGER.info(e)
            SERVER_LOGGER.info('Email failed to send for ' + config.USAIN_EMAIL)
            return field.STATUS_ERROR
