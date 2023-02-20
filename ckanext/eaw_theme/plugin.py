from collections import OrderedDict

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation

from ckanext.eaw_core.helpers import (
    eaw_helpers_geteawuser,
    eaw_theme_get_default_dataset_type,
    eaw_theme_get_spatial_query_default_extent,
    eaw_theme_patch_activity_actor,
    eaw_theme_patch_linked_user,
)


class EawThemePlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IFacets)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IPackageController, inherit=True)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "eaw_theme")

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
            "eaw_theme_geteawuser": eaw_helpers_geteawuser,
            "eaw_theme_patch_linked_user": eaw_theme_patch_linked_user,
        }

    # IPackageController
    def before_search(self, search_params):
        search_params.update(
            {"sort": search_params.get("sort", "mydefaultsortparam asc")}
        )
        return search_params
