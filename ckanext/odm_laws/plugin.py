import ckan
import pylons
import logging
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from beaker.middleware import SessionMiddleware
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
import odm_laws_helper
from urlparse import urlparse
import json
import collections
from routes.mapper import SubMapper
import ckan.lib.helpers as h

log = logging.getLogger(__name__)

class OdmLawsPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
  '''OD Mekong laws plugin.'''

  plugins.implements(plugins.IConfigurer)
  plugins.implements(plugins.ITemplateHelpers)
  plugins.implements(plugins.IRoutes, inherit=True)
  plugins.implements(plugins.IFacets)
  plugins.implements(plugins.IPackageController, inherit=True)

  def __init__(self, *args, **kwargs):

    log.debug('OdmLawsPlugin init')
    wsgi_app = SessionMiddleware(None, None)
    odm_laws_helper.session = wsgi_app.session

  def dataset_facets(self, facets_dict, package_type):

    facets_dict = {
              'license_id': toolkit._('License'),
              'vocab_taxonomy': toolkit._('Topics'),
              'organization': toolkit._('Organizations'),
              'groups': toolkit._('Groups'),
              'res_format': toolkit._('Formats'),
              'odm_language': toolkit._('Language'),
              'odm_spatial_range': toolkit._('Country')
              }

    return facets_dict

  def group_facets(self, facets_dict, group_type, package_type):

    group_facets = {
              'license_id': toolkit._('License'),
              'vocab_taxonomy': toolkit._('Topics'),
              'organization': toolkit._('Organizations'),
              'res_format': toolkit._('Formats'),
              'odm_language': toolkit._('Language'),
              'odm_spatial_range': toolkit._('Country')
              }

    return group_facets

  def organization_facets(self, facets_dict, organization_type, package_type):

    organization_facets = {
              'license_id': toolkit._('License'),
              'vocab_taxonomy': toolkit._('Topics'),
              'groups': toolkit._('Groups'),
              'res_format': toolkit._('Formats'),
              'odm_language': toolkit._('Language'),
              'odm_spatial_range': toolkit._('Country')
              }

    return organization_facets

  def before_map(self, m):

    m.connect('odm_laws_index','/laws',
      controller='ckanext.odm_laws.controller:LawsController',type='laws_record',action='search')

    m.connect('odm_laws_new','/laws/new',
      controller='ckanext.odm_laws.controller:LawsController',type='laws_record',action='new')

    m.connect('odm_laws_new_resource','/laws/new_resource/{id}',
      controller='ckanext.odm_laws.controller:LawsController',type='laws_record',action='new_resource')

    m.connect('odm_laws_read', '/laws/{id}',
      controller='ckanext.odm_laws.controller:LawsController',type='laws_record', action='read', ckan_icon='book')

    m.connect('odm_laws_edit', '/laws/edit/{id}',
      controller='ckanext.odm_laws.controller:LawsController',type='laws_record', action='edit')

    m.connect('odm_laws_delete', '/laws/delete/{id}',
      controller='ckanext.odm_laws.controller:LawsController',type='laws_record', action='delete')

    return m

  def update_config(self, config):
    '''Update plugin config'''

    toolkit.add_template_directory(config, 'templates')
    toolkit.add_resource('fanstatic', 'odm_laws')
    toolkit.add_public_directory(config, 'public')

  def get_helpers(self):
    '''Register the plugin's functions above as a template helper function.'''

    return {
      'odm_laws_last_dataset': odm_laws_helper.last_dataset,
      'odm_laws_get_dataset_type': odm_laws_helper.get_dataset_type,
      'odm_laws_lookup_relationship_target': odm_laws_helper.lookup_relationship_target,
      'odm_laws_semre_of_database_relationships': odm_laws_helper.semre_of_database_relationships,
      'odm_laws_get_dataset_name': odm_laws_helper.get_dataset_name,
      'odm_laws_get_dataset_notes' : odm_laws_helper.get_dataset_notes
    }

  def is_fallback(self):
    return False

  def package_types(self):
    return ['laws_record']

  def new_template(self):
    return 'laws/new.html'

  def read_template(self):
    return 'laws/read.html'

  def edit_template(self):
    return 'laws/edit.html'

  def search_template(self):
    return 'laws/search.html'

  def package_form(self):
    return 'laws/new_package_form.html'

  def resource_form(self):
    return 'laws/snippets/resource_form.html'

  def before_create(self, context, resource):
    log.info('before_create')

    odm_laws_helper.session['last_dataset'] = None
    odm_laws_helper.session.save()

  def after_create(self, context, pkg_dict):
    log.debug('after_create: %s', pkg_dict['name'])

    odm_laws_helper.session['last_dataset'] = pkg_dict
    odm_laws_helper.session.save()

  def after_update(self, context, pkg_dict):
    log.debug('after_update: %s', pkg_dict['name'])

    #  Create relationship if target is set
    if 'odm_laws_relationship_target' in pkg_dict:
      # current dataset
      rel_subj=pkg_dict['name']
      # is child of/parent of
      rel_type=pkg_dict['odm_laws_relationship_type']
      # relationship target
      rel_target=pkg_dict['odm_laws_relationship_target']

      log.debug("Creating relationship %s %s",rel_type,rel_target)
      toolkit.get_action('package_relationship_create')(data_dict={'subject': rel_subj,'object':rel_target,'type':rel_type})

    odm_laws_helper.session['last_dataset'] = pkg_dict
    odm_laws_helper.session.save()
