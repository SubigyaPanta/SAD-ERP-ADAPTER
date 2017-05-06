import xmlrpclib

class UserAuthentication:
    __authenticated = False

    __url = 'http://localhost:8069'
    __db = 'odoo'
    __username = 'api@subigya.com'
    __password = 'api@subigya.com'

    def __init__(self, name, identification):
        self.name = name
        self.identification = identification

    def setUrl(self, url):
        self.__url = url

    def setUrl(self, db):
        self.__db = db

    def setUsername(self, username):
        self.__username = username

    def setPassword(self, password):
        self.__password = password

    def connect(self):
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.__url))
        self.uid = common.authenticate(self.__db, self.__username, self.__password, {})

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
