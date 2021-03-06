from MessageQueue import MessageQueue
from OdooConnector import OdooConnector
from time import sleep
from requests.exceptions import ConnectionError
import logging

if __name__ == '__main__':

    logging.basicConfig(filename='../auth.log', level=logging.DEBUG, format="[%(filename)s:%(lineno)s - %(funcName)s ] %(message)s")

    while True:
        try:
            queue = MessageQueue()
            auth_details, id = queue.get_message()
            if auth_details is not None and id is not None:
                username = auth_details['username']
                password = auth_details['password']
                auth = OdooConnector()
                is_authenticated = auth.authenticate(username, password)
                logging.debug("Authentication result for %s: %s" % (username, is_authenticated))
                if is_authenticated is False:
                    success = 'false'
                    role = 'None'
                else:
                    success = 'true'
                    role = auth.get_user_role(is_authenticated)
                response = {'username': username, 'success': success, 'role': role, 'device-token': auth_details['device-token']}
                logging.debug("Response for %s: %s" % (username, response))
                queue.send_response(response, id)
        except ConnectionError as connection_error:
            logging.error('There is something wrong with the connection: [%s]' % connection_error)
        except Exception as exception:
            logging.error('Something went wrong [%s]' % exception)
    sleep(5)
