#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pylons
import logging
import json
import logging
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

log = logging.getLogger(__name__)

DATASET_TYPE_NAME = 'laws_record'

def last_dataset():
  ''' Returns the last dataset info stored in session'''

  if 'last_dataset' in session:
   return session['last_dataset']

  return None

def get_dataset_name(dataset_id):

  log.debug("dataset_idxs %s",dataset_id)
  # get dataset dict
  dataset_dict = toolkit.get_action('package_show')(data_dict={'id':dataset_id})
  resource_dict= dataset_dict['resources']
  # return name for the id
  # return resource_dict[0]['name']
  return resource_dict

def get_dataset_notes(dataset_id, truncate):
  dataset_dict = toolkit.get_action('package_show')(data_dict={'id':dataset_id})

  if 'notes' in dataset_dict :
      notes = dataset_dict['notes']

  # show only first 100 characters of the notes field

      if dataset_dict['notes'] !='none' and truncate == 'true':

          notes_trunc = notes[0:100]
          return notes_trunc
      else:
          return notes
  else:
      return ''

def lookup_relationship_target():

  # Get a list of all the site's datasets from CKAN,
  datasets = toolkit.get_action('package_list')(data_dict={'all_fields': True})
  return datasets

# semantic representation of relationships
def semre_of_database_relationships(c,viewpoint):
    #get the id of current editing dataset
    id=c.id
    # get dataset info
    dataset_dict = toolkit.get_action('package_show')(data_dict={'id':id})
    if viewpoint == 'object':
        result=dataset_dict['relationships_as_object']
    elif viewpoint == 'subject':
        result=dataset_dict['relationships_as_subject']
    else:
        log.error('Relationship Viewpoint not specified')
        return false
    return result

def get_dataset_type():
  '''Return the dataset type'''

  log.debug('get_dataset_type')

  return DATASET_TYPE_NAME

session = {}
