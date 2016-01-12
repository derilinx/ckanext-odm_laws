#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pylons
import logging
import json
import logging
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from genshi.template.text import NewTextTemplate
from ckan.lib.base import render

log = logging.getLogger(__name__)

def get_dataset_type():
  '''Return the dataset type'''

  log.debug('get_dataset_type')

  return 'laws_record'

def create_default_issue_laws_record(pkg_info):
  ''' Uses CKAN API to add a default Issue as part of the vetting workflow for library records'''
  try:

    extra_vars = {
        't0': toolkit._("Thank you for uploading the library item. You should have received a confirmation email from OD Mekong Datahub. This library item is still unpublished. Your item can only be published after you review this form and after our administrators approve your entry."),
        't1': toolkit._("It is important that you have entered the correct information in your library record form. We also ask that all contributors complete as many fields as possible."),
        't2': toolkit._("Please take this opportunity to review your library record. If you would like to make any changes please select your library record and then click on the Manage button on the top right corner."),
        't3': toolkit._("Please CHECK YOUR SPELLING against the original item to ensure the item is recorded correctly."),
        't4': toolkit._("Please review your library record form again for the mandatory fields:"),
        't5': toolkit._("Title (Please use Associated Press style title where the first letter is capitalized and the rest of the title is not, i.e. 'Study of Cambodian forests and lakes from 1992 to 1994')"),
        't6': toolkit._("Language"),
        't7': toolkit._("Edition / Version"),
        't8': toolkit._("Geographical area"),
        't9': toolkit._("Date uploaded"),
        't10': toolkit._("Please review again the following information, vital to other users who may search for your record:"),
        't11': toolkit._("Summary (Make sure this is a concise description of the record in your own words, please do not just 'copy' and 'paste' an abstract by the original author)"),
        't12': toolkit._("Topics"),
        't13': toolkit._("License (Make sure you indicated the correct license. Additional information on creative commons is found here http://opendefinition.org/licenses/. If there is no license, please indicate 'license unspecified')"),
        't14': toolkit._("Copyright"),
        't15': toolkit._("Access and Use Constraints"),
        't16': toolkit._("Author"),
        't17': toolkit._("Co-author"),
        't18': toolkit._("Corporate Author"),
        't19': toolkit._("Publisher"),
        't20': toolkit._("Lastly, please check again for the following information on the library record you entered. If the information is available, please include it in the appropriate field. This will greatly improve the searchability of your library record item or provide information that a user will find useful:"),
        't21': toolkit._("ISSN or ISBN numbers"),
        't22': toolkit._("Publication Place"),
        't23': toolkit._("Publication Date"),
        't24': toolkit._("Pagination"),
        't25': toolkit._("Our administrators need to review the library record as well. They will close fixed issues or open new issues if there are any other inconsistencies. Once all issues have been closed, the item will be published."),
        't26': toolkit._("Thank you for sharing,"),
        't27': toolkit._("Open Development Team")
    }

    issue_message = render('messages/default_issue_laws_record.txt',extra_vars=extra_vars,loader_class=NewTextTemplate)

    params = {'title':'User Laws record Upload Checklist','description':issue_message,'dataset_id':pkg_info['id']}
    toolkit.get_action('issue_create')(data_dict=params)

  except KeyError:

    log.error("Action 'issue_create' not found. Please make sure that ckanext-issues plugin is installed.")

def get_dataset_name(dataset_id):

  dataset_dict = toolkit.get_action('package_show')(data_dict={'id':dataset_id})
  return dataset_dict['name']

def get_dataset_notes(dataset_id, truncate):

  notes = None
  dataset_dict = toolkit.get_action('package_show')(data_dict={'id':dataset_id})

  if 'notes_translated' in dataset_dict :
    lang = pylons.request.environ['CKAN_LANG']
    if lang in dataset_dict['notes_translated']:
      notes = dataset_dict['notes_translated'][lang]
      if truncate == True and notes:
        notes = notes[0:99]

  return notes

def lookup_relationship_target():
  result = toolkit.get_action('package_search')(data_dict={'fq': '+type:laws_record'})
  return map(lambda x:x["name"], result['results'])

def semre_of_database_relationships(dataset_id,viewpoint):
  ''' semantic representation of relationships '''

  if not dataset_id:
    return []

  dataset_dict = toolkit.get_action('package_show')(data_dict={'id':dataset_id})
  relationships = []

  if viewpoint == 'object':
    relationships = dataset_dict['relationships_as_object']
  elif viewpoint == 'subject':
    relationships = dataset_dict['relationships_as_subject']

  return relationships

session = {}
