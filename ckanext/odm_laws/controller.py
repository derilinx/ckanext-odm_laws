import ckan.plugins as p
import logging
import ckan.lib.helpers as h
import plugin as odm_laws
from ckan.lib.base import BaseController, render
import ckan.model as model
from ckan.common import c, request
from ckan.controllers.package import PackageController
from ckanext.odm_laws.plugin import DATASET_TYPE_NAME

log = logging.getLogger(__name__)

class LawsController(PackageController):

  def new(self, data=None, errors=None, error_summary=None):

    log.debug('LawsController new')


    return super(LawsController, self).new(data=data, errors=errors,error_summary=error_summary)


  def search(self):

    log.debug('LawsController search')

    def remove_field(key, value=None, replace=None):
      return h.remove_url_param(key, value=value, replace=replace,controller='ckanext.odm_laws.controller:LawsController', type='laws_record', action='search')

    c.remove_field = remove_field

    return super(LawsController, self).search()

  def read(self, id, format='html'):

    log.debug('LawsController read')

    return super(LawsController, self).read(id=id,format=format)


  def edit(self, id, data=None, errors=None, error_summary=None):

    log.debug('LawsController edit')
    log.debug('LawsController NBEW')
    log.debug(LawsController)

    return super(LawsController, self).edit(id, data=data, errors=errors,error_summary=error_summary)

  def delete(self, id):

    log.debug('LawsController delete')

    return super(LawsController, self).delete(id)

  def new_resource(self, id, data=None, errors=None, error_summary=None):

    log.debug('LawsController new_resource')

    return super(LawsController, self).new_resource(id, data=data, errors=errors, error_summary=error_summary)

  def _guess_package_type(self, expecting_name=False):

    log.debug('LawsController _guess_package_type')

    return DATASET_TYPE_NAME
