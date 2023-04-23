# coding: utf-8
from lxml import etree as ET
import re
import uuid
from copy import deepcopy
from datetime import datetime

from packtools.sps.models import (
    journal_meta,
    dates,
    front_articlemeta_issue,
    article_and_subarticles,
    article_authors,
    aff,
    article_abstract,
    article_ids,
    article_license,
    article_titles,
    article_doi_with_lang,
    article_citations,
)

SUPPLBEG_REGEX = re.compile(r'^0 ')
SUPPLEND_REGEX = re.compile(r' 0$')


def get_timestamp():
    return datetime.now().strftime('%Y%m%d%H%M%S')


def get_doi_batch_id():
    return uuid.uuid4().hex


def pipeline_crossref(xml_tree, data):
    xml_crossref = setupdoibatch_pipe()
    xml_head_pipe(xml_crossref)
    xml_doibatchid_pipe(xml_crossref)
    xml_timestamp_pipe(xml_crossref)
    xml_depositor_pipe(xml_crossref, data)
    xml_registrant_pipe(xml_crossref, data)
    xml_body_pipe(xml_crossref)
    xml_journal_pipe(xml_crossref)
    xml_journalmetadata_pipe(xml_crossref)
    xml_journaltitle_pipe(xml_tree, xml_crossref)
    xml_abbreviatedjournaltitle_pipe(xml_tree, xml_crossref)
    xml_issn_pipe(xml_tree, xml_crossref)
    xml_journalissue_pipe(xml_crossref)
    xml_pubdate_pipe(xml_tree, xml_crossref)
    xml_journalvolume_pipe(xml_crossref)
    xml_volume_pipe(xml_tree, xml_crossref)
    xml_issue_pipe(xml_tree, xml_crossref)
    xml_journalarticle_pipe(xml_tree, xml_crossref)
    xml_articletitles_pipe(xml_tree, xml_crossref)
    # xml_articletitle_pipe(xml_tree, xml_crossref)
    xml_articlecontributors_pipe(xml_tree, xml_crossref)
    xml_articleabstract_pipe(xml_tree, xml_crossref)
    xml_articlepubdate_pipe(xml_tree, xml_crossref)
    xml_pages_pipe(xml_tree, xml_crossref)
    xml_pid_pipe(xml_tree, xml_crossref)
    xml_elocation_pipe(xml_tree, xml_crossref)
    xml_permissions_pipe(xml_tree, xml_crossref)
    xml_programrelateditem_pipe(xml_tree, xml_crossref)
    xml_doidata_pipe(xml_crossref)
    xml_doi_pipe(xml_tree, xml_crossref)
    xml_resource_pipe(xml_tree, xml_crossref)
    xml_collection_pipe(xml_tree, xml_crossref)
    xml_articlecitations_pipe(xml_tree, xml_crossref)
    # xml_close_pipe(xml_tree, xml_crossref)

    return xml_crossref


def setupdoibatch_pipe():
    """
    <doi_batch xmlns:ai="http://www.crossref.org/AccessIndicators.xsd"
    xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns="http://www.crossref.org/schema/4.4.0"
    xsi:schemaLocation="http://www.crossref.org/schema/4.4.0 http://www.crossref.org/schemas/crossref4.4.0.xsd"/>
    """

    nsmap = {
        'ai': 'http://www.crossref.org/AccessIndicators.xsd',
        'jats': 'http://www.ncbi.nlm.nih.gov/JATS1',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xml': 'http://www.w3.org/XML/1998/namespace'

    }

    el = ET.Element('doi_batch', nsmap=nsmap)
    el.set('version', '4.4.0')
    el.set('xmlns', 'http://www.crossref.org/schema/4.4.0')
    el.set('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation',
           'http://www.crossref.org/schema/4.4.0 http://www.crossref.org/schemas/crossref4.4.0.xsd')

    return el


def xml_head_pipe(xml_crossref):
    head = ET.Element('head')

    xml_crossref.append(head)


def xml_doibatchid_pipe(xml_crossref):
    """
    <head>
        <doi_batch_id>49d374553c5d48c0bdd54d25080e0045</doi_batch_id>
    </head>
    """

    doi_batch_id = ET.Element('doi_batch_id')
    doi_batch_id.text = get_doi_batch_id()

    xml_crossref.find('./head').append(doi_batch_id)


def xml_timestamp_pipe(xml_crossref):
    """
    <head>
        <timestamp>20230405112328</timestamp>
    </head>
    """

    timestamp = ET.Element('timestamp')
    timestamp.text = get_timestamp()

    xml_crossref.find('./head').append(timestamp)


def xml_depositor_pipe(xml_crossref, data):
    """
            data = {
                        "depositor_name": depositor,
                        "depositor_email_address": name@domain.com
                    }

            <head>
                <depositor>
                    <depositor_name>depositor</depositor_name>
                    <email_address>name@domain.com</email_address>
                </depositor>
            </head>
            """

    depositor = ET.Element('depositor')
    depositor_name = ET.Element('depositor_name')
    email_address = ET.Element('email_address')

    depositor_name.text = data.get('depositor_name')
    email_address.text = data.get('depositor_email_address')

    depositor.append(depositor_name)
    depositor.append(email_address)

    xml_crossref.find('./head').append(depositor)


def xml_registrant_pipe(xml_crossref, data):
    """
        data = {
                    "registrant": registrant
                }

        <head>
            <registrant>registrant</registrant>
        </head>
    """

    registrant = ET.Element('registrant')
    registrant.text = data.get('registrant')

    xml_crossref.find('./head').append(registrant)


def xml_body_pipe(xml_crossref):
    body = ET.Element('body')

    xml_crossref.append(body)


def xml_journal_pipe(xml_crossref):
    journal = ET.Element('journal')

    xml_crossref.find('./body').append(journal)


def xml_journalmetadata_pipe(xml_crossref):
    journal_metadata = ET.Element('journal_metadata')

    xml_crossref.find('./body/journal').append(journal_metadata)


def xml_journaltitle_pipe(xml_tree, xml_crossref):
    """
        <journal>
            <journal_metadata>
                <full_title>Revista da Escola de Enfermagem da USP</full_title>
            </journal_metadata>
        </journal>
    """
    titles = journal_meta.Title(xml_tree)
    full_title = ET.Element('full_title')
    full_title.text = titles.journal_title

    xml_crossref.find('./body/journal/journal_metadata').append(full_title)


def xml_abbreviatedjournaltitle_pipe(xml_tree, xml_crossref):
    """
        <journal>
            <journal_metadata>
                <abbrev_title>Rev. esc. enferm. USP</abbrev_title>
            </journal_metadata>
        </journal>
    """
    titles = journal_meta.Title(xml_tree)
    abbrev_title = ET.Element('abbrev_title')
    abbrev_title.text = titles.abbreviated_journal_title

    xml_crossref.find('./body/journal/journal_metadata').append(abbrev_title)


def xml_issn_pipe(xml_tree, xml_crossref):
    """
        <journal>
            <journal_metadata>
                <issn media_type="electronic">1980-220X</issn>
                <issn media_type="print">0080-6234</issn>
            </journal_metadata>
        </journal>
    """
    issns = journal_meta.ISSN(xml_tree)

    issn = ET.Element('issn')
    issn.text = issns.epub
    issn.set('media_type', 'electronic')
    xml_crossref.find('./body/journal/journal_metadata').append(issn)

    issn = ET.Element('issn')
    issn.text = issns.ppub
    issn.set('media_type', 'print')
    xml_crossref.find('./body/journal/journal_metadata').append(issn)


def xml_journalissue_pipe(xml_crossref):
    """
    <journal_issue>
        <publication_date media_type="online">
            <year>2022</year>
        </publication_date>
        <journal_volume>
            <volume>56</volume>
        </journal_volume>
    </journal_issue>
    """
    journal_issue = ET.Element('journal_issue')

    xml_crossref.find('./body/journal').append(journal_issue)


def xml_pubdate_pipe(xml_tree, xml_crossref):
    """
    <journal_issue>
        <publication_date media_type="online">
            <year>2022</year>
        </publication_date>
    </journal_issue>
    """
    year = ET.Element('year')
    year.text = dates.ArticleDates(xml_tree).article_date.get('year')

    publication_date = ET.Element('publication_date')
    publication_date.set('media_type', 'online')
    publication_date.append(year)

    xml_crossref.find('./body/journal/journal_issue').append(publication_date)


def xml_journalvolume_pipe(xml_crossref):
    journal_volume = ET.Element('journal_volume')

    xml_crossref.find('./body/journal/journal_issue').append(journal_volume)


def xml_volume_pipe(xml_tree, xml_crossref):
    """
    <journal_issue>
        <journal_volume>
            <volume>56</volume>
        </journal_volume>
    </journal_issue>
    """
    volume = ET.Element('volume')
    volume.text = front_articlemeta_issue.ArticleMetaIssue(xml_tree).volume

    xml_crossref.find('./body/journal/journal_issue/journal_volume').append(volume)


def xml_issue_pipe(xml_tree, xml_crossref):
    """
    <journal_issue>
        <journal_volume>
            <issue>4</issue>
        </journal_volume>
    </journal_issue>
    """
    issue = ET.Element('issue')
    issue.text = front_articlemeta_issue.ArticleMetaIssue(xml_tree).issue

    xml_crossref.find('./body/journal/journal_issue/journal_volume').append(issue)


def xml_journalarticle_pipe(xml_tree, xml_crossref):
    """
    <body>
        <journal>
            <journal_article language="en" publication_type="research-article" reference_distribution_opts="any"/>
            <journal_article language="pt" publication_type="translation" reference_distribution_opts="any"/>
        </journal>
    </body>
    """
    articles = article_and_subarticles.ArticleAndSubArticles(xml_tree).data
    for article in articles:
        journal_article = ET.Element('journal_article')
        journal_article.set('language', article['lang'])
        journal_article.set('publication_type', article['article_type'])
        # todo
        # reference_distribution_opts=?
        journal_article.set('reference_distribution_opts', 'any')
        xml_crossref.find('./body/journal').append(journal_article)


def xml_articletitles_pipe(xml_tree, xml_crossref):
    """
    IN (SciELO format) ->
    <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
    <front>
    <article-meta>
    <article-id specific-use="scielo-v3" pub-id-type="publisher-id">ZwzqmpTpbhTmtwR9GfDzP7c</article-id>
    <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0080-62342022000100445</article-id>
    <article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569en</article-id>
    <article-id pub-id-type="other">00445</article-id>
    <title-group>
    <article-title>
    Effects of an educational intervention with nursing professionals on approaches to hospitalized smokers: a quasi-experimental study
    <xref ref-type="fn" rid="FN1">*</xref>
    </article-title>
    <trans-title-group xml:lang="es">
    <trans-title>Efectos de una intervención educativa con profesionales de enfermería en el abordaje de pacientes fumadores: un estudio cuasi-experimental</trans-title>
    </trans-title-group>
    </title-group>
    </article-meta>
    </front>
    <sub-article article-type="translation" id="s1" xml:lang="pt">
    <front-stub>
    <title-group>
    <article-title>
    Efeitos de uma intervenção educativa com profissionais de enfermagem sobre abordagens ao paciente tabagista: estudo quase-experimental
    <xref ref-type="fn" rid="FN2">*</xref>
    </article-title>
    </title-group>
    </front-stub>
    </sub-article>
    </article>

    OUT (CrossRef format) ->
    <doi_batch
    xmlns:ai="http://www.crossref.org/AccessIndicators.xsd"
    xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns="http://www.crossref.org/schema/4.4.0" version="4.4.0"
    xsi:schemaLocation="http://www.crossref.org/schema/4.4.0
    http://www.crossref.org/schemas/crossref4.4.0.xsd">
    <body>
    <journal>
    <journal_article language="en" publication_type="research-article" reference_distribution_opts="any">
    <titles>
    <title>Effects of an educational intervention with nursing professionals on approaches to hospitalized smokers: a quasi-experimental study</title>
    <original_language_title language="pt">Efeitos de uma intervenção educativa com profissionais de enfermagem sobre abordagens ao paciente tabagista: estudo quase-experimental</original_language_title>
    </titles>
    </journal_article>
    <journal_article language="pt" publication_type="translation" reference_distribution_opts="any">
    <titles>
    <title>Efeitos de uma intervenção educativa com profissionais de enfermagem sobre abordagens ao paciente tabagista: estudo quase-experimental</title>
    <original_language_title language="en">Effects of an educational intervention with nursing professionals on approaches to hospitalized smokers: a quasi-experimental study</original_language_title>
    </titles>
    </journal_article>
    </journal>
    </body>
    </doi_batch>
    """
    art_titles = article_titles.ArticleTitles(xml_tree).article_title_dict
    art_lang = [lang.get('lang') for lang in article_and_subarticles.ArticleAndSubArticles(xml_tree).data]

    for lang in art_lang:
        titles = ET.Element('titles')
        title = ET.Element('title')
        title.text = art_titles.get(lang)
        titles.append(title)
        original_language_title = ET.Element('original_language_title')
        orig_lang = 'pt' if lang == 'en' else 'en'
        original_language_title.set('language', orig_lang)
        original_language_title.text = art_titles.get(orig_lang)
        titles.append(original_language_title)
        xml_crossref.find(f"./body/journal/journal_article[@language='{lang}']").append(titles)


def xml_articlecontributors_pipe(xml_tree, xml_crossref):
    """
    <journal_article language="en" publication_type="research-article" reference_distribution_opts="any">
        <contributors>
            <person_name contributor_role="author" sequence="first">
                <given_name>Fernanda Guarilha</given_name>
                <surname>Boni</surname>
                <affiliation>Universidade Federal do Rio Grande do Sul, Brazil</affiliation>
                <ORCID>http://orcid.org/0000-0003-0843-6485</ORCID>
            </person_name>
            <person_name contributor_role="author" sequence="additional">
                <given_name>Yasmin Lorenz</given_name>
                <surname>da Rosa</surname>
                <affiliation>Universidade Federal do Rio Grande do Sul, Brazil</affiliation>
                <ORCID>http://orcid.org/0000-0001-7364-4753</ORCID>
            </person_name>
        </contributors>
    </journal_article>
    <journal_article language="pt" publication_type="translation" reference_distribution_opts="any">
        <contributors>
            <person_name contributor_role="author" sequence="first">
                <given_name>Fernanda Guarilha</given_name>
                <surname>Boni</surname>
                <affiliation>Universidade Federal do Rio Grande do Sul, Brazil</affiliation>
                <ORCID>http://orcid.org/0000-0003-0843-6485</ORCID>
            </person_name>
            <person_name contributor_role="author" sequence="additional">
                <given_name>Yasmin Lorenz</given_name>
                <surname>da Rosa</surname>
                <affiliation>Universidade Federal do Rio Grande do Sul, Brazil</affiliation>
                <ORCID>http://orcid.org/0000-0001-7364-4753</ORCID>
            </person_name>
        </contributors>
    </journal_article>
    """
    articles = article_and_subarticles.ArticleAndSubArticles(xml_tree).data
    authors = article_authors.Authors(xml_tree).contribs
    for article in articles:
        contributors = ET.Element('contributors')
        for seq, author in enumerate(authors):
            person_name = ET.Element('person_name')
            person_name.set('contributor_role', author.get('contrib-type'))
            if seq == 0:
                person_name.set('sequence', 'first')
            else:
                person_name.set('sequence', 'additional')
            given_name = ET.Element('given_name')
            given_name.text = author.get('given_names')
            person_name.append(given_name)
            surname = ET.Element('surname')
            surname.text = author.get('surname')
            person_name.append(surname)
            affiliation = ET.Element('affiliation')
            affs = aff.AffiliationExtractor(xml_tree).get_affiliation_data_from_multiple_tags(subtag=False)
            for a in affs:
                if a['id'] == author['rid']:
                    affiliation.text = a.get('institution')[0].get('orgname') + ', ' + a.get('country')[0].get('name')
            person_name.append(affiliation)
            ORCID = ET.Element('ORCID')
            ORCID.text = 'http://orcid.org/' + author.get('orcid')
            person_name.append(ORCID)
            contributors.append(person_name)
        xml_crossref.find(f"./body/journal/journal_article[@language='{article['lang']}']").append(contributors)


def xml_articleabstract_pipe(xml_tree, xml_crossref):
    """
    <jats:abstract xml:lang="en">
        <jats:p>Abstract Objective: to assess the effects of an educational intervention on smoking cessation aimed at the nursing team. Method: this is a quasi-experimental study with 37 nursing professionals from a Brazilian hospital from May/2019 to December/2020. The intervention consisted of training nursing professionals on approaches to hospitalized smokers divided into two steps, the first, online, a prerequisite for the face-to-face/videoconference. The effect of the intervention was assessed through pre- and post-tests completed by participants. Smokers’ medical records were also analyzed. For analysis, McNemar’s chi-square test was used. Results: there was an increase in the frequency of actions aimed at smoking cessation after the intervention. Significant differences were found in guidelines related to disclosure to family members of their decision to quit smoking and the need for support, encouragement of abstinence after hospital discharge, and information on tobacco cessation and relapse strategies. Conclusion: the educational intervention proved to be innovative and with a great capacity for disseminating knowledge. The post-test showed a positive effect on the frequency of actions aimed at smoking cessation implemented by the nursing team.</jats:p>
    </jats:abstract>
    <jats:abstract xml:lang="es">
        <jats:p>RESUMEN Objetivo: evaluar los efectos de una intervención educativa para dejar de fumar dirigida al equipo de enfermería. Método: estudio cuasi-experimental con 37 profesionales de enfermería de un hospital brasileño de mayo/2019 a diciembre/2020. La intervención consistió en capacitar a los profesionales de enfermería en el abordaje del paciente fumador, dividida en dos etapas, la primera, en línea, requisito previo para la presencial/videoconferencia. El efecto de la intervención se evaluó a través del pre y post test realizado por los participantes. También se analizaron los registros en las historias clínicas de los fumadores. Para el análisis se utilizó la prueba Chi-Square de McNemar. Resultados: hubo un aumento en la frecuencia de acciones dirigidas a dejar de fumar después de la intervención. Se encontraron diferencias significativas en las guías relacionadas con la divulgación a los familiares de la decisión de dejar de fumar y la necesidad de apoyo, el estímulo de la abstinencia después del alta hospitalaria y la información sobre estrategias para dejar de fumar y recaer. Conclusión: la intervención educativa demostró ser innovadora y con gran capacidad de diseminación del conocimiento. El post-test mostró un efecto positivo en la frecuencia de las acciones dirigidas a la deshabituación tabáquica implementadas por el equipo de enfermería.</jats:p>
    </jats:abstract>
    <jats:abstract xml:lang="pt">
        <jats:p>RESUMO Objetivo: avaliar os efeitos de uma intervenção educativa sobre cessação do tabagismo direcionada à equipe de enfermagem. Método: estudo quase-experimental com 37 profissionais de enfermagem de um hospital brasileiro de maio/2019 a dezembro/2020. A intervenção consistiu em capacitar profissionais de enfermagem sobre abordagens aos pacientes tabagistas, dividida em duas etapas, a primeira, online, pré-requisito para a presencial/videoconferência. O efeito da intervenção foi avaliado por meio do pré- e pós-teste preenchido pelos participantes. Também foram analisados registros em prontuários de pacientes fumantes. Para análise, utilizou-se o Teste do Qui-Quadrado de McNemar. Resultados: houve aumento da frequência das ações visando à cessação tabágica após a intervenção. Diferenças significativas foram encontradas em orientações relacionadas à divulgação aos familiares da decisão de parar de fumar e necessidade de apoio, incentivo à abstinência após alta hospitalar e informações sobre estratégias para cessação do tabaco e recaídas. Conclusão: a intervenção educativa se mostrou inovadora e com grande capacidade de difusão do conhecimento. O pós-teste evidenciou efeito positivo na frequência das ações visando à cessação tabágica implementadas pela equipe de enfermagem.</jats:p>
    </jats:abstract>
    """
    abstracts = article_abstract.Abstract(xml_tree).abstracts_with_tags
    articles = article_and_subarticles.ArticleAndSubArticles(xml_tree).data

    for article in articles:
        for abstract in abstracts:
            jats = ET.Element('{http://www.ncbi.nlm.nih.gov/JATS1}abstract')
            jats.set('{http://www.w3.org/XML/1998/namespace}lang', abstract.get('lang'))
            jats_p = ET.Element('{http://www.ncbi.nlm.nih.gov/JATS1}p')
            text = [abstract.get('title')]
            for key, value in abstract.get('sections').items():
                text.append(key)
                text.append(value)
            jats_p.text = ' '.join(text)
            jats.append(jats_p)
            xml_crossref.find(f"./body/journal/journal_article[@language='{article['lang']}']").append(deepcopy(jats))


def xml_articlepubdate_pipe(xml_tree, xml_crossref):
    """
    <journal_article language="en" publication_type="full_text" reference_distribution_opts="any">
        <publication_date media_type="online">
            <year>2022</year>
        </publication_date>
    </journal_article>
    <journal_article language="pt" publication_type="full_text" reference_distribution_opts="any">
        <publication_date media_type="online">
            <year>2022</year>
        </publication_date>
    </journal_article>

    todo
    publication_type in SciELO format: research-article and translation
    publication_type in CrossRef format: full_text
    """
    articles = article_and_subarticles.ArticleAndSubArticles(xml_tree).data
    pub_date = dates.ArticleDates(xml_tree).article_date

    for article in articles:
        publication_date = ET.Element('publication_date')
        # todo
        # identify media_type value
        publication_date.set('media_type', 'online')

        year = ET.Element('year')
        year.text = pub_date.get('year')

        publication_date.append(year)

        xml_crossref.find(f"./body/journal/journal_article[@language='{article['lang']}']").append(publication_date)


