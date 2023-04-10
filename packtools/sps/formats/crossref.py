# coding: utf-8
from lxml import etree as ET
import re
import os
import uuid
from copy import deepcopy
from datetime import datetime

from packtools.sps.models import journal_meta, dates, front_articlemeta_issue

SUPPLBEG_REGEX = re.compile(r'^0 ')
SUPPLEND_REGEX = re.compile(r' 0$')


def pipeline_crossref(xml_tree, data):
    xml_crossref = setupdoibatch_pipe()
    xml_head_pipe(xml_crossref)
    xml_doibatchid_pipe(xml_crossref, data)
    xml_timestamp_pipe(xml_crossref, data)
    xml_depositor_pipe(xml_crossref, data)
    xml_registrant_pipe(xml_crossref, data)
    xml_body_pipe(xml_crossref)
    xml_journal_pipe(xml_crossref)
    xml_journalmetadata_pipe(xml_tree, xml_crossref)
    xml_journaltitle_pipe(xml_tree, xml_crossref)
    xml_abbreviatedjournaltitle_pipe(xml_tree, xml_crossref)
    xml_issn_pipe(xml_tree, xml_crossref)
    xml_journalissue_pipe(xml_tree, xml_crossref)
    xml_pubdate_pipe(xml_tree, xml_crossref)
    xml_journalvolume_pipe(xml_crossref)
    xml_volume_pipe(xml_tree, xml_crossref)
    xml_issue_pipe(xml_tree, xml_crossref)
    # xml_journalarticle_pipe(xml_tree, xml_crossref)
    # xml_articletitles_pipe(xml_tree, xml_crossref)
    # xml_articletitle_pipe(xml_tree, xml_crossref)
    # xml_articlecontributors_pipe(xml_tree, xml_crossref)
    # xml_articleabstract_pipe(xml_tree, xml_crossref)
    # xml_articlepubdate_pipe(xml_tree, xml_crossref)
    # xml_pages_pipe(xml_tree, xml_crossref)
    # xml_pid_pipe(xml_tree, xml_crossref)
    # xml_elocation_pipe(xml_tree, xml_crossref)
    # xml_permissions_pipe(xml_tree, xml_crossref)
    # xml_programrelateditem_pipe(xml_tree, xml_crossref)
    # xml_doidata_pipe(xml_tree, xml_crossref)
    # xml_doi_pipe(xml_tree, xml_crossref)
    # xml_resource_pipe(xml_tree, xml_crossref)
    # xml_collection_pipe(xml_tree, xml_crossref)
    # xml_articlecitations_pipe(xml_tree, xml_crossref)
    # xml_close_pipe(xml_tree, xml_crossref)

    return xml_crossref


