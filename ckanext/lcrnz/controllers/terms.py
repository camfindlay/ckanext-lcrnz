from ckan.plugins import toolkit

class TermsController(toolkit.BaseController):
    def terms_of_use(self):
        return toolkit.render('terms_of_use.html')
