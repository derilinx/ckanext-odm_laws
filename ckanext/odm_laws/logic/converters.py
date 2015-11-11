import json

import ckan.model as model
import ckan.lib.navl.dictization_functions as df
import ckan.logic.validators as validators

from ckan.common import _

def odm_laws_create_relationship(rel_type, target):

    log.debug('creating relationship %s with target %s', rel_type, target )
    
