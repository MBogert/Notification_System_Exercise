import config
from db.dao.collection import dispatch, dispatch_program, event_type, user_group, user
from db.dao import field

def write_transaction_log(log_name, dispatch_id, dispatch_timestamp, status):
    disp = dispatch.get_dispatch_by_id(dispatch_id)
    start_time = disp[field.START_TIME]

    end_time =''
    try:
        end_time = disp[field.END_TIME]
    except KeyError as e: # The system doesn't care about this exception
        print('Tossing aside exception')
        print(e)

    program = dispatch_program.get_dispatch_program(disp[field.PROGRAM_ID])
    program_name = program[field.NAME]
    program_msg = program[field.MESSAGE]

    type_of_event = event_type.get_event_type(disp[field.EVENT_TYPE_ID])
    event_name = type_of_event[field.NAME]

    user_groups = user_group.get_user_groups(type_of_event[field.USER_GROUP_IDS])
    user_ids = []
    for group_id in user_groups:
        user_ids.extend(user.get_users_in_group(group_id))

    # Pseudoimplementation
    phones = [config.TWILIO_RECIPIENT_DEFAULT]
    emails = [config.USAIN_EMAIL]

    f = open(log_name, 'w')
    f.write(f'Transaction for Dispatch: {dispatch_id} \n#===================================# \nTimestamp: {str(dispatch_timestamp)} \nStatus: {status} \nStart Time: {start_time} \n{"End Time: " + end_time if end_time is not None else "N/A"} \nEvent Type: {event_name} \nProgram Name: {program_name} \nUser Groups: {user_groups} \nPhone Numbers: {phones} \nE-mails: {emails} \nMessage: {program_msg}\n#===================================#')
    f.close()

