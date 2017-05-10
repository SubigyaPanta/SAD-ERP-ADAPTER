import config
import requests
import datetime
import logging

class Incident:

    __AITSG_URL = 'https://aitsgapi.mrteera.com/incidents'
    __HEADER = {'Authorization': "JWT %s" % config.AITSG_TOKEN}
    __CLOSED_STATUS = {'status': 'closed'}
    logging.getLogger(__name__)

    def get_incidents(self, start_date, end_date):
        logging.info('Getting incidents for date: start_date[%s] and end_date[%s]' % (start_date, end_date))
        res = requests.get(self.__AITSG_URL, headers=self.__HEADER, params=self.__CLOSED_STATUS)
        logging.info('URL: [%s]' % res.url)
        response = res.json()
        incident_counts = {}
        for incident in response:
            try:
                assignee = incident['assignee']
                username = assignee['username']
                updated_at_str = incident['updatedAt'].split("T")[0]
                updated_at = datetime.datetime.strptime(updated_at_str, "%Y-%m-%d").date()
                if start_date < updated_at < end_date:
                    if incident_counts.has_key(username):
                        incident_counts[username] = incident_counts[username] + 1
                    else:
                        incident_counts[username] = 1
            except Exception as e:
                logging.error("Improper object format [%s]" % incident)
        logging.debug("Incident counts for date %s : %s" % (start_date, incident_counts))
        return incident_counts
