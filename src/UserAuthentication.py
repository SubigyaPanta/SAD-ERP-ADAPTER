import xmlrpclib
import config

class UserAuthentication:
    __authenticated = False

    __url = config.ODOO_URL
    __db = config.ODOO_DB

    def __init__(self, name, identification):
        self.username = name
        self.password = identification

    def setUrl(self, url):
        self.__url = url

    def setUrl(self, db):
        self.__db = db


    def authenticate(self):
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.__url))
        print self.username
        print self.password
        self.uid = common.authenticate(self.__db, self.username, self.password, {})
        return self.uid

    def authenticateUser(self):
        self.connect()
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.__url))
        count = models.execute_kw(self.__db, self.uid, self.__password,
                          'hr.employee', 'search_count',
                                  [[['name_related', '=', self.name], ['identification_id', '=', self.identification]]])
        if (count == 0):
            self.__authenticated = False
        elif(count == 1):
            self.__authenticated = True
        return self.__authenticated