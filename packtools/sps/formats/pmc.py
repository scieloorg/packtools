# coding: utf-8
from lxml import etree as ET


def pipeline_pmc(xml_tree):
    xml_pmc_authors(xml_tree)
    xml_pmc_aff(xml_tree)
    xml_pmc_ref(xml_tree)

    return xml_tree


