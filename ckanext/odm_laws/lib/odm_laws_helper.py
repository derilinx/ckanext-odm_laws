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
			't0': toolkit._("Thank you for uploading this item. Instructions about vetting system available on https://wiki.opendevelopmentmekong.net/partners:content_review#instructions_for_default_issue_on_law_records")
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

def get_values_from_datatable(resource_id,field_id,field_value):
  ''' pulls tabular data from datastore '''

  result = toolkit.get_action('datastore_search')(data_dict={'resource_id': resource_id})

  return result['records']

session = {}
