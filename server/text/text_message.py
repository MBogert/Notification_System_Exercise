import config
from logger.server_logger import SERVER_LOGGER
from db.dao.collection import dispatch_program, user
from db.dao import field
from twilio.base.exceptions import TwilioRestException
from server.text.twilio_client import SMS_CLIENT

# Example Twilio REST Request
# curl -X POST https://api.twilio.com/2010-04-01/Accounts/ACa75404d3c1ba1972b080925f24249dfb/Messages.json --data-urlencode "Body=Hello from Twillo" --data-urlencode "From=+18647404384" --data-urlencode "To=+13606897730" -u ACa75404d3c1ba1972b080925f24249dfb:df419092917c547146a50a347d8d3019

def execute_sms_dispatch(dispatch_id):
    SERVER_LOGGER.info('Beginning SMS Dispatch: ' + dispatch_id)
    program_message = dispatch_program.get_dispatch_program_message_for_dispatch(dispatch_id)
    # Pseudocode
    # statuses = []
    # user_numbers = user.get_user_phone_numbers_for_dispatch(dispatch_id)
    # for number in user_numbers:
    #     statuses.append(send_sms(number, program_message))
    status = send_sms(config.TWILIO_RECIPIENT_DEFAULT, program_message)
    return field.STATUS_ERROR if status is field.STATUS_ERROR else field.STATUS_OK

def send_sms(number, program_message):
    try:
        message = SMS_CLIENT.messages.create(
            to=number,
            from_=config.TWILIO_PHONE_NUM,
            body=program_message
        )
        SERVER_LOGGER.info('Message successfully sent')
        return field.STATUS_OK
    except TwilioRestException as e:
        SERVER_LOGGER.info(e)
        SERVER_LOGGER.info('Issue detected in Twilio SMS Client. Please try booting up again, or investigate existing Twilio credentials')
        return field.STATUS_ERROR
