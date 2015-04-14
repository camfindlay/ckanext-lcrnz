from ckan.plugins import toolkit


class UserController(toolkit.BaseController):

    def ldap_login(self):

        return toolkit.render('user/login_ldap.html')
