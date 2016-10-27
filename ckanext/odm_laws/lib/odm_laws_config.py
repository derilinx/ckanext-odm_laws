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

def get_resource_id_for_field(field):

	resource_ids = {
		'odm_laws_status': '717ae4f5-8abc-4959-99a0-aa2497ce776f',
		'odm_document_type': 'b25a6083-0c5e-4ec6-8aa7-a343fc7546b0',
		'odm_laws_implementing_agencies': '88bfd7e3-adf2-4705-a8a6-fa3a64324401',
		'odm_laws_issuing_agency_parties': '302c89d2-f238-4e73-8ceb-714ff7238c77'
	}

	return resource_ids[field]
