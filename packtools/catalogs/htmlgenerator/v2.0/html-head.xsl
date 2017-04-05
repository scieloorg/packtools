<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:template match="*" mode="html-head-title">
		<title>
			<xsl:apply-templates select=".//article/journal-title"/>
		</title>
	</xsl:template>
	<xsl:template match="*" mode="html-head-meta">
		<!-- FIXME -->
		<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1.0"/>

		<!-- adicionar o link da versão antiga no rel=canonical -->
		<link rel="canonical" href=""/>

		<meta name="citation_journal_title" content="Materials Research"/>
		<meta name="citation_journal_title_abbrev" content="Mat. Res."/>
		<meta name="citation_publisher" content="ABM, ABC, ABPol"/>

		<meta name="citation_title"
			content="Effect of Tetraethoxy-silane (TEOS) Amounts on the Corrosion Prevention Properties of Siloxane-PMMA Hybrid Coatings on Galvanized Steel Substrates"/>
		<meta name="citation_date" content="12/2015"/>
		<meta name="citation_volume" content="18"/>
		<meta name="citation_issue" content="6"/>
		<meta name="citation_issn" content="1980-5373"/>
		<meta name="citation_doi" content="10.1590/1516-1439.321614"/>

		<!-- adicionar links para os parâmetros abaixo -->
		<meta name="citation_abstract_html_url" content=""/>
		<meta name="citation_fulltext_html_url" content=""/>
		<meta name="citation_pdf_url" content=""/>

		<meta name="citation_author" content="Marielen Longhi"/>
		<meta name="citation_author_institution"
			content="Programa de Pós-Graduação em Engenharia de Processos e Tecnologia, Universidade de Caxias do Sul – UCS"/>

		<meta name="citation_author" content="Sandra Raquel Kunsta"/>
		<meta name="citation_author_institution"
			content="Programa de Pós-Graduação em Engenharia de Processos e Tecnologia, Universidade de Caxias do Sul – UCS"/>

		<meta name="citation_author" content="Lilian Vanessa Rossa Beltrami"/>
		<meta name="citation_author_institution"
			content="Laboratório de Pesquisa em Corrosão, Universidade Federal do Rio Grande do Sul – UFRGS"/>

		<meta name="citation_author" content="Estela Knopp Kerstner"/>
		<meta name="citation_author_institution"
			content="Laboratório de Pesquisa em Corrosão, Universidade Federal do Rio Grande do Sul – UFRGS"/>

		<meta name="citation_author" content="Cícero Inácio Silva Filho"/>
		<meta name="citation_author_institution"
			content="Departamento de Química, Universidade Federal de Sergipe – UFS"/>

		<meta name="citation_author" content="Victor Hugo Vitorino Sarmento"/>
		<meta name="citation_author_institution"
			content="Departamento de Química, Universidade Federal de Sergipe – UFS"/>

		<meta name="citation_author" content="Célia Malfatti"/>
		<meta name="citation_author_institution"
			content="Laboratório de Pesquisa em Corrosão, Universidade Federal do Rio Grande do Sul – UFRGS"/>

		<meta name="citation_id" content="10.1590/1414-431X20122409"/>

		<meta property="og:title"
			content="Effect of Tetraethoxy-silane (TEOS) Amounts on the Corrosion Prevention Properties of Siloxane-PMMA Hybrid Coatings on Galvanized Steel Substrates"/>
		<!-- Description = 250 primeiros caracteres do abstract -->
		<meta property="og:description"
			content="Siloxane-poly(methyl methacrylate) (PMMA) organic-inorganic hybrid coatings were deposited on galvanized steel by the dip-coating sol-gel technique. Anticorrosion properties, as well as the morphological, surface and structural features were studied."/>
		<!-- -->
		<meta property="og:url" content="http://dx.doi.org/10.1590/1516-1439.321614"/>
	</xsl:template>

</xsl:stylesheet>
