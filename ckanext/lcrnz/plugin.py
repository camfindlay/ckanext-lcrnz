from ckan import plugins
from ckan.plugins import toolkit


class NewZealandLandcarePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IConfigurer)

    def before_map(self, map):
        # from the IRoutes plugin, here we add an additional
        # url that maps to our terms of use controller
        terms = 'ckanext.lcrnz.controllers.terms:TermsController'
        map.connect('terms_of_use', '/terms_of_use',
                    controller=terms, action='terms_of_use')
        return map

    def update_config(self, config):
        # from the IConfigurer interface, we're telling ckan
        # where our templates are kept in this pluign
        toolkit.add_template_directory(config, 'templates')

        # add our extension's public directory, to include the custom css file
        toolkit.add_public_directory(config, 'public')
