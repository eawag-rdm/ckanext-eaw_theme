from collections import OrderedDict

import mimetypes
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation

from ckanext.eaw_theme import validators

from ckanext.eaw_schema.helpers import (
    eaw_helpers_geteawuser,
    eaw_theme_get_default_dataset_type,
    eaw_theme_get_spatial_query_default_extent,
    eaw_theme_patch_activity_actor,
    eaw_theme_patch_linked_user,
)


# Returns boolean indicating wheter organization is department
# (= has empty group field)
# --- CURRENTLY NOT USED ---
def eaw_theme_orga_is_dept(name):
    if tk.get_action('organization_show')(data_dict={'id': name}).get('groups'):
        return False
    else:
        return True
    
# view function for disclaimers (IBlueprint)
def disclaimer(typ):
    try:
        return render_template(u'disclaimer/disclaimer.html', typ=typ)
    except TemplateNotFound:
        abort(404)



class EawThemePlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IFacets)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "eaw_theme")
        mimetypes.add_type('application/x-7z-compressed', '.7z')

    # IFacets
    def dataset_facets(self, facet_dict, package_type):
        new_facets = [
            ("organization", "Organizations"),
            ("groups", "Projects"),
            ("tags", "Keywords"),
            ("variables", "Variables"),
            ("systems", "Systems"),
            ("substances", "Substances"),
            ("taxa", "Taxa"),
        ]
        return OrderedDict(new_facets)

    def group_facets(self, facet_dict, group_type, package_type):
        new_facets = [
            ("organization", "Organizations"),
            ("tags", "Keywords"),
            ("variables", "Variables"),
            ("systems", "Systems"),
            ("substances", "Substances"),
            ("taxa", "Taxa"),
        ]
        return OrderedDict(new_facets)

    def organization_facets(self, facet_dict, organization_type, package_type):
        new_facets = [
            ("groups", "Projects"),
            ("tags", "Keywords"),
            ("variables", "Variables"),
            ("systems", "Systems"),
            ("substances", "Substances"),
            ("taxa", "Taxa"),
        ]
        return OrderedDict(new_facets)

    # ITemplateHelpers
    def get_helpers(self):
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {
            "eaw_theme_get_spatial_query_default_extent": eaw_theme_get_spatial_query_default_extent,
            "eaw_theme_get_default_dataset_type": eaw_theme_get_default_dataset_type,
            "eaw_theme_patch_activity_actor": eaw_theme_patch_activity_actor,
            "eaw_helpers_geteawuser": eaw_helpers_geteawuser,
            "eaw_theme_patch_linked_user": eaw_theme_patch_linked_user,
            'eaw_theme_orga_is_dept': eaw_theme_orga_is_dept  # currently not used
        }

    # IPackageController
    def before_search(self, search_params):
        search_params.update(
            {"sort": search_params.get("sort", "mydefaultsortparam asc")}
        )
        return search_params
    
    # IBlueprint
    def get_blueprint(self):
        bp = Blueprint(u'disclaimer', self.__module__)
        bp.add_url_rule(u'/disclaimer/<typ>', view_func=disclaimer)
        return bp
    
    # IValidators
    def get_validators(self):
        return {
            'repeating_text': validators.repeating_text,
            'repeating_text_output':
                validators.repeating_text_output,
            }
