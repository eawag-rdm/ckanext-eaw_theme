from collections import OrderedDict

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation

from ckanext.eaw_theme import validators


from ckanext.eaw_core.helpers import (
    eaw_theme_get_default_dataset_type,
    eaw_theme_get_spatial_query_default_extent,
    eaw_theme_patch_activity_actor,
    eaw_theme_patch_linked_user,
    eaw_schema_set_default,
    eaw_schema_get_values,
    eaw_helpers_geteawuser,
    eaw_schema_embargo_interval,
    eaw_username_fullname_email,
    eaw_schema_human_filesize
)

from ckanext.eaw_core.validators import (
    vali_daterange,
    output_daterange,
    eaw_schema_multiple_string_convert,
    eaw_schema_multiple_string_output,
    eaw_schema_multiple_choice,
    eaw_schema_json_not_empty,
    eaw_schema_is_orga_admin,
    eaw_schema_embargodate,
    eaw_schema_publicationlink,
    eaw_schema_striptime,
    eaw_schema_list_to_commasepstring_output,
    eaw_users_exist,
    test_before,
    eaw_schema_cp_filename2name,
    eaw_schema_check_package_type,
    eaw_schema_check_hashtype
)

from ckanext.eaw_core.actions import (
    eaw_schema_datamanger_show
)


class EawThemePlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IFacets)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.IActions)

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
            "eaw_helpers_geteawuser": eaw_helpers_geteawuser,
            "eaw_theme_patch_linked_user": eaw_theme_patch_linked_user,
            'eaw_schema_set_default': eaw_schema_set_default,
            'eaw_schema_get_values': eaw_schema_get_values,
            'eaw_schema_geteawuser': eaw_helpers_geteawuser,
            'eaw_schema_embargo_interval': eaw_schema_embargo_interval,
            'eaw_username_fullname_email': eaw_username_fullname_email,
            'eaw_schema_human_filesize': eaw_schema_human_filesize
        }

    # IPackageController
    def before_search(self, search_params):
        search_params.update(
            {"sort": search_params.get("sort", "mydefaultsortparam asc")}
        )
        return search_params
    
    # IValidators
    def get_validators(self):
        return {
            'repeating_text': validators.repeating_text,
            'repeating_text_output':
                validators.repeating_text_output,
            "vali_daterange":
                vali_daterange,
            "output_daterange":
                output_daterange,
            "eaw_schema_multiple_string_convert":
                eaw_schema_multiple_string_convert,
            "eaw_schema_multiple_string_output":
                eaw_schema_multiple_string_output,
            "eaw_schema_multiple_choice":
                eaw_schema_multiple_choice,
            "eaw_schema_json_not_empty":
                eaw_schema_json_not_empty,
            "eaw_schema_is_orga_admin":
                eaw_schema_is_orga_admin,
            "eaw_schema_embargodate":
                eaw_schema_embargodate,
            "eaw_schema_publicationlink":
                eaw_schema_publicationlink,
            "eaw_schema_striptime":
                eaw_schema_striptime,
            'eaw_schema_list_to_commasepstring_output':
                eaw_schema_list_to_commasepstring_output,
            'eaw_users_exist':
                eaw_users_exist,
            'test_before':
                test_before,
            'eaw_schema_cp_filename2name':
                eaw_schema_cp_filename2name,
            'eaw_schema_check_package_type':
                eaw_schema_check_package_type,
            'eaw_schema_check_hashtype':
                eaw_schema_check_hashtype
            }
    
    # IActions
    def get_actions(self):
        return {'eaw_schema_datamanger_show': eaw_schema_datamanger_show}