from ckan import plugins
from ckan.plugins import toolkit


class NewZealandLandcarePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    def update_config(self, config):
        # from the IConfigurer interface, we're telling ckan
        # where our templates are kept in this pluign
        toolkit.add_template_directory(config, 'templates')

