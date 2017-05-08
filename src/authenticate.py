from MessageQueue import MessageQueue
from UserAuthentication import UserAuthentication
from time import sleep
import logging

while True:
    logging.basicConfig(filename='../auth.log', level=logging.DEBUG, format="[%(filename)s:%(lineno)s - %(funcName)s ] %(message)s")
    queue = MessageQueue()
    auth_details, id = queue.get_message()
    if auth_details is not None and id is not None:
        username = auth_details['username']
        password = auth_details['password']
        auth = UserAuthentication(username, password)
        is_authenticated = auth.authenticate()
        logging.debug("Authentication result for %s: %s" % (username, is_authenticated))
        if is_authenticated is False:
            success = 'false'
            role = 'None'
        else:
            success = 'true'
            role = auth.get_user_role(is_authenticated)
        response = {'username': username, 'success': success,'role': role, 'device-token': auth_details['device-token']}
        logging.debug("Response for %s: %s" % (username, response))
        queue.send_response(response, id)
    sleep(5)
