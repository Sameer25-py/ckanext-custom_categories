import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.plugins.toolkit import Invalid
import ckan.lib.helpers as h


# Category Validator
def check_empty(key, data, errors, context):
    if not data.get(key, None):
        errors[key].append('Category field is empty')
    return

# Template Helper Functions


def get_allCategories():
    categories = ['Health', 'Economy & Finance', 'Demography', 'Environment & Energy', 'Public Safety', 'Education',
                  'Government & Public Sector', 'Agriculture, Food & Forests', 'Cities & Regions', 'Connectivity',
                  'Housing & Public Sector', 'Culture', 'Manufecturing', 'Science & Technology']

    return categories


class Custom_CategoriesPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IFacets)
    plugins.implements(plugins.ITemplateHelpers)
    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'custom_categories')

    # IDatasetForm

    def create_package_schema(self):
        schema = super(Custom_CategoriesPlugin, self).create_package_schema()
        schema.update({
            'custom_category': [check_empty, toolkit.get_converter('convert_to_extras')]
        })
        return schema

    def update_package_schema(self):
        schema = super(Custom_CategoriesPlugin, self).update_package_schema()
        schema.update({
            'custom_category': [toolkit.get_converter('convert_to_extras')]
        })
        return schema

    def show_package_schema(self):
        schema = super(Custom_CategoriesPlugin, self).show_package_schema()
        schema.update({
            'custom_category': [toolkit.get_converter('convert_from_extras'), check_empty]
        })
        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    # IFacets

    def dataset_facets(self, facets_dict, package_type):
        facets_dict['custom_category'] = toolkit._('Categories')
        return facets_dict

    def organization_facets(self, facets_dict, organization_type, package_type):
        return facets_dict

    # ITemplateHelpers

    def get_helpers(self):
        return {
            "get_allCategories": get_allCategories
        }
