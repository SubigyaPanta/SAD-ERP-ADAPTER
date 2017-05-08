import requests
import logging
import ast


class MessageQueue():

    __REQUEST_QUEUE_URL = 'https://aitsgqueues.mrteera.com/messages/erp_request'
    __RESPONSE_QUEUE_URL = 'https://aitsgqueues.mrteera.com/messages/erp_response'
    __DELETE_MSG_URL = 'https://aitsgqueues.mrteera.com/messages/erp_request/{}'
    logging.getLogger(__name__)

    def __init__(self):
        pass

    def get_message(self):
        resp = requests.get(self.__REQUEST_QUEUE_URL, verify=False)
        message_from_req = resp.json()

        if ('{}' == str(message_from_req)):
            logging.info('No message in the queue:' + str(message_from_req))
            return None, None
        else:
            logging.info('Found a message in the queue: ' + str(message_from_req['id']))
            message_id = message_from_req['id']
            auth_details = ast.literal_eval(message_from_req['message'])
            return auth_details, message_id

    # Sends authentication response to queue
    # message should be dict type
    # It should contain the keys: username, success, device-token
    def send_response(self, message, message_id):
        if message is None:
            return None
        resp_msg = "{\r\n\t\"gid\": \"%s\"" % message['username']
        resp_msg += ",\r\n\t\"name\": \"noname\""
        resp_msg += ",\r\n\t\"auth\": \"%s\"" % message['success']
        resp_msg += ",\r\n\t\"role\": \"%s\"" % message['role']
        resp_msg += ",\r\n\t\"device_token\": \"%s\"\r\n}" % message['device-token']
        payload = {"qname": "erp_response",
                   "message": resp_msg
                   }
        resp = requests.post(self.__RESPONSE_QUEUE_URL, payload, verify=False)
        logging.debug("erp_response status code: " + str(resp.status_code))
        if resp.status_code == 200:
            resp = requests.delete(self.__DELETE_MSG_URL.format(message_id), verify=False)
            logging.debug('delete message status: ' + str(resp.status_code))

