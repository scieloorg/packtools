<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="/" mode="js"><!--FIXME-->
        <script src="{$JS_PATH}/vendor/jquery-1.11.0.min.js"></script>
        <script src="{$JS_PATH}/vendor/bootstrap.min.js"></script>
        <script src="{$JS_PATH}/vendor/jquery-ui.min.js"></script>
        <script src="{$JS_PATH}/plugins.js"></script>
        <script src="{$JS_PATH}/main.js"></script>
    </xsl:template>
    <xsl:template match="/" mode="css"><!--FIXME-->
        <link rel="stylesheet" href="{$CSS_PATH}/bootstrap.min.css"/>
        <link rel="stylesheet" href="{$CSS_PATH}/scielo-portal.css"/>
        <link rel="stylesheet" href="{$CSS_PATH}/scielo-print.css" media="print"/>
    </xsl:template>
    <xsl:template match="/">
       <html>
       <xsl:text>
            <!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
            <!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
            <!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
            <!--[if gt IE 8]> <html class="no-js"> <![endif]-->
       </xsl:text>
	<head>
		<meta charset="utf-8"/>
		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>
				
		<title>Boletim do Museu Paraense Emílio Goeldi - SciELO Brasil</title>

		<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1.0"/>

		<!-- adicionar o link da versão antiga no rel=canonical -->
		<link rel="canonical" href="" />

		<meta name="citation_journal_title" content="Brazilian Journal of Medical and Biological Research" />
		<meta name="citation_journal_title_abbrev" content="Braz J Med Biol Res" />
		<meta name="citation_publisher" content="Associação Brasileira de Divulgação Científica" />

		<meta name="citation_title" content="Induction of chagasic-like arrhythmias in the isolated beating hearts of healthy rats perfused with Trypanosoma cruzi-conditioned médium" />
		<meta name="citation_date" content="01/2013" />
		<meta name="citation_volume" content="46" />
		<meta name="citation_issue" content="1" />
		<meta name="citation_issn" content="1414-431X" />
		<meta name="citation_doi" content="10.1590/1414-431X20122409" />

		<!-- adicionar links para os parâmetros abaixo -->
		<meta name="citation_abstract_html_url" content="" />
		<meta name="citation_fulltext_html_url" content="" />
		<meta name="citation_pdf_url" content="" />

		<meta name="citation_author" content="Rodríguez-Angulo, H."/>
		<meta name="citation_author_institution" content="Instituto Venezolano de Investigaciones Científicas, Centro de Biofísica y Bioquímica, Caracas, Venezuela" />

		<meta name="citation_author" content="Toro-Mendoza, J."/>
		<meta name="citation_author_institution" content="Instituto Venezolano de Investigaciones Científicas, Centro de Estudios Interdisciplinarios de la Física, Caracas, Venezuela" />

		<meta name="citation_author" content="Marques, J."/>
		<meta name="citation_author_institution" content="Instituto de Medicina Tropical, Universidad Central de Venezuela, Servicio de Cardiología, Caracas, Venezuela" />

		<meta name="citation_author" content="Bonfante-Cabarcas, R."/>
		<meta name="citation_author_institution" content="Universidad Centroccidental &#8220;Lisandro Alvarado&#8221;, Unidad de Investigación en Bioquímica, Decanato de Ciencias de la Salud, Barquisimeto, Venezuela" />

		<meta name="citation_author" content="Mijares, A."/>
		<meta name="citation_author_institution" content="Instituto Venezolano de Investigaciones Científicas, Centro de Biofísica y Bioquímica, Caracas, Venezuela" />

		<meta name="citation_firstpage" content="58" />
		<meta name="citation_lastpage" content="64" />
		<meta name="citation_id" content="10.1590/1414-431X20122409" />

		<meta property="og:title" content="Induction of chagasic-like arrhythmias in the isolated beating hearts of healthy rats perfused with Trypanosoma cruzi-conditioned médium" /> 
		<meta property="og:image" content="http://localhost/static/img/logo-plainScielo.png" /> 
		<meta property="og:description" content="Brazilian Journal of Medical and Biological Research" /> 
		<meta property="og:url" content="http://localhost/article.html"/>

		<xsl:apply-templates select="." mode="css"></xsl:apply-templates>

		<link rel="alternate" type="application/rss+xml" title="SciELO" href=""/>
        <xsl:text>
		<!--[if lt IE 9]>
			<script src="../static/js/vendor/html5-3.6-respond-1.1.0.min.js"></script>
		<![endif]-->
            </xsl:text>
	</head>
	<body class="journal article">
		<a name="top"></a>
		<header>
			<div class="container">
				<div class="topFunction">
					<div class="col-md-2 col-sm-3 mainNav">
						<a href="" class="menu" data-rel="#mainMenu" title="Abrir menu">Abrir menu</a>
						<h2><a href="/Colecao/" title="Ir para a homepage da Coleção SciELO Brasil"><img src="../static/img/logo-scielo-journal-brasil.png" alt="SciELO Brasil"/></a></h2>
						<div class="mainMenu" id="mainMenu">
							<div class="row">
								<div class="col-md-7 col-md-offset-2 col-sm-7 col-sm-offset-2 logo">
									<img src="../static/img/logo-scielo-journal-brasil.png" alt="SciELO Brasil"/>
								</div>
							</div>
							<nav>
								<ul>
									<li>
										<a href="/Colecao/"><strong>SciELO Brasil</strong></a>
										<ul>
											<li><a href="/Colecao/alfa.html">Lista alfabética de periódicos</a></li>
											<li><a href="/Colecao/tema.html">Lista temática de periódicos</a></li> 
											<li><a href="/Colecao/edit.html">Lista de periódicos por editoras</a></li>
											<li><a href="/Colecao/buscar.html">Busca</a></li>
											<li><a href="/Colecao/metricas.html">Métricas</a></li>
											<li><a href="/Colecao/sobre.html">Sobre o SciELO Brasil</a></li>
											<li><a href="/Colecao/contatos.html">Contatos</a></li>
										</ul>
									</li>
									<li>
										<a href="/Rede/"><strong>SciELO.org - Rede SciELO</strong></a>
										<ul>
											<li><a href="http://www.scielo.org/php/index.php">Coleções nacionais e temáticas</a></li>
											<li><a href="http://www.scielo.org/applications/scielo-org/php/secondLevel.php?xml=secondLevelForAlphabeticList&amp;xsl=secondLevelForAlphabeticList">Lista alfabética de periódicos</a></li>
										    <li><a href="http://www.scielo.org/applications/scielo-org/php/secondLevel.php?xml=secondLevelForSubjectByLetter&amp;xsl=secondLevelForSubjectByLetter">Lista de periódicos por assunto</a></li>
											<li><a href="/Colecao/buscar.html">Busca</a></li>
											<li><a href="http://www.scielo.org/applications/scielo-org/php/siteUsage.php">Métricas</a></li>
										    <li><a href="http://www.scielo.org/php/level.php?lang=pt&amp;component=56&amp;item=9">Acesso OAI e RSS</a></li>
										    <li><a href="http://www.scielo.org/php/level.php?lang=pt&amp;component=56&amp;item=8">Sobre a Rede SciELO</a></li>
											<li><a href="#">Contatos</a></li>
										</ul>
									</li>
									<li>
										<a href="#"><strong>Portal do Autor</strong></a>
									</li>
									<li>
										<a href="http://blog.scielo.org/"><strong>Blog SciELO em Perspectiva</strong></a>
									</li>
								</ul>
							</nav>
						</div>
					</div>
					<div class="col-md-8 col-sm-6 brandLogo">
						<div class="row">
							<div class="col-md-3 hidden-sm">
								<img src="../static/trash/logo-biological.gif" alt="Logomarca do Boletim do Museu Paraense Emílio Goeldi" />
							</div>
							<div class="col-md-9 col-md-offset-0 col-sm-11 col-sm-offset-1">
								<span class="theme">Ciências Biológicas</span>
								<h1>Brazilian Journal of Medical and Biological Research</h1>
								<span class="publisher">Publicação de <strong>Associação Brasileira de Divulgação Científica</strong></span>
								<span class="issn">ISSN 1414-431X</span>
							</div>
						</div>
					</div>
					<div class="col-md-2 col-sm-3 journalMenu">
						<div class="language">
							<a href="index.en.html" class="lang-en" lang="en">English</a>
							<a href="index.es.html" class="lang-es" lang="es">Español</a>
						</div>
						<ul>
							<li><a href="secundaria.html"><span class="glyphBtn submission"></span> Submissão de manuscritos</a></li>
							<li><a href="secundaria.html"><span class="glyphBtn authorInstructions"></span> Instruções aos autores</a></li>
							<li><a href="secundaria.html"><span class="glyphBtn about"></span> Sobre o periódico</a></li>
							<li><a href="secundaria.html"><span class="glyphBtn contact"></span> Contato</a></li>
						</ul>
					</div>
					<div class="clearfix"></div>
				</div>
			</div>
		</header>

		<section class="levelMenu">
			<div class="container">
				<div class="col-md-2 col-sm-2">
					<h2>&#160;</h2>
					<a href="/Periodico/homepage.html" class="btn single"><span class="glyphBtn home"></span> home</a>
				</div>
				<div class="col-md-5 col-sm-5">
					<h2><span class="glyphBtn articles"></span> Artigos do Ano 2013, Volume 46 Número 1</h2>
					<div class="btn-group">
						<a href="/Periodico/atual.html" class="btn group">sumário</a>
						<a href="javascript:;" class="btn group">« anterior</a>
						<a href="javascript:;" class="btn group selected">atual</a>
						<a href="javascript:;" class="btn group">próximo »</a>
					</div>
				</div>
				<div class="col-md-5 col-sm-5 downloadOptions">
					<h2><span class="glyphBtn articleDownload"></span> Outras versões deste artigo</h2>
					<div class="btn-group">
						<ul>
							<li class="group">
								<a href="javascript:;" class="btn dropdown-toggle" data-toggle="dropdown"><span class="glyphBtn pdfDownload"></span> PDF</a>
								<ul class="dropdown-menu">
									<li><a href="">Espanhol</a></li>
									<li><a href="">Inglês</a></li>
									<li><a href="">Português</a></li>
								</ul>
							</li>
							<li class="group">
								<a href="javascript:;" class="btn group"><span class="glyphBtn epubDownload"></span> ePUB</a>
							</li>
							<li class="group">
								<a href="javascript:;" class="btn group"><span class="glyphBtn readcubeView"></span> readcube</a>
							</li>
							<li class="group">
								<a href="javascript:;" class="btn group"><span class="glyphBtn xmlDownload"></span> XML</a>
								<ul class="dropdown-menu">
									<li><a href="">Espanhol</a></li>
									<li><a href="">Inglês</a></li>
									<li><a href="">Português</a></li>
								</ul>
							</li>

						</ul>
					</div>
				</div>
			</div>
		</section>

		<xsl:apply-templates select="." mode="article"></xsl:apply-templates>

		<section class="journalContacts">
			<div class="container">
				<div class="col-md-5 col-sm-5 journalAddress">
					<div class="col-md-1 col-sm-2">
						<span class="glyphBtn pin"></span>
					</div>
					<div class="col-md-10 col-sm-9">
						<strong>MCT/Museu Paraense Emílio Goeldi</strong>
						Av. Magalhães Barata, 376 - São Braz 66040-170 - Belém - PA<br/>
						Tel/Fax: (55 91) 3249-6373
					</div>
				</div>
				<div class="col-md-4 col-sm-4 journalLinks">
					<a href="" class="showTooltip" title="Facebook"><span class="glyphBtn bigFacebook"></span></a>
					<a href="" class="showTooltip" title="Twitter"><span class="glyphBtn bigTwitter"></span></a>
					<a href="" class="showTooltip" title="Google+"><span class="glyphBtn bigGooglePlus"></span></a>
					<span class="text">Siga este periódico nas redes sociais</span>
				</div>
				<div class="col-md-3 col-sm-3 journalLinks">
					<a href="" class="showTooltip" title="RSS"><span class="glyphBtn bigRSS"></span></a>
					<span class="text" style="width: 70%;">Acompanhe os números deste periódico no seu leitor de RSS</span>
				</div>
				<div class="clearfix"></div>
			</div>
		</section>

		<footer>
			<div class="collectionSignature">
				<div class="container">
					<div class="col-md-2 col-sm-2">
						<img src="../static/img/logo-scielo-signature.png" alt="Logo SciELO" />
					</div>
					<div class="col-md-8 col-sm-9">
						<strong>SciELO - Scientific Electronic Library Online</strong><br/>						
						Av. Onze de Junho, 269 - Vila Clementino 04041-050 São Paulo SP - Brasil<br/>
						Tel.: (55 11) 5083-3639 - Email: scielo@scielo.org
					</div>
				</div>
			</div>
			<div class="partners">
				<a href="http://www.fapesp.br/" target="_blank"><img src="../static/img/partner-fapesp.png" alt="FAPESP"/></a>
				<a href="http://www.cnpq.br/" target="_blank"><img src="../static/img/partner-cnpq.png" alt="CNPQ"/></a>
				<a href="http://regional.bvsalud.org/php/index.php?lang=pt" target="_blank"><img src="../static/img/partner-bvs.png" alt="Biblioteca Virtual em Saúde"/></a>
				<a href="http://regional.bvsalud.org/bvs/bireme/homepage.htm" target="_blank"><img src="../static/img/partner-bireme.png" alt="BIREME - OPAS - OMS"/></a>
				<img src="../static/img/partner-fap.png" alt="FAP UNIFESP"/>
			</div>
		</footer>

		<div class="alternativeHeader">
			<div class="container">
				<div class="col-md-2 col-sm-3 mainNav">
					<a href="" class="menu" data-rel="#alternativeMainMenu" title="Abrir menu">Abrir menu</a>
					<h2><a href="/Colecao/" title="Ir para a homepage da Coleção SciELO Brasil"><img src="../static/img/logo-scielo-alternative-brasil.png" alt="SciELO Brasil"/></a></h2>
					<div class="mainMenu" id="alternativeMainMenu">
						<div class="row">
							<div class="col-md-7 col-md-offset-2 col-sm-7 col-sm-offset-2 logo">
								<img src="../static/img/logo-scielo-journal-brasil.png" alt="SciELO Brasil"/>
							</div>
						</div>
						<nav>
							<ul>
							</ul>
						</nav>
					</div>
				</div>
				<div class="col-md-4 col-sm-5 journalInfo">
					<ul>
						<li>
							<a href="" class="dropdown-toggle" data-toggle="dropdown"><span class="text">Induction of chagasic-like arrhythmias... <span class="glyphBtn grayArrowDown"></span></span></a>
							<ul class="dropdown-menu" role="menu">
								<li class="dropdown-header">Braz J Med Biol Res vol.46 no.1 Ribeirão Preto Jan. 2013 Epub Jan 11, 2013</li>
								<li><strong>Induction of chagasic-like arrhythmias in the isolated beating hearts of healthy rats perfused with <em>Trypanosoma cruzi</em>-conditioned medium</strong></li>
								<li class="author">H. Rodríguez-Angulo; J. Toro-Mendoza; J. Marques; R. Bonfante-Cabarcas; A. Mijares;</li>
								<li class="listLink">
									<a href="#authorInfo" class="goto trigger" data-rel="#authorInfoBtn">Sobre os autores</a>
								</li>
								<li class="listLink">
									<a href="#authorInfo" class="goto trigger" data-rel="#copyrightInfoBtn">Permissões</a>
								</li>
							</ul>
						</li>
					</ul>
				</div>
				<div class="col-md-6 col-md-5 menuItens">
					<ul>
						<li><a href="homepage.html" class="showTooltip" data-placement="bottom" title="Homepage do periódico"><span class="glyphBtn home"></span></a></li>
						<li>
							<a href="atual.html" class="dropdown-toggle" data-toggle="dropdown"><span class="glyphBtn articles"></span></a>
							<ul class="dropdown-menu" role="menu">
								<li class="dropdown-header">Artigos de 2013, V.46 N.1</li>
								<li><a href="../Periodico/atual.html">• sumário</a></li>
								<li><a href="#">« anterior</a></li>
								<li><a href="#">• atual</a></li>
								<li><a href="#">» próximo</a></li>
							</ul>
						</li>
						<li>
							<a href="atual.html" class="dropdown-toggle" data-toggle="dropdown"><span class="glyphBtn pdfDownload"></span></a>
							<ul class="dropdown-menu" role="menu">
								<li class="dropdown-header">Download PDF</li>
								<li><a href="#">Português</a></li>
								<li><a href="#">Inglês</a></li>
								<li><a href="#">Espanhol</a></li>
							</ul>
						</li>
						<li><a href="#" class="showTooltip" data-placement="bottom" title="Visualizar no Readcube"><span class="glyphBtn readcubeView"></span></a></li>
						<li>
							<a href="atual.html" class="dropdown-toggle" data-toggle="dropdown"><span class="glyphBtn xmlDownload"></span></a>
							<ul class="dropdown-menu" role="menu">
								<li class="dropdown-header">Download XML</li>
								<li><a href="#">Português</a></li>
								<li><a href="#">Inglês</a></li>
								<li><a href="#">Espanhol</a></li>
							</ul>
						</li>
						<li><a href="#" class="showTooltip expandReduceText" data-expandreducetext="true" data-placement="bottom" title="Expandir/Reduzir texto"><span class="glyphBtn expandTextIcon"></span></a></li>
						<li><a href="#top" class="showTooltip goto" data-placement="bottom" title="Topo"><span class="glyphBtn gotoTopoIcon"></span></a></li>
					</ul>
				</div>
			</div>
		</div>

		<div class="modal fade" id="SendViaEmail" tabindex="-1" role="dialog" aria-hidden="true">
			<div class="modal-dialog">
				<div class="modal-content">
					<div class="modal-header">
					    <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&#215;</span><span class="sr-only">Close</span></button>
						<h4 class="modal-title">Enviar página por e-mail</h4>
					</div>
					<form name="sendViaEmail" action="resultados-enviado.en.html" method="post" class="validate">
						<div class="modal-body">
							<div class="form-group">
								<label class="control-label">Para*</label>
								<input type="text" name="email" value="" class="form-control valid multipleMail" />

								<p class="text-muted">
									Use ; (semicolon) to insert more emails.
								</p>
							</div>
							<div class="form-group extendForm">
								<a href="javascript:;" class="showBlock" id="showBlock" data-rel="#extraFields" data-hide="#showBlock">Alterar remetente, assunto e comentários</a>

								<div id="extraFields" style="display: none;">
									<div class="form-group">
										<label>Seu e-mail</label>
										<input type="text" name="yourEmail" value="" class="form-control" placeholder="" />
									</div>
									<div class="form-group">
										<label>Assunto</label>
										<input type="text" name="subject" value="" class="form-control" placeholder="" />
									</div>
									<div class="form-group">
										<label>Comentário</label>
										<textarea name="comment" class="form-control"></textarea>
									</div>
									<a href="javascript:;" class="showBlock" data-rel="#showBlock" data-hide="#extraFields">Remover remetente, assunto e comentários</a>
								</div>
							</div>
						</div>
						<div class="modal-footer">
							<input type="submit" name="s" value="Enviar" class="btn"/>
						</div>
					</form>
				</div>
			</div>
		</div>

        <xsl:apply-templates select="." mode="js"/>
	</body>
</html>
   </xsl:template>
</xsl:stylesheet>