from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client
import config
from logger.server_logger import SERVER_LOGGER


SMS_CLIENT = Client(config.TWILIO_ACCT_SID, config.TWILIO_AUTH_TKN)
try:
    message = SMS_CLIENT.messages.create(
        to=config.TWILIO_RECIPIENT_DEFAULT,
        from_=config.TWILIO_PHONE_NUM,
        body=config.TWILIO_MSG_DEFAULT
    )
except TwilioRestException as e:
    SERVER_LOGGER.info(e)
    SERVER_LOGGER.info('Issue detected in Twilio SMS Client. Please try booting up again, or investigate existing Twilio credentials')
