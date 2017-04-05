<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="*" mode="article-modals">
        <xsl:apply-templates select="." mode="modal-authors"/>
        <xsl:apply-templates select="." mode="modal-translations"/>
        <xsl:apply-templates select="." mode="modal-related-articles"/>
        <xsl:apply-templates select="." mode="modal-tables-figures"/>
        <xsl:apply-templates select="." mode="modal-tables"/>
        <xsl:apply-templates select="." mode="modal-articles"/>
        <xsl:apply-templates select="." mode="modal-metrics"/>
    </xsl:template>
    <xsl:template match="*" mode="modal-authors">
        <xsl:if test=".//article-meta//contrib[*]">
            <div class="modal fade ModalDefault" id="ModalTutors" tabindex="-1" role="dialog" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&#xd7;</span><span class="sr-only">Close</span></button>
                            <h4 class="modal-title"><xsl:apply-templates select="." mode="text-labels">
                                <xsl:with-param name="text">About the authors</xsl:with-param>
                            </xsl:apply-templates></h4>
                        </div>
                        <div class="modal-body">
                            <div class="info">
                                <xsl:apply-templates select=".//article-meta//contrib" mode="modal-author"></xsl:apply-templates>
                                <xsl:apply-templates select=".//article-meta//contrib-group/author-notes" mode="modal-author"></xsl:apply-templates>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </xsl:if>    
    </xsl:template>
    <xsl:template match="contrib" mode="modal-author">
        <div class="tutors">
            <strong><xsl:apply-templates select="name"/></strong>
            <br/>
            <xsl:apply-templates select="role"/>
            <xsl:apply-templates select="xref"/>
            <xsl:apply-templates select="author-notes"/>
            <xsl:if test="contrib-id">
                <ul class="md-list inline">
                    <xsl:apply-templates select="contrib-id" mode="li"></xsl:apply-templates>
                </ul>
            </xsl:if>
            <div class="clearfix"></div>
        </div>
    </xsl:template>
    <xsl:template match="contrib-id" mode="li">
        <li><xsl:apply-templates select="."></xsl:apply-templates></li>
    </xsl:template>
    <xsl:template match="author-notes" mode="modal-author">
        <div class="info">
            <h3><xsl:apply-templates select="title"></xsl:apply-templates></h3>
            <xsl:apply-templates select="*[name()!='title']|text()"></xsl:apply-templates>
        </div>
    </xsl:template>
    <xsl:template match="*" mode="modal-translations">
        <div class="modal fade ModalDefault" id="ModalVersionsTranslations" tabindex="-1" role="dialog" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <!-- FIXME -->
                        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&#xd7;</span><span class="sr-only">Close</span></button>
                        <h4 class="modal-title">Versões e tradução automática</h4>
                    </div>
                    <div class="modal-body">
                        <div class="row modal-center">
                            <div class="col-md-4 col-md-offset-1">
                                <strong>Texto</strong>
                                <ul class="md-list">
                                    <li><a href="">Inglês</a></li>
                                    <li><a href="">Português</a></li>
                                </ul>
                            </div>
                            <div class="col-md-2 md-body-dashVertical"></div>
                            <div class="col-md-4">
                                <strong>Tradução automática</strong>
                                <ul class="md-list">
                                    <li><a href="">Google Translator</a></li>
                                    <li><a href="">Microsoft Translator</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </xsl:template>
    <xsl:template match="*" mode="modal-related-articles">
        <!-- FIXME -->
        <div class="modal fade ModalDefault" id="ModalRelatedArticles" tabindex="-1" role="dialog" aria-hidden="true">
            <div class="modal-dialog modal-sm">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&#xd7;</span><span class="sr-only">Close</span></button>
                        <h4 class="modal-title">Artigos relacionados</h4>
                    </div>
                    <div class="modal-body">
                        <div class="modal-center">
                            <ul class="md-list inline">
                                <li class="colspan3"><a href="">Similares <br/>na Rede SciELO</a></li>
                                <li class="colspan3"><a href="">Projetos FAPESP</a></li>
                                <li class="colspan3"><a href="">Similares no Google</a></li>
                                <li class="colspan3"><a href="">uBIO</a></li>
                            </ul>
                            <div class="clearfix"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </xsl:template>
    <xsl:template match="*" mode="modal-tables-figures">
        <div class="modal fade ModalDefault" id="ModalTablesFigures" tabindex="-1" role="dialog" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&#xd7;</span><span class="sr-only">Close</span></button>
                        <h4 class="modal-title">Figuras e tabelas</h4><!-- FIXME -->
                    </div>
                    <div class="modal-body">
                        <ul class="nav nav-tabs md-tabs" role="tablist">
                            <xsl:if test=".//fig">
                                <li role="presentation" class="col-md-6 active">
                                    <a href="#figures" aria-controls="figures" role="tab" data-toggle="tab">
                                        <span class="glyphBtn figureIconGray"></span>
                                        Lista de figuras (<xsl:value-of select="count(.//body//fig)"/>)
                                    </a>
                                </li>
                            </xsl:if>
                            <xsl:if test=".//table-wrap">
                            <li role="presentation" class="col-md-6">
                                <a href="#tables" aria-controls="tables" role="tab" data-toggle="tab">
                                    <span class="glyphBtn tableIconGray"></span>
                                    Lista de tabelas (<xsl:value-of select="count(.//body//table-wrap)"/>)
                                </a>
                            </li>
                            </xsl:if>
                        </ul>
                        <div class="clearfix"></div>
                        <div class="tab-content">
                            <div role="tabpanel" class="tab-pane active" id="figures">
                                <xsl:apply-templates select=".//body//fig" mode="modal"></xsl:apply-templates>
                            </div>
                            <div role="tabpanel" class="tab-pane" id="tables">
                                <xsl:apply-templates select=".//body//table-wrap" mode="modal"></xsl:apply-templates>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </xsl:template>
    <xsl:template match="fig" mode="modal">
        <div class="row fig" id="{@id}">
            <div class="col-md-4">
                <!-- FIXME -->
                <div class="thumb" style="background-image: url(../static/trash/1414-431X-bjmbr-46-01-058-gf01.jpg);">
                    Thumbnail
                    <span class="glyphBtn zoomWhite"></span>
                </div>
            </div>
            <div class="col-md-8">
                <strong><xsl:value-of select="label"/></strong>
                <br/>
                <xsl:apply-templates select="caption"></xsl:apply-templates>
                <div class="preview" style="display: none;"><xsl:apply-templates select="graphic"></xsl:apply-templates></div>
            </div>
        </div>
    </xsl:template>
    <xsl:template match="table-wrap" mode="modal">
        <div class="row fig" id="{@id}">
            <div class="col-md-4">
                <a data-toggle="modal" data-target="#ModalTables">
                    <div class="thumbOff" style="background-image: url(../static/trash/artigo-tabela.jpg);">
                        Thumbnail
                        <span class="glyphBtn zoomWhite"></span>
                    </div>
                </a>
            </div>
            <div class="col-md-8">
                <strong><xsl:apply-templates select="label"></xsl:apply-templates></strong>
                <br/>
                <xsl:apply-templates select="caption"></xsl:apply-templates>
                
            </div>
        </div>
    </xsl:template>
    <xsl:template match="*" mode="modal-tables">
        <div class="modal fade ModalDefault" id="ModalTables" tabindex="-1" role="dialog" aria-hidden="true">
            <xsl:apply-templates select=".//body//table-wrap"></xsl:apply-templates>
        </div>
    </xsl:template>
    <xsl:template match="*" mode="modal-articles">
        <div class="modal fade ModalDefault" id="ModalArticles" tabindex="-1" role="dialog" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&#xd7;</span><span class="sr-only">Close</span></button>
                        <h4 class="modal-title">Como citar</h4>
                    </div>
                    <div class="modal-body">
                        <p>RODRIGUEZ-ANGULO, H. et al. Induction of chagasic-like arrhythmias in the isolated beating hearts of healthy rats perfused with Trypanosoma cruzi-conditioned medium. Braz J Med Biol Res [online]. 2013, vol.46, n.1 [cited  2015-01-23], pp. 58-64 . Available from: &amp;lt;http://www.scielo.br/scielo.php?script=sci_arttext&amp;pid=S0100-879X2013000100058&amp;lng=en&amp;nrm=iso&amp;gt;. Epub Jan 11, 2013. ISSN 1414-431X.  http://dx.doi.org/10.1590/1414-431X20122409.</p>
                        <a href="javascript:;" class="copyLink outlineFadeLink" data-clipboard-text="RODRIGUEZ-ANGULO, H. et al. Induction of chagasic-like arrhythmias in the isolated beating hearts of healthy rats perfused with Trypanosoma cruzi-conditioned medium. Braz J Med Biol Res [online]. 2013, vol.46, n.1 [cited  2015-01-23], pp. 58-64 . Available from: &amp;lt;http://www.scielo.br/scielo.php?script=sci_arttext&amp;pid=S0100-879X2013000100058&amp;lng=en&amp;nrm=iso&amp;gt;. Epub Jan 11, 2013. ISSN 1414-431X.  http://dx.doi.org/10.1590/1414-431X20122409."><span class="glyphBtn copyIcon"></span> Copiar</a>
                        
                        <div class="row" id="how2cite-export">
                            <div class="col-md-2 col-sm-2">
                                <a href="http://www.scielo.br/scielo.php?download&amp;format=BibTex&amp;pid=S1981-81222013000300008" class="midGlyph download">
                                    BibText
                                </a>
                            </div>
                            <div class="col-md-2 col-sm-2">
                                <a href="http://www.scielo.br/scielo.php?download&amp;format=RefMan&amp;pid=S1981-81222013000300008" class="midGlyph download">
                                    Reference Manager
                                </a>
                            </div>
                            <div class="col-md-2 col-sm-2">
                                <a href="http://www.scielo.br/scielo.php?download&amp;format=RefMan&amp;pid=S1981-81222013000300008" class="midGlyph download">
                                    ProCite
                                </a>
                            </div>
                            <div class="col-md-2 col-sm-2">
                                <a href="http://www.scielo.br/scielo.php?download&amp;format=RefMan&amp;pid=S1981-81222013000300008" class="midGlyph download">
                                    End Note
                                </a>
                            </div>
                            <div class="col-md-2 col-sm-2">
                                <a href="http://www.scielo.br/scielo.php?download&amp;format=RefMan&amp;pid=S1981-81222013000300008" class="midGlyph download">
                                    Refworks
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </xsl:template>
    <xsl:template match="*" mode="modal-metrics">
        <div class="modal fade ModalDefault" id="ModalMetrics" tabindex="-1" role="dialog" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&#xd7;</span><span class="sr-only">Close</span></button>
                        <h4 class="modal-title">Métricas</h4>
                    </div>
                    <div class="modal-body">
                        <ul class="nav nav-tabs md-tabs" role="tablist">
                            <li role="presentation" class="col-md-6 active">
                                <a href="#tab-metric-download" aria-controls="tab-metric-download" role="tab" data-toggle="tab">
                                    SciELO Analytics
                                </a>
                            </li>
                            <li role="presentation" class="col-md-6">
                                <a href="#tab-metric-altmetric" aria-controls="tab-metric-altmetric" role="tab" data-toggle="tab">
                                    Altmetrics
                                </a>
                            </li>
                        </ul>
                        <div class="clearfix"></div>
                        <div class="tab-content">
                            <div class="tab-pane active" id="tab-metric-download">
                                <div class="row">
                                    <div class="col-md-6 col-md-offset-3">
                                        <a href="http://analytics.scielo.org/w/accesses?document=S0100-879X2013000100058&amp;collection=" class="outlineFadeLink" target="_blank">Downloads</a>
                                    </div>
                                    <div class="col-md-6 col-md-offset-3">
                                        <a href="http://analytics.scielo.org/w/accesses?document=S0100-879X2013000100058&amp;collection=" class="outlineFadeLink" target="_blank">Citações</a>
                                    </div>
                                </div>
                            </div>
                            <div class="tab-pane" id="tab-metric-altmetric">
                                <div class="row">
                                    <div class="col-md-4 col-sm-4 center">
                                        <script type="text/javascript" src="https://d1bxh8uas1mnw7.cloudfront.net/assets/embed.js"></script>
                                        <div class="altmetric-embed" data-badge-type="large-donut" data-doi="10.1590/S1981-81222013000300008"></div>
                                    </div>
                                    <div class="col-md-8 col-sm-8">
                                        <p>SciELO has partnered with altmetric.com to bring you greater insight into the online attention surrounding this article.</p>
                                        <p>Altmetric hasn't tracked any mentions of this article yet. Please check back later to see if anything has changed.</p>
                                        <p>Have you blogged, tweeted or written a story about this article? <a href="mailto:support@altmetric.com">Let us know</a> if we've missed it somehow.</p>
                                        <p>Want to be alerted when we see this article? Sign up for <a href="http://www.altmetric.com/details.php?domain=www.scielo.br&amp;doi=10.1590/1414-431x20122409#getEmailUpdates" target="_blank">email updates when this article is shared</a>.</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </xsl:template>
</xsl:stylesheet>