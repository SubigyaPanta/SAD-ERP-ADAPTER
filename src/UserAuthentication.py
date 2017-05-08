import xmlrpclib
import config
import logging


class UserAuthentication:

    __authenticated = False
    __url = config.ODOO_URL
    __db = config.ODOO_DB
    __admin_user = config.ODOO_ADMIN
    __admin_pw = config.ODOO_ADMIN_PW
    logging.getLogger(__name__)

    def __init__(self, name, identification):
        self.username = name
        self.password = identification

    def set_url(self, url):
        self.__url = url

    def set_db(self, db):
        self.__db = db

    def authenticate(self):
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.__url))
        logging.debug("Authenticating user: %s" % self.username)
        uid = common.authenticate(self.__db, self.username, self.password, {})
        logging.debug("Got uid for %s: %s" % (self.username, uid))
        return uid

    def __connect(self):
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.__url))
        self.username = self.__admin_user
        self.password = self.__admin_pw
        self.uid = self.authenticate()
        return self.uid

    def authenticate_user(self):
        self.__connect()
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.__url))
        count = models.execute_kw(self.__db, self.uid, self.__password,
                          'hr.employee', 'search_count',
                                  [[['name_related', '=', self.name], ['identification_id', '=', self.identification]]])
        if count == 0:
            self.__authenticated = False
        elif count == 1:
            self.__authenticated = True
        return self.__authenticated

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


a = UserAuthentication('bla@mycompany.com', 'secret123')
uid = a.authenticate()
groups = a.get_user_role(uid)
print groups