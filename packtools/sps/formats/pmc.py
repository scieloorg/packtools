# coding: utf-8
from lxml import etree as ET


def pipeline_pmc(xml_tree):
    xml_pmc_aff(xml_tree)
    xml_pmc_ref(xml_tree)

    return xml_tree


def xml_pmc_aff(xml_tree):
    """
    Remove os elementos 'institution', 'addr-line' e 'country' do XML SciELO.
    Adiciona o conteúdo de 'institution content-type="original"' no XML PMC.

    Parameters
    ----------
    xml_tree : lxml.etree._Element
        Elemento XML no padrão SciELO com os dados de origem, por exemplo:
        <aff id="aff1">
            <label>1</label>
            <institution content-type="original">Universidade Federal do Rio Grande do Sul, Escola de Enfermagem, Programa de Pós-Graduação em Enfermagem, Porto Alegre, RS, Brazil.</institution>
            <institution content-type="orgname">Universidade Federal do Rio Grande do Sul</institution>
            <institution content-type="orgdiv1">Escola de Enfermagem</institution>
            <institution content-type="orgdiv2">Programa de Pós-Graduação em Enfermagem</institution>
            <addr-line>
               <named-content content-type="city">Porto Alegre</named-content>
               <named-content content-type="state">RS</named-content>
            </addr-line>
            <country country="BR">Brazil</country>
         </aff>

    Returns
    -------
    lxml.etree._Element :
    <aff id="aff1">
        <label>1</label>
        Universidade Federal do Rio Grande do Sul, Escola de Enfermagem, Programa de Pós-Graduação em Enfermagem, Porto Alegre, RS, Brazil.
    </aff>
    """
    affs = xml_tree.findall(".//aff")
    for aff in affs:
        aff_institution = aff.find("./institution[@content-type='original']").text

        for institution in aff.findall(".//institution"):
            aff.remove(institution)

        aff.remove(aff.find('./addr-line'))

        aff.remove(aff.find("./country"))

        node_label = aff.find("./label")

        if node_label is not None:
            node_label.tail = aff_institution
        else:
            aff.text = aff_institution


def xml_pmc_ref(xml_tree):
    refs = xml_tree.findall(".//ref")
    for ref in refs:
        ref.remove(ref.find("./mixed-citation"))

