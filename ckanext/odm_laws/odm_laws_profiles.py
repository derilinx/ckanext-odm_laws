import datetime
import json
from pylons import config
import rdflib
from rdflib import URIRef, BNode, Literal
from rdflib.namespace import Namespace, RDF, XSD, SKOS, RDFS
from geomet import wkt, InvalidGeoJSONException
from ckan.plugins import toolkit
from ckanext.dcat.utils import resource_uri, publisher_uri_from_dataset_dict
from ckanext.dcat.profiles import RDFProfile
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
import odm_rdf_helper
import logging

log = logging.getLogger(__name__)

AGLS = Namespace('http://www.agls.gov.au/agls/terms/')
BIBO = Namespace('http://bibliontology.com/bibo/bibo.php#')
BIBFRAME = Namespace('http://id.loc.gov/ontologies/bibframe.html#')
GC = Namespace('http://www.oegov.org/core/owl/gc#')
DBPEDIA = Namespace('http://dbpedia.org/ontology/')
DCT = Namespace('http://purl.org/dc/terms/')
DCAT = Namespace('http://www.w3.org/ns/dcat#')
FOAF = Namespace('http://xmlns.com/foaf/0.1/')
MREL = Namespace('http://id.loc.gov/vocabulary/relators/')
SCHEMA = Namespace('http://schema.org/')
SPDX = Namespace('http://spdx.org/rdf/terms#')
CRO = Namespace('http://rhizomik.net/ontologies/copyrightonto.owl#')
DOAP = Namespace('http://usefulinc.com/ns/doap#')
EBUCORE = Namespace('https://www.ebu.ch/metadata/ontologies/ebucore/index.html#')
DQM = Namespace('http://semwebquality.org/dqm-vocabulary/v1/dqm#')
DQ = Namespace('http://def.seegrid.csiro.au/isotc211/iso19115/2003/dataquality#')
OMN = Namespace('https://raw.githubusercontent.com/open-multinet/playground-rspecs-ontology/master/omnlib/ontologies/omn.ttl#')
OPUS = Namespace('http://lsdis.cs.uga.edu/projects/semdis/opus#')
PPROC = Namespace('http://contsem.unizar.es/def/sector-publico/pproc.html#')
MD = Namespace('http://def.seegrid.csiro.au/isotc211/iso19115/2003/metadata#')
GN = Namespace('http://www.geonames.org/ontology#')
SKOS = Namespace('https://www.w3.org/2009/08/skos-reference/skos.html#')
SORON = Namespace('http://www.bib.uc3m.es/~fcalzada/soron/soron_content/soron#')

namespaces = {
  'agls': AGLS,
  'bibo': BIBO,
  'bibframe': BIBFRAME,
  'dbpedia': DBPEDIA,
  'gc': GC,
  'dct': DCT,
  'dcat': DCAT,
  'foaf': FOAF,
  'mrel': MREL,
  'schema': SCHEMA,
  'cro': CRO,
  'doap': DOAP,
  'ebucore': EBUCORE,
  'dqm': DQM,
  'dq': DQ,
  'omn': OMN,
  'opus': OPUS,
  'pproc': PPROC,
  'md': MD,
  'gn': GN,
  'skos': SKOS,
  'soron': SORON
}


class ODMDCATBasicProfileLaws(RDFProfile):
  '''
  An RDF profile exposing metadata using standard vocabularies

  More information and specification:

  https://joinup.ec.europa.eu/asset/dcat_application_profile

  '''

  def parse_dataset(self, dataset_dict, dataset_ref):

    # This method does not need to be implemented until Harvesters are needed
    return super(ODMDCATBasicProfileLaws, self).parse_dataset(dataset_dict, dataset_ref)

  def graph_from_dataset(self, dataset_dict, dataset_ref):

    if dataset_dict['type'] != "laws_record":
      return

    log.debug("ODMDCATBasicProfileLaws graph_from_dataset")

    g = self.g

    for prefix, namespace in namespaces.iteritems():
      g.bind(prefix, namespace)

    g.add((dataset_ref, DCT.identifier, Literal(dataset_dict.get('id'))))
    g.add((dataset_ref, DCT.type, Literal(dataset_dict.get('type', 'dataset'))))
    g.add((dataset_ref, RDF.type, DCAT.Dataset))

    # Basic fields
    raw_triples = [
      (dataset_ref, AGLS.documentType, dataset_dict.get('document_type')),
      (dataset_ref, DBPEDIA.documentNumber, dataset_dict.get('odm_document_number')),
      (dataset_ref, DCT.title, dataset_dict.get('title_translated')),
      (dataset_ref, GC.shortTitle, dataset_dict.get('odm_short_title')),
      (dataset_ref, DCT.description, dataset_dict.get('notes_translated')),
      (dataset_ref, CRO.copyright, dataset_dict.get('copyright')),
      (dataset_ref, FOAF.organization, dataset_dict.get('owner_org')),
      (dataset_ref, EBUCORE.contact, dataset_dict.get('contact')),
      (dataset_ref, SKOS.changeNote, dataset_dict.get('odm_laws_previous_changes_notes')),
      (dataset_ref, SORON.citedBy, dataset_dict.get('odm_laws_official_publication_reference')),
      (dataset_ref, SKOS.note, dataset_dict.get('odm_laws_notes')),
      (dataset_ref, PPROC.documentReference, dataset_dict.get('odm_reference_document'))
    ]

    for raw_triple in raw_triples:
      triples = odm_rdf_helper.split_multilingual_object_into_triples(raw_triple)
      for triple in triples:
        g.add(triple)

    #license
    license = URIRef(dataset_dict.get('license_url'))
    g.add((license, DCT.title, Literal(dataset_dict.get('license_title'))))
    g.add((dataset_ref, DCT.license, license))

    # odm_spatial_range
    for item in dataset_dict.get('odm_spatial_range'):
      g.add((dataset_ref, GN.countrycode, Literal(item.upper())))

    #taxonomy
    for term in dataset_dict.get('taxonomy'):
      node = odm_rdf_helper.map_internal_to_standard_taxonomic_term(term)
      if  isinstance(node,URIRef):
        g.add((node,DCT.title, Literal(term)))
      g.add((dataset_ref, FOAF.topic, node))

    #  Lists
    items = [
        ('odm_language', DCT.language, None)
    ]
    self._add_list_triples_from_dict(dataset_dict, dataset_ref, items)

    # Dates
    items = [
        ('odm_promulgation_date',BIBFRAME.legalDate, None)
    ]
    self._add_date_triples_from_dict(dataset_dict, dataset_ref, items)

    # Resources
    for resource_dict in dataset_dict.get('resources', []):

      resource = URIRef(resource_uri(resource_dict))
      g.add((dataset_ref, DCAT.Resources, resource))
      g.add((resource, RDF.type, DCAT.Resource))

      items = [
          ('name', DCT.title, None),
          ('description', DCT.description, None)
      ]
      self._add_triples_from_dict(resource_dict, resource, items)

      #  Lists
      items = [
          ('odm_language', DCT.language, None)
      ]
      self._add_list_triples_from_dict(resource_dict, resource, items)

      # Format
      if '/' in resource_dict.get('format', ''):
        g.add((resource, DCAT.mediaType,
               Literal(resource_dict['format'])))
      else:
        if resource_dict.get('format'):
          g.add((resource, DCT['format'],
                 Literal(resource_dict['format'])))

        if resource_dict.get('mimetype'):
          g.add((resource, DCAT.mediaType,
                 Literal(resource_dict['mimetype'])))

      # URL
      url = resource_dict.get('url')
      download_url = resource_dict.get('download_url')
      if download_url:
        g.add((resource, DCAT.downloadURL, Literal(download_url)))
      if (url and not download_url) or (url and url != download_url):
        g.add((resource, DCAT.accessURL, Literal(url)))

  def graph_from_catalog(self, catalog_dict, catalog_ref):

    # Code maintained on ckanext-odm_dataset
    pass
