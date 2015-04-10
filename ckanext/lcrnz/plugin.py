from ckan import plugins
from ckan.plugins import toolkit

import ckanext.lcrnz.logic.validators as validators


class NewZealandLandcarePlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IValidators)

    def _modify_package_schema(self, schema):
        default_validators = [toolkit.get_validator('ignore_missing'),
                              toolkit.get_converter('convert_to_extras')]

        schema.update({
            'publisher': default_validators,
            'publication_year': [toolkit.get_validator('ignore_empty'),
                                 toolkit.get_validator('ckanext_lcrnz_is_year'),
                                 toolkit.get_converter('convert_to_extras')],
            'start_date': [toolkit.get_validator('ignore_empty'),
                           toolkit.get_validator('ckanext_lcrnz_is_date'),
                           toolkit.get_converter('convert_to_extras')],
            'end_date': [toolkit.get_validator('ignore_empty'),
                         toolkit.get_validator('ckanext_lcrnz_is_date'),
                         toolkit.get_converter('convert_to_extras')],
            'doi': default_validators,
        })
        return schema

    def create_package_schema(self):
        schema = super(NewZealandLandcarePlugin, self).create_package_schema()
        return self._modify_package_schema(schema)

    def update_package_schema(self):
        schema = super(NewZealandLandcarePlugin, self).update_package_schema()
        return self._modify_package_schema(schema)

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
        return map

    def update_config(self, config):
        # from the IConfigurer interface, we're telling ckan
        # where our templates are kept in this pluign
        toolkit.add_template_directory(config, 'templates')

        # add our extension's public directory, to include the custom css file
        toolkit.add_public_directory(config, 'public')

    def get_validators(self):
        return {
            'ckanext_lcrnz_is_year': validators.is_year,
            'ckanext_lcrnz_is_date': validators.is_date
        }
