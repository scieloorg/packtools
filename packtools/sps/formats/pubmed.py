# coding: utf-8
from lxml import etree as ET

from packtools.sps.models import (
    journal_meta,
    front_articlemeta_issue,
    dates,
    article_titles,
    article_ids,
    article_and_subarticles,
)


def xml_pubmed_article_pipe():
    root = ET.Element("Article")
    tree = ET.ElementTree(root)

    return tree


def xml_pubmed_journal_pipe(xml_pubmed):
    el = ET.Element('Journal')
    xml_pubmed.append(el)


