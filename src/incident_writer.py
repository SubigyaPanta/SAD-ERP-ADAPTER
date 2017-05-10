import logging
from Incident import Incident
from OdooConnector import OdooConnector
import datetime
import calendar

logging.basicConfig(filename='../incident.log', level=logging.DEBUG, format="[%(filename)s:%(lineno)s - %(funcName)s ] %(message)s")
current_date = datetime.date.today()
_, num_days = calendar.monthrange(current_date.year, current_date.month)
start_date = datetime.date(current_date.year, current_date.month, 1)
end_date = datetime.date(current_date.year, current_date.month, num_days)
incident_status = Incident()
incident_counts = incident_status.get_incidents(start_date, end_date)
auth = OdooConnector()
for username in incident_counts.keys():
    user_id = auth.find_user(username)
    if user_id is not False:
        auth.write_current_incident(user_id, incident_counts[username])
    else:
        logging.warn('No user with username[%s] in the system' % username)

# auth = OdooConnector()
# uid = auth.authenticate('somchai@mycompany.com', 'secret123')
# print uid
# auth.write_current_incident(uid,2)