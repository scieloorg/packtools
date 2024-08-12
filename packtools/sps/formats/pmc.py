# coding: utf-8
from lxml import etree as ET


def pipeline_pmc(xml_tree, pretty_print=True):
    xml_pmc_aff(xml_tree)
    xml_pmc_ref(xml_tree)

    return ET.tostring(xml_tree, pretty_print=pretty_print, encode="utf-8").decode(
        "utf-8"
    )


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
        original_institution = aff.find("./institution[@content-type='original']")
        if original_institution is not None:
            aff_institution = original_institution.text
        else:
            aff_with_address = []
            aff_with_address.append(aff.find("./institution[@content-type='orgname']").text)
            
            addr_line = aff.find("./addr-line")
            if addr_line is not None:
                named_contents = addr_line.xpath(".//named-content | .//state | .//city ")
                aff_with_address.extend([named_content.text for named_content in named_contents])
            
            country = aff.find("./country")
            if country is not None:
                aff_with_address.append(country.text)
            aff_institution = ", ".join(aff_with_address)


        for institution in aff.findall(".//institution"):
            aff.remove(institution)

        for element in [aff.find("./addr-line"), aff.find("./country")]:
            aff.remove(element)

        node_label = aff.find("./label")

        if node_label is not None:
            node_label.tail = aff_institution
        else:
            aff.text = aff_institution


def xml_pmc_ref(xml_tree):
    """
    Remove o elemento 'mixed-citation' do XML SciELO.

    Parameters
    ----------
    xml_tree : lxml.etree._Element
        Elemento XML no padrão SciELO com os dados de origem, por exemplo:
        <ref id="B1">
            <label>1.</label>
            <mixed-citation>
               1. Tran B, Falster MO, Douglas K, Blyth F, Jorm LR. Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages. Drug Alcohol Depend. 2015;150:85-91. DOI:
               <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </mixed-citation>
            <element-citation publication-type="journal">
               <person-group person-group-type="author">
                  <name>
                     <surname>Tran</surname>
                     <given-names>B</given-names>
                  </name>
                  <name>
                     <surname>Falster</surname>
                     <given-names>MO</given-names>
                  </name>
                  <name>
                     <surname>Douglas</surname>
                     <given-names>K</given-names>
                  </name>
                  <name>
                     <surname>Blyth</surname>
                     <given-names>F</given-names>
                  </name>
                  <name>
                     <surname>Jorm</surname>
                     <given-names>LR</given-names>
                  </name>
               </person-group>
               <article-title>Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages</article-title>
               <source>Drug Alcohol Depend.</source>
               <year>2015</year>
               <volume>150</volume>
               <fpage>85</fpage>
               <lpage>91</lpage>
               <comment>
                  DOI:
                  <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
               </comment>
            </element-citation>
         </ref>

    Returns
    -------
    lxml.etree._Element :
        <ref id="B1">
            <label>1.</label>
            <element-citation publication-type="journal">
               <person-group person-group-type="author">
                  <name>
                     <surname>Tran</surname>
                     <given-names>B</given-names>
                  </name>
                  <name>
                     <surname>Falster</surname>
                     <given-names>MO</given-names>
                  </name>
                  <name>
                     <surname>Douglas</surname>
                     <given-names>K</given-names>
                  </name>
                  <name>
                     <surname>Blyth</surname>
                     <given-names>F</given-names>
                  </name>
                  <name>
                     <surname>Jorm</surname>
                     <given-names>LR</given-names>
                  </name>
               </person-group>
               <article-title>Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages</article-title>
               <source>Drug Alcohol Depend.</source>
               <year>2015</year>
               <volume>150</volume>
               <fpage>85</fpage>
               <lpage>91</lpage>
               <comment>
                  DOI:
                  <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
               </comment>
            </element-citation>
         </ref>
    """
    refs = xml_tree.findall(".//ref")
    for ref in refs:
        ref.remove(ref.find("./mixed-citation"))

