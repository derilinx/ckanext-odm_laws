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

def check_required_fields(package):
	'''Checks that the package has all required fields'''

	if DEBUG:
		log.info('check_required_fields: %s', package)

	valid = True

	schema_path = os.path.abspath(os.path.join(__file__, '../../','odm_laws_schema.json'))
	with open(schema_path) as f:
		try:
			schema_json = json.loads(f.read())

			for field in schema_json['dataset_fields']:
				if field["required"] == "true" and not package[field["field_name"]]:
					valid = False
					break

			for resource_field in schema_json['resource_fields']:
				for resource in package["resources"]:
					if resource_field["required"] == "true" and not resource[resource_field["field_name"]]:
						valid = False
						break

		except ValueError as e:
			log.info('invalid json: %s' % e)

	return valid

session = {}
