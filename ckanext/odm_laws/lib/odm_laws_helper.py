#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pylons
import logging
import json

document_types = [
  ('advocacy_and_promotional_materials','Advocacy and promotional materials'),
  ('analysis_discussion_papers_and_blogs','Analysis, discussion papers, and blogs'),
  ('books_and_book_chapters','Books and book chapters'),
  ('case_studies','Case studies'),
  ('issue_and_policy_briefs','Issue and policy briefs'),
  ('profiles_people','Profiles - People'),
  ('profiles_organizations_and_projects','Profiles - Organizations  and projects'),
  ('profiles_geographical_areas_and_sites','Profiles - Geographical areas and sites'),
  ('conference_workshops_proceedings_and_presentations','Conference/workshop proceedings and presentations'),
  ('reports_journal_articles_and_research_papers','Reports, journal articles, and research papers (including theses and dissertations)')
]

laws_fields = [
  ('document_type','Document type',False),
  ('odm_laws_short_title','Alternative/Short Title',True),
  ('odm_laws_number','Legal document #',False),
  ('odm_laws_drafting_agency','Known Drafting Agency', False),
  ('odm_laws_draft_assistance','Technical assistance for drafting',False),
  ('odm_laws_technical_assistance','Agency providing technical assistance',False),
  ('odm_laws_implementing_agency','Implementing Agency',False),
  ('odm_laws_primary_policy_reference_point','Primary policy reference point',False),
  ('odm_laws_status','Status',True),
  ('odm_laws_version_date','Version date',False),
  ('odm_laws_date_of_enactment','Date of enactment', False),
  ('odm_laws_final_action','Date final action necessary to formalize Policy',False),
  ('odm_laws_efective_date','Effective Date (if adopted)',False),
  ('odm_laws_action_previous_law','Does this law replace, amend or supplement previous law',False),
  ('odm_laws_action_previous_law_description','Describe what changed',False),
  ('odm_laws_relationship_type','Add Relationship to other Document', False),
  ('odm_laws_relationship_target','Associated Document', False),
  ('odm_laws_official_publication_reference','Official publication reference (if exists)',False),
  ('odm_laws_source','Official Link to Source',False),
  ('odm_laws_notes','Notes',False)

]

odc_fields = [
  ('file_name_kh','File (Khmer)',False),
  ('file_name_en','File (English)',False),
  ('adopted_date','Adopted Date',False),
  ('number_en','Number (English)',False),
  ('number_kh','Number (Khmer)',False),
  ('published_date','Publication date',False),
  ('published_under','Published under',False)
]

metadata_fields = [
  ('odm_copyright','Copyright',False),
  ('odm_access_and_use_constraints','Access and Use Constraints',False),
  ('odm_contact','Contact',False),
  ('odm_language','Language',True),
  ('odm_date_uploaded','Date Uploaded',True),
  ('odm_spatial_range','Geographic area (Spatial Range)',True),
  ('odm_version', 'Draft Version', True)
]

ckan_fields= [
  ('version','Version',True)
]

def get_document_types():
  '''Return a list of document types'''

  log.debug('get_document_types')

  return document_types

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

DATASET_TYPE_NAME = 'laws_record'

def get_dataset_type():
  '''Return the dataset type'''

  log.debug('get_dataset_type')

  return DATASET_TYPE_NAME

session = {}
