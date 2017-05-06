import xmlrpclib

class UserAuthentication:
    authenticated = False

    url = 'http://localhost:8069'
    db = 'odoo'
    username = 'api@subigya.com'
    password = 'api@subigya.com'

    def __init__(self, name, identification):
        self.name = name
        self.identification = identification

    def setUrl(self, url):
        self.url = url

    def setUrl(self, db):
        self.db = db

    def setUsername(self, username):
        self.username = username

    def setPassword(self, password):
        self.password = password

    def connect(self):
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        self.uid = common.authenticate(self.db, self.username, self.password, {})

    def authenticateUser(self):
        self.connect()
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
        count = models.execute_kw(self.db, self.uid, self.password,
                          'hr.employee', 'search_count',
                          [[['name_related', '=', self.name], ['identification_id', '=', self.identification]]])

        return count
