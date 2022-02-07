import time
from http.server import BaseHTTPRequestHandler
from db.dao import field
from db.dao.collection import dispatch, dispatch_transaction, communication_modal as comms
from logger import transaction_log as txn_logger
from logger.server_logger import SERVER_LOGGER
from server.e_mail import e_mail_behavior as e_mail
from server.text import text_message as text
from util import cmd_line_util as cmd, common_util as common


class DispatchHandler(BaseHTTPRequestHandler):

    def _set_response(self, dispatch_id, status, transaction_log):
        self.send_response(200 if status is field.STATUS_OK else 500, {'dispatch_id': dispatch_id, 'transaction_log': transaction_log})
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    # As of now, implementation does not require GET
    # def do_GET(self):

    def do_POST(self):
        dispatch_id = str(int(time.time()))
        dispatch_timestamp = common.get_current_timestamp()
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        SERVER_LOGGER.info("POST request,\n" + "Path: " + str(self.path) + "\nHeaders: " + str(self.headers) + "Body:\n" + post_data + "\n")
        id_post_data = common.add_dispatch_id(post_data, dispatch_id).replace("\'", "\"")
        res = dispatch.insert_dispatch(id_post_data)
        SERVER_LOGGER.info("Dispatch Response: \n" + str(res) + "\n")
        status = deploy_dispatch(dispatch_id)
        if status is field.STATUS_OK:
            SERVER_LOGGER.info("Logging Dispatch Transaction for " + dispatch_id)
            log_name = cmd.create_transaction_log(dispatch_id)
            txn_logger.write_transaction_log(log_name, dispatch_id, dispatch_timestamp, status)
        else:
            log_name = ''
        txn_res = dispatch_transaction.create_dispatch_transaction(dispatch_id, dispatch_timestamp, status, log_name)
        SERVER_LOGGER.info("Transaction Response: \n" + str(txn_res) + "\n")
        self._set_response(dispatch_id=dispatch_id, status=status, transaction_log=log_name)

# Deploy dispatch among communication mediums
def deploy_dispatch(dispatch_id):
    SERVER_LOGGER.info('Deploying Dispatch ' + dispatch_id)
    # Pseudocode
    # codes = comms.get_communication_modals_for_dispatch(dispatch_id)
    # statuses = []
    # for code in codes:
    #     statuses.append(execute_dispatch(code, dispatch_id))
    status_sms = text.execute_sms_dispatch(dispatch_id)
    status_email = e_mail.execute_email_dispatch(dispatch_id)
    # return field.STATUS_ERROR if field.STATUS_ERROR in statuses else field.STATUS_OK
    return field.STATUS_ERROR if status_sms is field.STATUS_ERROR or status_email is field.STATUS_ERROR else field.STATUS_OK

def execute_dispatch(comm_code, dispatch_id):
    if comm_code == comms.COMM_SMS:
        text.execute_sms_dispatch(dispatch_id)
    elif comm_code == comms.COMM_EMAIL:
        e_mail.execute_email_dispatch(dispatch_id)
    else:
        print('Unknown code')
        return field.STATUS_ERROR

