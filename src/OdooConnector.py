import xmlrpclib
import config
import logging


class OdooConnector:

    __authenticated = False
    __url = config.ODOO_URL
    __db = config.ODOO_DB
    __admin_user = config.ODOO_ADMIN
    __admin_pw = config.ODOO_ADMIN_PW
    logging.getLogger(__name__)

    def __init__(self):
        pass

    def set_url(self, url):
        self.__url = url

    def set_db(self, db):
        self.__db = db

    def authenticate(self, username, password):
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.__url))
        logging.debug("Authenticating user: %s" % username)
        uid = common.authenticate(self.__db, username, password, {})
        logging.debug("Got uid for %s: %s" % (username, uid))
        return uid

    def __connect(self):
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.__url))
        self.uid = self.authenticate(self.__admin_user, self.__admin_pw)
        return self.uid

    def get_user_role(self, user_id):
        if user_id is False:
            return 'None'
        uid = self.__connect()
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.__url))
        groups = models.execute_kw(self.__db, uid, self.__admin_pw,
                                  'res.users', 'search_read',
                                  [[['id', '=', user_id]]], {'fields': ['groups_id']})
        group_ids = groups[0]['groups_id']
        # get manager role id
        manager_id = models.execute_kw(self.__db, uid, self.__admin_pw,
                                  'res.groups', 'search',
                                  [[['name', '=', 'Manager']]])
        # get employee role id
        employee_id = models.execute_kw(self.__db, uid, self.__admin_pw,
                                  'res.groups', 'search',
                                  [[['name', '=', 'Employee']]])
        if manager_id[0] in group_ids:
            role = 'Manager'
        elif employee_id[0] in group_ids:
            role = 'Employee'
        else:
            role = 'None'
        return role

    # Finds the user with the given username in Odoo
    def find_user(self, username):
        uid = self.__connect()
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.__url))
        user_id = models.execute_kw(self.__db, uid, self.__admin_pw, 'res.users', 'search',
                                    [[['login', '=', username]]])
        return user_id

    # Writes completed incident's count to employees in Odoo
    def write_current_incident(self, user_id, incident_count):
        logging.info('Writing incident_count %s for user %s' % (incident_count, user_id))
        uid = self.__connect()
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.__url))
        user = models.execute_kw(self.__db, uid, self.__admin_pw,
                          'res.users', 'read',
                          [user_id], {'fields': ['employee_ids']})
        employee_id = user[0]['employee_ids'][0]
        models.execute_kw(self.__db, uid, self.__admin_pw, 'hr.employee', 'write', [[employee_id], {
            'x_incidents': incident_count
        }])




# a = UserAuthentication('bla@mycompany.com', 'secret123')
# uid = a.authenticate()
# groups = a.get_user_role(uid)
# print groups