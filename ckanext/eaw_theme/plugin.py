from collections import OrderedDict
import ckan.plugins as plugins
import ckan.plugins.toolkit as tk
from ckan.lib.plugins import DefaultTranslation
from ckan.lib.helpers import linked_user
import logging
from json import loads
import re

logger = logging.getLogger(__name__)

# This is a workaround issue  #2713
# https://github.com/ckan/ckan/issues/2713
def new_facet_dict(facet_dict, new_facets):
    for e in facet_dict:
        del facet_dict[e]
    for k, v in new_facets:
        facet_dict[k] = v
    return facet_dict

# template helper functions

def eaw_theme_get_spatial_query_default_extent():
    extent_s = tk.config.get('ckanext.eaw_theme.spatial_query_default_extent')
    try:
        extent = loads(extent_s)
    except:
        extent =  [[-40.0, -20.], [60.0, 20.]]
    return extent

def eaw_theme_get_default_dataset_type(organization_id):
    '''Returns the [default] dataset type of an organization'''
    default_pkg_type = tk.get_action('organization_show')(
        data_dict={
            'id': organization_id,
            'include_extras': True,
            'include_users': False,
            'include_groups': False,
            'include_tags': False,
            'include_followers': False
            }).get('default_package_type', 'dataset')
    return default_pkg_type

def eaw_theme_patch_activity_actor(actor):
    '''Patches an activity_item actor string to replace the
    image source at gravatar.com with the Eawag picture.

    '''
    newusername = re.search(
        r'<a\s*href="/user/(.*?)"\s*>', actor, flags=re.S)
    try:
        newusername = newusername.group(1)
    except AttributeError:
        newusername = 'unknown user'
        logger.warn("faild to extract username")
    eawuserpic = eaw_theme_geteawuser(newusername)
    try:
        eawuserpic = eawuserpic.get('pic_url', '')
    except AttributeError:
        logger.warn("Could not find Eawag user picture")
        eawuserpic = ''
    newactor = re.sub(
        '<\s*img\s*.*?/\s*>',
        '<img src="{}" width="30px height="30px"/>'.format(eawuserpic),
        actor, flags=re.S).unescape()
    return newactor

def eaw_theme_patch_linked_user(user, maxlength=0, avatar=20):
    res = linked_user(user, maxlength=0, avatar=20)
    # Get the username in case <user> is the id
    username = tk.get_action('user_show')(data_dict={'id': user})['name']
    eawuserpic = eaw_theme_geteawuser(username)
    try:
        eawuserpic = eawuserpic.get('pic_url', '')
    except AttributeError:
        logger.warn("Could not find Eawag user picture")
        eawuserpic = ''
    else:
        res = re.sub('src="[^"]*?"',
                     'src={}'.format(eawuserpic),
                     res, flags=re.S)
    return res

# A copy & paste from ckanext-eaw_schema (eaw_schema_geteawuser)
# for better modularity
def eaw_theme_geteawuser(username):
    """Returns info about Eawag user:
       + link to picture
       + link to homepage of user
       + ...

    """

    pic_url_prefix = ("https://www.eawag.ch/fileadmin/user_upload/"
                      "tx_userprofiles/profileImages/")
    def geteawhp(fullname):
        "Returns the Eawag homepage of somebody"
        hp_url_prefix = ('https://www.eawag.ch/en/aboutus/portrait/'
                         'organisation/staff/profile/')
        # If we can't derive the Eawag personal page, go to search page.
        hp_url_fallback_template = ('https://www.eawag.ch/en/suche/'
                                    '?q=__NAME__&tx_solr[filter][0]'
                                    '=filtertype%3A3')
        try:
            last, first = fullname.split(',')
        except (ValueError, AttributeError):
            if not isinstance(fullname, str):
                fullname = 'not a string'
            logger.warn('User Fullname "{}" does not '
                        'have standard format ("lastname, firstname")'
                        .format(fullname))
            return hp_url_fallback_template.replace('__NAME__', fullname)
            
        normname = '-'.join([s.strip().lower() for s in [first, last]])
        return hp_url_prefix + normname

    try:
        userdict = tk.get_action('user_show')(data_dict={'id': username})
    except:
       return None
    eawuser = {'fullname': userdict.get('fullname'), 'email': userdict.get('email'),
               'no_of_packages': userdict.get('number_created_packages'),
               'homepage': geteawhp(userdict.get('fullname')),
               'pic_url': '{}{}.jpg'.format(pic_url_prefix, username)}
    return eawuser

    
class Eaw_ThemePlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IFacets)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IPackageController, inherit=True)
    

    # IConfigurer
    def update_config(self, config_):
        tk.add_template_directory(config_, 'templates')
        tk.add_public_directory(config_, 'public')
        tk.add_resource('fanstatic/vendor/bootstrap-switch', 'bootstrap-switch')
        tk.add_resource('fanstatic', 'eaw_theme')

    # IFacets
    def dataset_facets(self, facet_dict, package_type):
         new_facets = [('organization', 'Organizations'),
                       ('groups', 'Projects'),
                       ('tags', 'Keywords'),
                       ('variables', 'Variables'),
                       ('systems', 'Systems'),
                       ('substances', 'Substances'),
                       ('taxa', 'Taxa')]
         return new_facet_dict(facet_dict, new_facets)

    def group_facets(self, facet_dict, group_type, package_type):
        new_facets =  [('organization', 'Organizations'),
                       ('tags', 'Keywords'),
                       ('variables', 'Variables'),
                       ('systems', 'Systems'),
                       ('substances', 'Substances'),
                       ('taxa', 'Taxa')]
        return new_facet_dict(facet_dict, new_facets)

    def organization_facets(self, facet_dict, organization_type, package_type):
        new_facets =  [('groups', 'Projects'),
                       ('tags', 'Keywords'),
                       ('variables', 'Variables'),
                       ('systems', 'Systems'),
                       ('substances', 'Substances'),
                       ('taxa', 'Taxa')]
        return new_facet_dict(facet_dict, new_facets)


    #ITemplateHelpers
    def get_helpers(self):
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {'eaw_theme_get_spatial_query_default_extent':
                eaw_theme_get_spatial_query_default_extent,
                'eaw_theme_get_default_dataset_type':
                eaw_theme_get_default_dataset_type,
                'eaw_theme_patch_activity_actor':
                eaw_theme_patch_activity_actor,
                'eaw_theme_geteawuser':
                eaw_theme_geteawuser,
                'eaw_theme_patch_linked_user':
                eaw_theme_patch_linked_user}

    # IPackageController
    def before_search(self, search_params):
        search_params.update({
            'sort': search_params.get('sort', 'mydefaultsortparam asc')
        })
        return search_params

        
