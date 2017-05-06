from MessageQueue import MessageQueue
from UserAuthentication import UserAuthentication

# while (True):
queue = MessageQueue()
auth_details, id = queue.get_message()
if(auth_details != None and id != None):
    username = auth_details['username']
    password = auth_details['password']
    auth = UserAuthentication(username, password)
    is_authenticated = auth.authenticate()
    print "Authentication result for %s: %s", username, is_authenticated
    if (is_authenticated == False):
        success = 'false'
    else:
        success = 'true'
    response = {'username': username, 'success': success, 'device-token': auth_details['device-token']}
    queue.send_response(response, id)