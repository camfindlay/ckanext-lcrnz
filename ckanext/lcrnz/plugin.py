from ckan import plugins
from ckan.plugins import toolkit

import ckanext.lcrnz.logic.validators as validators


class NewZealandLandcarePlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IValidators)

    def _modify_package_schema(self, schema):
        schema.update({
            'publisher': [toolkit.get_validator('ignore_empty'),
                          toolkit.get_converter('convert_to_extras')],
            'publication_year': [toolkit.get_validator('ignore_empty'),
                                 toolkit.get_validator('ckanext_lcrnz_is_year'),
                                 toolkit.get_converter('convert_to_extras')],
            'start_date': [toolkit.get_validator('ignore_empty'),
                           toolkit.get_validator('ckanext_lcrnz_is_date'),
                           toolkit.get_converter('convert_to_extras')],
            'end_date': [toolkit.get_validator('ignore_empty'),
                         toolkit.get_validator('ckanext_lcrnz_is_date'),
                         toolkit.get_converter('convert_to_extras')],
            'doi': [toolkit.get_validator('ignore_empty'),
                    toolkit.get_converter('convert_to_extras')],
        })
        schema['author'] = [toolkit.get_validator('repeating_text'),
                            toolkit.get_validator('ignore_empty')]
        return schema

    def create_package_schema(self):
        schema = super(NewZealandLandcarePlugin, self).create_package_schema()
        return self._modify_package_schema(schema)

    def update_package_schema(self):
        schema = super(NewZealandLandcarePlugin, self).update_package_schema()
        return self._modify_package_schema(schema)

    def show_package_schema(self):
        schema = super(NewZealandLandcarePlugin, self).show_package_schema()

        schema.update({
            'publisher': [toolkit.get_converter('convert_from_extras'),
                          toolkit.get_validator('ignore_empty')],
            'publication_year': [toolkit.get_converter('convert_from_extras'),
                                 toolkit.get_validator('ignore_empty'),
                                 toolkit.get_validator('ckanext_lcrnz_is_year'),
                                 ],
            'start_date': [toolkit.get_converter('convert_from_extras'),
                           toolkit.get_validator('ignore_empty'),
                           toolkit.get_validator('ckanext_lcrnz_is_date'),
                           ],
            'end_date': [toolkit.get_converter('convert_from_extras'),
                         toolkit.get_validator('ignore_empty'),
                         toolkit.get_validator('ckanext_lcrnz_is_date'),
                         ],
            'doi': [toolkit.get_converter('convert_from_extras'),
                    toolkit.get_validator('ignore_empty')],
        })
        schema['author'] = [toolkit.get_validator('repeating_text_output'),
                            toolkit.get_validator('ignore_empty')]

        return schema

    def is_fallback(self):
        return True

    def package_types(self):
        return []

    def before_map(self, map):
        # from the IRoutes plugin, here we add an additional
        # url that maps to our terms of use controller
        terms = 'ckanext.lcrnz.controllers.terms:TermsController'
        map.connect('terms_of_use', '/terms_of_use',
                    controller=terms, action='terms_of_use')

        user = 'ckanext.lcrnz.controllers.user:UserController'
        map.connect('ldap_login', '/user/ldap_login',
                    controller=user, action='ldap_login')

        return map

    def update_config(self, config):
        # from the IConfigurer interface, we're telling ckan
        # where our templates are kept in this pluign
        toolkit.add_template_directory(config, 'templates')

        # add our extension's public directory, to include the custom css file
        toolkit.add_public_directory(config, 'public')

        toolkit.add_resource('fanstatic', 'lcrnz')

    def get_validators(self):
        return {
            'ckanext_lcrnz_is_year': validators.is_year,
            'ckanext_lcrnz_is_date': validators.is_date
        }
