import ckan.plugins as p
import logging
import ckan.lib.helpers as h
import plugin as odm_library
from ckan.lib.base import BaseController, render
import ckan.model as model
from ckan.common import c, request
from ckan.controllers.package import PackageController
from ckanext.odm_library.plugin import DATASET_TYPE_NAME

log = logging.getLogger(__name__)

class LibraryController(PackageController):

  def new(self, data=None, errors=None, error_summary=None):

    log.debug('LibraryController new')

    return super(LibraryController, self).new(data=data, errors=errors,error_summary=error_summary)

  def search(self):

    log.debug('LibraryController search')

    def remove_field(key, value=None, replace=None):
      return h.remove_url_param(key, value=value, replace=replace,controller='ckanext.odm_library.controller:LibraryController', type='library_record', action='search')

    c.remove_field = remove_field

    return super(LibraryController, self).search()

  def read(self, id, format='html'):

    log.debug('LibraryController read')

    return super(LibraryController, self).read(id=id,format=format)

  def edit(self, id, data=None, errors=None, error_summary=None):

    log.debug('LibraryController edit')

    return super(LibraryController, self).edit(id, data=data, errors=errors,error_summary=error_summary)

  def delete(self, id):

    log.debug('LibraryController delete')

    return super(LibraryController, self).delete(id)

  def new_resource(self, id, data=None, errors=None, error_summary=None):

    log.debug('LibraryController new_resource')

    return super(LibraryController, self).new_resource(id, data=data, errors=errors, error_summary=error_summary)

  def _guess_package_type(self, expecting_name=False):

    log.debug('LibraryController _guess_package_type')

    return DATASET_TYPE_NAME
