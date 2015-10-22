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

DATASET_TYPE_NAME = 'laws_record'

def get_document_types():
  '''Return a list of document types'''

  log.debug('get_document_types')

  return odm_laws_helper.document_types

def last_dataset():
  ''' Returns the last dataset info stored in session'''
  if 'last_dataset' in odm_laws_helper.session:
    return odm_laws_helper.session['last_dataset']

  return None

def get_dataset_type():
  '''Return the dataset type'''

  log.debug('get_dataset_type')

  return DATASET_TYPE_NAME

def odc_fields():
  '''Return a list of odc fields'''

  log.debug('odc_fields')

  return odm_laws_helper.odc_fields

def metadata_fields():
  '''Return a list of metadata fields'''

  log.debug('metadata_fields')

  return odm_laws_helper.metadata_fields

def laws_fields():
  '''Return a list of laws fields'''

  log.debug('laws_fields')

  return odm_laws_helper.laws_fields

def validate_not_empty(value,context):
  '''Returns if a string is empty or not'''

  log.debug('validate_not_empty: %s', value)

  if not value or len(value) is None:
    raise toolkit.Invalid('Missing value')
  return value

class OdmLawsPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
  '''OD Mekong laws plugin.'''

  plugins.implements(plugins.IDatasetForm)
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
      'odm_laws_document_types': get_document_types,
      'odm_laws_odc_fields': odc_fields,
      'odm_laws_metadata_fields': metadata_fields,
      'odm_laws_last_dataset': last_dataset,
      'odm_laws_get_dataset_type': get_dataset_type,
      'odm_laws_laws_fields': laws_fields
    }

  def _modify_package_schema_write(self, schema):

    for metadata_field in odm_laws_helper.metadata_fields:
      validators_and_converters = [toolkit.get_validator('ignore_missing'),toolkit.get_converter('convert_to_extras'), ]
      if metadata_field[2]:
        validators_and_converters.insert(1,validate_not_empty)
      schema.update({metadata_field[0]: validators_and_converters})

    for odc_field in odm_laws_helper.odc_fields:
      validators_and_converters = [toolkit.get_validator('ignore_missing'),toolkit.get_converter('convert_to_extras'), ]
      if odc_field[2]:
        validators_and_converters.insert(1,validate_not_empty)
      schema.update({odc_field[0]: validators_and_converters})

    for laws_field in odm_laws_helper.laws_fields:
      validators_and_converters = [toolkit.get_validator('ignore_missing'),toolkit.get_converter('convert_to_extras'), ]
      if laws_field[2]:
        validators_and_converters.insert(1,validate_not_empty)
      schema.update({laws_field[0]: validators_and_converters})

    for ckan_field in odm_laws_helper.ckan_fields:
      validators_and_converters = [toolkit.get_validator('ignore_missing'),toolkit.get_converter('convert_to_extras'), ]
      if ckan_field[2]:
        validators_and_converters.insert(1,validate_not_empty)
      schema.update({ckan_field[0]: validators_and_converters})

    schema.update({odm_laws_helper.taxonomy_dictionary: [toolkit.get_validator('ignore_missing'),toolkit.get_converter('convert_to_tags')(odm_laws_helper.taxonomy_dictionary)]})

    return schema

  def _modify_package_schema_read(self, schema):

    for metadata_field in odm_laws_helper.metadata_fields:
      validators_and_converters = [toolkit.get_converter('convert_from_extras'),toolkit.get_validator('ignore_missing')]
      if metadata_field[2]:
        validators_and_converters.append(validate_not_empty)
      schema.update({metadata_field[0]: validators_and_converters})

    for odc_field in odm_laws_helper.odc_fields:
      validators_and_converters = [toolkit.get_converter('convert_from_extras'),toolkit.get_validator('ignore_missing')]
      if odc_field[2]:
        validators_and_converters.append(validate_not_empty)
      schema.update({odc_field[0]: validators_and_converters})

    for laws_field in odm_laws_helper.laws_fields:
      validators_and_converters = [toolkit.get_converter('convert_from_extras'),toolkit.get_validator('ignore_missing')]
      if laws_field[2]:
        validators_and_converters.append(validate_not_empty)
      schema.update({laws_field[0]: validators_and_converters})

    for ckan_field in odm_laws_helper.ckan_fields:
      validators_and_converters = [toolkit.get_converter('convert_from_extras'),toolkit.get_validator('ignore_missing')]
      if ckan_field[2]:
        validators_and_converters.append(validate_not_empty)
      schema.update({ckan_field[0]: validators_and_converters})

    schema.update({odm_laws_helper.taxonomy_dictionary: [toolkit.get_converter('convert_from_tags')(odm_laws_helper.taxonomy_dictionary),toolkit.get_validator('ignore_missing')]})

    return schema

  def create_package_schema(self):
    schema = super(OdmLawsPlugin, self).create_package_schema()
    schema = self._modify_package_schema_write(schema)
    return schema

  def update_package_schema(self):
    schema = super(OdmLawsPlugin, self).update_package_schema()
    schema = self._modify_package_schema_write(schema)
    return schema

  def show_package_schema(self):
    schema = super(OdmLawsPlugin, self).show_package_schema()
    schema = self._modify_package_schema_read(schema)
    return schema

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

    odm_laws_helper.session['last_dataset'] = pkg_dict
    odm_laws_helper.session.save()
