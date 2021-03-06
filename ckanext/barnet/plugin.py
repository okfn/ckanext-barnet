import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.barnet.logic import schema as barnet_schema
from ckanext.barnet.logic import auth
from ckanext.barnet import template_helpers

class BarnetPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    '''Barnet theme plugin.

    '''
    # Declare that this class implements IConfigurer.
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IAuthFunctions, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)

    def update_config(self, config):

        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        # 'templates' is the path to the templates dir, relative to this
        # plugin.py file.
        toolkit.add_template_directory(config, 'theme_1/templates')
        
        # Add this plugin's public dir to CKAN's extra_public_paths, so
        # that CKAN will use this plugin's custom static files.
        toolkit.add_public_directory(config, 'theme_1/public')

        # Stuff that both theme_1 and theme_2 need.
        toolkit.add_public_directory(config, 'public')
        
        # Register this plugin's fanstatic directory with CKAN.
        # Here, 'fanstatic' is the path to the fanstatic directory
        # (relative to this plugin.py file), and 'example_theme' is the name
        # that we'll use to refer to this fanstatic directory from CKAN
        # templates.
        toolkit.add_resource('theme_1/resources', 'barnet-theme')

    def dataset_facets(self, facets_dict, package_type):
        facets_dict.pop('organization', None)
        return facets_dict

    def create_package_schema(self):
        return barnet_schema.package_create_schema()

    def update_package_schema(self):
        return barnet_schema.package_update_schema()

    def show_package_schema(self):
        return barnet_schema.package_show_schema()

    def is_fallback(self):
        return True

    def package_types(self):
        return []

    # IRoutes

    def before_map(self, map_):
        map_.connect(
            "/dataset/export.csv",
            controller="ckanext.barnet.controllers:CSVExportController",
            action="export",
        )
        map_.connect(
            'register',
            '/user/register', 
            controller='ckanext.barnet.controllers:BarnetUserController',
            action='register'
        )
        return map_

    def get_auth_functions(self):
        return {
            'export_csv': auth.export_csv,
            'user_create': auth.user_create,
        }

    def get_helpers(self):
        return {
            'convert_to_british_date_format': 
                template_helpers.convert_to_british_date_format 
        }
