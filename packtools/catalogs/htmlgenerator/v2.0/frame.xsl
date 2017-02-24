<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="/" mode="js"><!--FIXME-->
        <script src="{$JS_PATH}/vendor/jquery-1.11.0.min.js"></script>
        <script src="{$JS_PATH}/vendor/bootstrap.min.js"></script>
        <script src="{$JS_PATH}/vendor/jquery-ui.min.js"></script>
        <script src="{$JS_PATH}/plugins.js"></script>
        <script src="{$JS_PATH}/min/main-min.js"></script>
    	<!-- 
    	<script src="../static/js/vendor/jquery-1.11.0.min.js"></script>
		<script src="../static/js/vendor/bootstrap.min.js"></script>
		<script src="../static/js/vendor/jquery-ui.min.js"></script>

		<script src="../static/js/plugins.js"></script>
		<script src="../static/js/min/main-min.js"></script>
    	-->
    </xsl:template>
    <xsl:template match="/" mode="css"><!--FIXME-->
        <link rel="stylesheet" href="{$CSS_PATH}/bootstrap.min.css"/>
        <link rel="stylesheet" href="{$CSS_PATH}/scielo-portal.css"/>
        <link rel="stylesheet" href="{$CSS_PATH}/scielo-print.css" media="print"/>
    	<style>
    		table {
				font-size: 90%;
				background-color: #E8F3F8;
				font-family: courier;
			}
			.footnote {
			font-size: 70%;
			
			font-family: courier;
			}
			
    	</style>
    </xsl:template>
	<xsl:template match="/" mode="html-head-title">
		<title>Boletim do Museu Paraense Emílio Goeldi - SciELO Brasil</title>
	</xsl:template>
	<xsl:template match="/" mode="article-html-meta">
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
		<meta name="citation_author_institution" content="Universidad Centroccidental &amp;#8220;Lisandro Alvarado&amp;#8221;, Unidad de Investigación en Bioquímica, Decanato de Ciencias de la Salud, Barquisimeto, Venezuela" />
		
		<meta name="citation_author" content="Mijares, A."/>
		<meta name="citation_author_institution" content="Instituto Venezolano de Investigaciones Científicas, Centro de Biofísica y Bioquímica, Caracas, Venezuela" />
		
		<meta name="citation_firstpage" content="58" />
		<meta name="citation_lastpage" content="64" />
		<meta name="citation_id" content="10.1590/1414-431X20122409" />
		
		<meta property="og:title" content="Induction of chagasic-like arrhythmias in the isolated beating hearts of healthy rats perfused with Trypanosoma cruzi-conditioned médium" /> 
		<meta property="og:image" content="http://localhost/static/img/logo-plainScielo.png" /> 
		<meta property="og:description" content="Brazilian Journal of Medical and Biological Research" /> 
		<meta property="og:url" content="http://localhost/article.html"/>
	</xsl:template>
	<xsl:template match="/" mode="html-header">
		<header>
			<div class="container">
				<div class="topFunction">
					<div class="col-md-2 col-sm-3 mainNav">
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
				</div>
			</div>
		</header>
	</xsl:template>
	<xsl:template match="/" mode="html-body-section-menu">
		<section class="levelMenu">
			<div class="container">
				<div class="col-md-2 col-sm-2">
					<a href="/Periodico/homepage.html" class="btn single"><span class="glyphBtn home"></span> home</a>
				</div>
				<div class="col-md-7 col-sm-7">
					<div class="btn-group">
						<a href="/Periodico/atual.html" class="btn group">sumário</a>
						<a href="javascript:;" class="btn group">« anterior</a>
						<a href="javascript:;" class="btn group selected">atual</a>
						<a href="javascript:;" class="btn group">próximo »</a>
					</div>
				</div>
				<div class="col-md-3 col-sm-3 share">
					Compartilhe
					<a href="" class="sendViaMail showTooltip" data-placement="top" title="Enviar link por e-mail"><span class="glyphBtn sendMail"></span></a>
					<a href="" class="shareFacebook showTooltip" data-placement="top" title="Compartilhar no Facebook"><span class="glyphBtn facebook"></span></a>
					<a href="" class="shareTwitter showTooltip" data-placement="top" title="Compartilhar no Twitter"><span class="glyphBtn twitter"></span></a>
					<a href="" class="showTooltip dropdown-toggle" data-toggle="dropdown" data-placement="top" title="Outras redes sociais"><span class="glyphBtn otherNetworks"></span></a>
					<ul class="dropdown-menu">
						<li class="dropdown-header">Outras redes sociais</li>
						<li><a href="" class="shareGooglePlus"><span class="glyphBtn googlePlus"></span> Google+</a></li>
						<li><a href="" class="shareLinkedIn"><span class="glyphBtn linkedIn"></span> LinkedIn</a></li>
						<li><a href="" class="shareReddit"><span class="glyphBtn reddit"></span> Reddit</a></li>
						<li><a href="" class="shareStambleUpon"><span class="glyphBtn stambleUpon"></span> StambleUpon</a></li>
						<li><a href="" class="shareCiteULike"><span class="glyphBtn citeULike"></span> CiteULike</a></li>
						<li><a href="" class="shareMendeley"><span class="glyphBtn mendeley"></span> Mendeley</a></li>
					</ul>
				</div>
			</div>
		</section>
	</xsl:template>
    <xsl:template match="/">
		<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
		<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
		<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
		<!--[if gt IE 8]><!--> 
    	<html class="no-js"> <!--<![endif]-->
			<head>
				<meta charset="utf-8"/>
				<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>
				<xsl:apply-templates select="." mode="html-head-title"></xsl:apply-templates>
				<xsl:apply-templates select="." mode="article-html-meta"></xsl:apply-templates>
				<xsl:apply-templates select="." mode="css"></xsl:apply-templates>
				<link rel="alternate" type="application/rss+xml" title="SciELO" href=""/>
				<!--[if lt IE 9]>
					<script src="../static/js/vendor/html5-3.6-respond-1.1.0.min.js"></script>
				<![endif]-->
			</head>
			<body class="journal article">
				<a name="top"></a>
				<xsl:apply-templates select="." mode="html-body-section-menu"></xsl:apply-templates>
				<xsl:apply-templates select="." mode="article"></xsl:apply-templates>		
				<xsl:apply-templates select="." mode="article-modals"></xsl:apply-templates>
				<xsl:apply-templates select="." mode="journal-contacts"></xsl:apply-templates>
				<xsl:apply-templates select="." mode="html-body-footer"></xsl:apply-templates>
				<xsl:apply-templates select="." mode="alternative-header"></xsl:apply-templates>
				<xsl:apply-templates select="." mode="floating-menu"></xsl:apply-templates>
				<xsl:apply-templates select="." mode="article-modals-automatic-translation"></xsl:apply-templates>
				<xsl:apply-templates select="." mode="article-modals-send-by-email"></xsl:apply-templates>
				<xsl:apply-templates select="." mode="article-modals-services"></xsl:apply-templates>		
				<xsl:apply-templates select="." mode="js"></xsl:apply-templates>
			</body>
		</html>
   </xsl:template>
	<xsl:template match="/" mode="article-modals-services">
		<div class="modal fade ModalDefault" id="ModalDownloads" tabindex="-1" role="dialog" aria-hidden="true">
			<div class="modal-dialog">
				<div class="modal-content">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&amp;times;</span><span class="sr-only">Close</span></button>
						<h4 class="modal-title">Versão para download</h4>
					</div>
					<div class="modal-body">
						<div class="row modal-center">
							<div class="col-md-3">
								<span class="glyphBtn pdfDownloadMid"></span>
								<br/>
								<strong>PDF</strong>
								<ul class="md-list">
									<li><a href="">Espanhol</a></li>
									<li><a href="">Inglês</a></li>
									<li><a href="">Português</a></li>
								</ul>
							</div>
							<div class="col-md-3">
								<span class="glyphBtn epubDownloadMid"></span>
								<br/>
								<strong>ePUB</strong>
								<ul class="md-list">
									<li><a href="">Espanhol</a></li>
									<li><a href="">Inglês</a></li>
									<li><a href="">Português</a></li>
								</ul>
							</div>
							<div class="col-md-3">
								<span class="glyphBtn readcubeViewMid"></span>
								<br/>
								<strong>ReadCube</strong>
								<ul class="md-list">
									<li class="colspan3"><a href="">Visualizar <br/>o texto</a></li>
								</ul>
							</div>
							<div class="col-md-3">
								<span class="glyphBtn xmlDownloadMid"></span>
								<br/>
								<strong>XML</strong>
								<ul class="md-list">
									<li><a href="">Espanhol</a></li>
									<li><a href="">Inglês</a></li>
									<li><a href="">Português</a></li>
								</ul>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</xsl:template>
	<xsl:template match="/" mode="article-modals-send-by-email">
		<div class="modal fade" id="SendViaEmail" tabindex="-1" role="dialog" aria-hidden="true">
			<div class="modal-dialog">
				<div class="modal-content">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&amp;times;</span><span class="sr-only">Close</span></button>
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
	</xsl:template>
	<xsl:template match="/" mode="article-modals-automatic-translation">
		<div class="modal fade" id="translateArticleModal" tabindex="-1" role="dialog" aria-hidden="true">
			<div class="modal-dialog">
				<div class="modal-content">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&amp;times;</span><span class="sr-only">Fechar</span></button>
						<h4 class="modal-title">Automatic translation using @Google@ Translator service</h4>
					</div>
					<div class="modal-body">
						<p>This is an automatic translation that represents a best effort but it was not reviewed by the author and might have imperfections.</p>
						<table>
							<thead>
								<tr>
									<th colspan="3"><a href="" target="_top"><span class="glyphFlags BR"></span>Portuguese</a></th>
									<th colspan="3"><a href="" target="_top"><span class="glyphFlags ES"></span> Spanish</a></th>
								</tr>
							</thead>
						</table>
						<div class="dashline">
							<h4>Others:</h4>
						</div>
						<table>
							<tbody>
								
								<tr>
									<td>
										<a href="http://www.scielo.br/scieloOrg/php/translateCallAndLog.php?date=&amp;translator=google&amp;tlang=en&amp;tlang2=af&amp;lang=en&amp;pid=S0102-695X2011000300029&amp;script=sci_arttext&amp;url=http%3A%2F%2Fwww.scielo.br%2Fscielo.php%3Fscript%3Dsci_arttext%26pid%3DS0102-695X2011000300029%26lng%3Den%26nrm%3Diso%26tlng%3Den" target="_top">Afrikaans</a>
									</td>
									<td>
										<a href="http://www.scielo.br/scieloOrg/php/translateCallAndLog.php?date=&amp;translator=google&amp;tlang=en&amp;tlang2=ar&amp;lang=en&amp;pid=S0102-695X2011000300029&amp;script=sci_arttext&amp;url=http%3A%2F%2Fwww.scielo.br%2Fscielo.php%3Fscript%3Dsci_arttext%26pid%3DS0102-695X2011000300029%26lng%3Den%26nrm%3Diso%26tlng%3Den" target="_top">Arabic</a>
									</td>
									<td>
										<a href="http://www.scielo.br/scieloOrg/php/translateCallAndLog.php?date=&amp;translator=google&amp;tlang=en&amp;tlang2=az&amp;lang=en&amp;pid=S0102-695X2011000300029&amp;script=sci_arttext&amp;url=http%3A%2F%2Fwww.scielo.br%2Fscielo.php%3Fscript%3Dsci_arttext%26pid%3DS0102-695X2011000300029%26lng%3Den%26nrm%3Diso%26tlng%3Den" target="_top">Azerbaijani ALPHA</a>
									</td>
									<td>
										<a href="http://www.scielo.br/scieloOrg/php/translateCallAndLog.php?date=&amp;translator=google&amp;tlang=en&amp;tlang2=be&amp;lang=en&amp;pid=S0102-695X2011000300029&amp;script=sci_arttext&amp;url=http%3A%2F%2Fwww.scielo.br%2Fscielo.php%3Fscript%3Dsci_arttext%26pid%3DS0102-695X2011000300029%26lng%3Den%26nrm%3Diso%26tlng%3Den" target="_top">Belarusian</a>
									</td>
									<td>
										<a href="http://www.scielo.br/scieloOrg/php/translateCallAndLog.php?date=&amp;translator=google&amp;tlang=en&amp;tlang2=ca&amp;lang=en&amp;pid=S0102-695X2011000300029&amp;script=sci_arttext&amp;url=http%3A%2F%2Fwww.scielo.br%2Fscielo.php%3Fscript%3Dsci_arttext%26pid%3DS0102-695X2011000300029%26lng%3Den%26nrm%3Diso%26tlng%3Den" target="_top">Catalan</a>
									</td>
									<td>
										<a href="http://www.scielo.br/scieloOrg/php/translateCallAndLog.php?date=&amp;translator=google&amp;tlang=en&amp;tlang2=da&amp;lang=en&amp;pid=S0102-695X2011000300029&amp;script=sci_arttext&amp;url=http%3A%2F%2Fwww.scielo.br%2Fscielo.php%3Fscript%3Dsci_arttext%26pid%3DS0102-695X2011000300029%26lng%3Den%26nrm%3Diso%26tlng%3Den" target="_top">Danish</a>
									</td>
								</tr>
								<tr>
									<td>
										<a href="http://www.scielo.br/scieloOrg/php/translateCallAndLog.php?date=&amp;translator=google&amp;tlang=en&amp;tlang2=tl&amp;lang=en&amp;pid=S0102-695X2011000300029&amp;script=sci_arttext&amp;url=http%3A%2F%2Fwww.scielo.br%2Fscielo.php%3Fscript%3Dsci_arttext%26pid%3DS0102-695X2011000300029%26lng%3Den%26nrm%3Diso%26tlng%3Denn" target="_top">Filipino</a>
									</td>
									<td>
										<a href="http://www.scielo.br/scieloOrg/php/translateCallAndLog.php?date=&amp;translator=google&amp;tlang=en&amp;tlang2=ka&amp;lang=en&amp;pid=S0102-695X2011000300029&amp;script=sci_arttext&amp;url=http%3A%2F%2Fwww.scielo.br%2Fscielo.php%3Fscript%3Dsci_arttext%26pid%3DS0102-695X2011000300029%26lng%3Den%26nrm%3Diso%26tlng%3Den" target="_top">French</a>
									</td>
									<td>
										<a href="http://www.scielo.br/scieloOrg/php/translateCallAndLog.php?date=&amp;translator=google&amp;tlang=en&amp;tlang2=ka&amp;lang=en&amp;pid=S0102-695X2011000300029&amp;script=sci_arttext&amp;url=http%3A%2F%2Fwww.scielo.br%2Fscielo.php%3Fscript%3Dsci_arttext%26pid%3DS0102-695X2011000300029%26lng%3Den%26nrm%3Diso%26tlng%3Den" target="_top">Georgian ALPHA</a>
									</td>
									<td>
										<a href="http://www.scielo.br/scieloOrg/php/translateCallAndLog.php?date=&amp;translator=google&amp;tlang=en&amp;tlang2=el&amp;lang=en&amp;pid=S0102-695X2011000300029&amp;script=sci_arttext&amp;url=http%3A%2F%2Fwww.scielo.br%2Fscielo.php%3Fscript%3Dsci_arttext%26pid%3DS0102-695X2011000300029%26lng%3Den%26nrm%3Diso%26tlng%3Den" target="top">Greek</a>
									</td>
									<td>
										<a href="http://www.scielo.br/scieloOrg/php/translateCallAndLog.php?date=&amp;translator=google&amp;tlang=en&amp;tlang2=hi&amp;lang=en&amp;pid=S0102-695X2011000300029&amp;script=sci_arttext&amp;url=http%3A%2F%2Fwww.scielo.br%2Fscielo.php%3Fscript%3Dsci_arttext%26pid%3DS0102-695X2011000300029%26lng%3Den%26nrm%3Diso%26tlng%3Den" target="top">Hindi</a>
									</td>
									<td>
										<a href="http://www.scielo.br/scieloOrg/php/translateCallAndLog.php?date=&amp;translator=google&amp;tlang=en&amp;tlang2=da&amp;lang=en&amp;pid=S0102-695X2011000300029&amp;script=sci_arttext&amp;url=http%3A%2F%2Fwww.scielo.br%2Fscielo.php%3Fscript%3Dsci_arttext%26pid%3DS0102-695X2011000300029%26lng%3Den%26nrm%3Diso%26tlng%3Den" target="top">Danish</a>
									</td>
								</tr>
								<tr>
									<td>
										<a href="http://www.scielo.br/scieloOrg/php/translateCallAndLog.php?date=&amp;translator=google&amp;tlang=en&amp;tlang2=is&amp;lang=en&amp;pid=S0102-695X2011000300029&amp;script=sci_arttext&amp;url=http%3A%2F%2Fwww.scielo.br%2Fscielo.php%3Fscript%3Dsci_arttext%26pid%3DS0102-695X2011000300029%26lng%3Den%26nrm%3Diso%26tlng%3Den" target="top">Icelandic</a>
									</td>
									<td>
										<a href="http://www.scielo.br/scieloOrg/php/translateCallAndLog.php?date=&amp;translator=google&amp;tlang=en&amp;tlang2=ga&amp;lang=en&amp;pid=S0102-695X2011000300029&amp;script=sci_arttext&amp;url=http%3A%2F%2Fwww.scielo.br%2Fscielo.php%3Fscript%3Dsci_arttext%26pid%3DS0102-695X2011000300029%26lng%3Den%26nrm%3Diso%26tlng%3Den" target="top">Irish</a>
									</td>
									<td>
										<a href="http://www.scielo.br/scieloOrg/php/translateCallAndLog.php?date=&amp;translator=google&amp;tlang=en&amp;tlang2=ga&amp;lang=en&amp;pid=S0102-695X2011000300029&amp;script=sci_arttext&amp;url=http%3A%2F%2Fwww.scielo.br%2Fscielo.php%3Fscript%3Dsci_arttext%26pid%3DS0102-695X2011000300029%26lng%3Den%26nrm%3Diso%26tlng%3Den" target="top">Irish</a>
									</td>
									<td>
										<a href="http://www.scielo.br/scieloOrg/php/translateCallAndLog.php?date=&amp;translator=google&amp;tlang=en&amp;tlang2=ja&amp;lang=en&amp;pid=S0102-695X2011000300029&amp;script=sci_arttext&amp;url=http%3A%2F%2Fwww.scielo.br%2Fscielo.php%3Fscript%3Dsci_arttext%26pid%3DS0102-695X2011000300029%26lng%3Den%26nrm%3Diso%26tlng%3Den" target="top">Japanese</a>
									</td>
									<td>
										<a href="http://www.scielo.br/scieloOrg/php/translateCallAndLog.php?date=&amp;translator=google&amp;tlang=en&amp;tlang2=lv&amp;lang=en&amp;pid=S0102-695X2011000300029&amp;script=sci_arttext&amp;url=http%3A%2F%2Fwww.scielo.br%2Fscielo.php%3Fscript%3Dsci_arttext%26pid%3DS0102-695X2011000300029%26lng%3Den%26nrm%3Diso%26tlng%3Den" target="top">Latvian</a>
									</td>
									<td>
										<a href="http://www.scielo.br/scieloOrg/php/translateCallAndLog.php?date=&amp;translator=google&amp;tlang=en&amp;tlang2=mk&amp;lang=en&amp;pid=S0102-695X2011000300029&amp;script=sci_arttext&amp;url=http%3A%2F%2Fwww.scielo.br%2Fscielo.php%3Fscript%3Dsci_arttext%26pid%3DS0102-695X2011000300029%26lng%3Den%26nrm%3Diso%26tlng%3Den" target="top">Macedonian</a>
									</td>
								</tr>
								<tr>
									<td>
										<a href="http://www.scielo.br/scieloOrg/php/translateCallAndLog.php?date=&amp;translator=google&amp;tlang=en&amp;tlang2=mt&amp;lang=en&amp;pid=S0102-695X2011000300029&amp;script=sci_arttext&amp;url=http%3A%2F%2Fwww.scielo.br%2Fscielo.php%3Fscript%3Dsci_arttext%26pid%3DS0102-695X2011000300029%26lng%3Den%26nrm%3Diso%26tlng%3Den" target="top">Maltese</a>
									</td>
									<td>
										<a href="http://www.scielo.br/scieloOrg/php/translateCallAndLog.php?date=&amp;translator=google&amp;tlang=en&amp;tlang2=fa&amp;lang=en&amp;pid=S0102-695X2011000300029&amp;script=sci_arttext&amp;url=http%3A%2F%2Fwww.scielo.br%2Fscielo.php%3Fscript%3Dsci_arttext%26pid%3DS0102-695X2011000300029%26lng%3Den%26nrm%3Diso%26tlng%3Den" target="top">Persian</a>
									</td>
									<td>
										<a href="http://www.scielo.br/scieloOrg/php/translateCallAndLog.php?date=&amp;translator=google&amp;tlang=en&amp;tlang2=ru&amp;lang=en&amp;pid=S0102-695X2011000300029&amp;script=sci_arttext&amp;url=http%3A%2F%2Fwww.scielo.br%2Fscielo.php%3Fscript%3Dsci_arttext%26pid%3DS0102-695X2011000300029%26lng%3Den%26nrm%3Diso%26tlng%3Den" target="top">Russian</a>
									</td>
									<td>
										<a href="http://www.scielo.br/scieloOrg/php/translateCallAndLog.php?date=&amp;translator=google&amp;tlang=en&amp;tlang2=ja&amp;lang=en&amp;pid=S0102-695X2011000300029&amp;script=sci_arttext&amp;url=http%3A%2F%2Fwww.scielo.br%2Fscielo.php%3Fscript%3Dsci_arttext%26pid%3DS0102-695X2011000300029%26lng%3Den%26nrm%3Diso%26tlng%3Den" target="top">Slovak</a>
									</td>
									<td>
										<a href="Turkish" target="top">Swedish</a>
									</td>
									<td>
										<a href="http://www.scielo.br/scieloOrg/php/translateCallAndLog.php?date=&amp;translator=google&amp;tlang=en&amp;tlang2=tr&amp;lang=en&amp;pid=S0102-695X2011000300029&amp;script=sci_arttext&amp;url=http%3A%2F%2Fwww.scielo.br%2Fscielo.php%3Fscript%3Dsci_arttext%26pid%3DS0102-695X2011000300029%26lng%3Den%26nrm%3Diso%26tlng%3Den" target="top">Turkish</a>
									</td>
								</tr>
							</tbody>
						</table>
					</div>
					<div class="modal-footer">
						
					</div>
				</div>
			</div>
		</div>
		
	</xsl:template>
	<xsl:template match="/" mode="floating-menu">
		<ul class="floatingMenu fm-slidein" data-fm-toogle="hover">
			<li class="fm-wrap">
				<a href="#" class="fm-button-main">
					<span class="glyphFloatMenu fm-ico-hamburguer"></span>
					<span class="glyphFloatMenu fm-ico-close"></span>
				</a>
				<ul class="fm-list">
					<li>
						<a class="fm-button-child" data-fm-label="Download" data-toggle="modal" data-target="#ModalDownloads">
							<span class="glyphFloatMenu fm-ico-download"></span>	
						</a>
					</li>
					<li>
						<a class="fm-button-child" data-fm-label="Figuras e tabelas" data-toggle="modal" data-target="#ModalTablesFigures">
							<span class="glyphFloatMenu fm-ico-pictures-tables"></span>
						</a>
					</li>
					<li>
						<a class="fm-button-child" data-fm-label="Versões e traduções" data-toggle="modal" data-target="#ModalVersionsTranslations">
							<span class="glyphFloatMenu fm-ico-versions-translations"></span>
						</a>
					</li>
					<li>
						<a class="fm-button-child" data-fm-label="Como citar este artigo" data-toggle="modal" data-target="#ModalArticles">
							<span class="glyphFloatMenu fm-ico-articles"></span>
						</a>
					</li>
					<li>
						<a class="fm-button-child" data-fm-label="Métricas" data-toggle="modal" data-target="#ModalMetrics">
							<span class="glyphFloatMenu fm-ico-metrics"></span>
						</a>
					</li>
					<li>
						<a class="fm-button-child" data-fm-label="Artigos e similares" data-toggle="modal" data-target="#ModalRelatedArticles">
							<span class="glyphFloatMenu fm-ico-articles-thelike"></span>
						</a>
					</li>	
				</ul>
			</li>
		</ul>
	</xsl:template>
	<xsl:template match="/" mode="journal-contacts">
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
	</xsl:template>
	<xsl:template match="/" mode="html-body-footer">
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
	</xsl:template>
	<xsl:template match="/" mode="alternative-header">
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
				<div class="col-md-6 col-sm-6 journalInfo">
					<ul>
						<li>
							<a href="" class="dropdown-toggle" data-toggle="dropdown"><span class="text"><span class="truncate">Brazilian Journal of Medical and Biological Research </span><span class="glyphBtn grayArrowDown"></span></span></a>
							<ul class="dropdown-menu" role="menu">
								<div class="col-md-9 col-sm-8 brandLogo">
									<div class="row">
										<div class="col-md-3 hidden-sm">
											<img src="../static/trash/logo-biological.gif" alt="Logomarca do Boletim do Museu Paraense Emílio Goeldi"/>
										</div>
										<div class="col-md-9">
											<span class="theme">Ciências Biológicas</span>
											<h1>Brazilian Journal of Medical and Biological Research</h1>
										</div>
									</div>
								</div>
								<div class="col-md-3 col-sm-4 journalMenu">
									<ul>
										<li><a href="secundaria.html"><span class="glyphBtn submission"></span> Submissão de manuscritos</a></li>
										<li><a href="secundaria.html"><span class="glyphBtn authorInstructions"></span> Instruções aos autores</a></li>
										<li><a href="secundaria.html"><span class="glyphBtn about"></span> Sobre o periódico</a></li>
										<li><a href="secundaria.html"><span class="glyphBtn contact"></span> Contato</a></li>
									</ul>
								</div>
							</ul>
						</li>
					</ul>
				</div>
				<div class="col-md-2 col-md-offset-2 col-sm-3 journalMenu">
					<div class="language">
						<a href="index.en.html" class="lang-en" lang="en">English</a>
						<a href="index.es.html" class="lang-es" lang="es">Español</a>
					</div>
				</div>
			</div>
		</div>
	</xsl:template>
</xsl:stylesheet>