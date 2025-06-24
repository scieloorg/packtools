<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/html-modals.xsl"/>

    <xsl:template match="article" mode="modal-header-content">
        <h5 class="modal-title"><xsl:value-of select="$graphic_elements_title"/></h5>
        <button class="btn-close" data-bs-dismiss="modal">
            <xsl:attribute name="aria-label">
                <xsl:apply-templates select="." mode="interface">
                    <xsl:with-param name="text">Close</xsl:with-param>
                </xsl:apply-templates>
            </xsl:attribute>
        </button>
    </xsl:template>

    <xsl:template match="article" mode="modal-grouped-figs-tables-schemes">
        <!--
            Modal que apresenta juntos figuras, tabelas e fórmulas presentes
            em um dado idioma do texto do artigo
        -->
        <xsl:variable name="total_figs">
            <xsl:apply-templates select="." mode="get-total">
                <xsl:with-param name="content_type">figures</xsl:with-param>
            </xsl:apply-templates>
        </xsl:variable>
        <xsl:variable name="total_tables">
            <xsl:apply-templates select="." mode="get-total">
                <xsl:with-param name="content_type">tables</xsl:with-param>
            </xsl:apply-templates>
        </xsl:variable>
        <xsl:variable name="total_formulas">
            <xsl:apply-templates select="." mode="get-total">
                <xsl:with-param name="content_type">schemes</xsl:with-param>
            </xsl:apply-templates>
        </xsl:variable>
        <xsl:if test="number($total_figs) + number($total_tables) + number($total_formulas) &gt; 0">
             <div class="modal fade ModalDefault" id="ModalTablesFigures" tabindex="-1" role="dialog" aria-hidden="true">
                 <div class="modal-dialog">
                     <div class="modal-content">
                         <div class="modal-header">
                            <xsl:apply-templates select="." mode="modal-header-content"/>
                         </div>
                         <div class="modal-body">
                             <ul class="nav nav-tabs" role="tablist">
                                <xsl:apply-templates select="." mode="generic-tab-title-and-total">
                                    <xsl:with-param name="previous_tab_total">0</xsl:with-param>
                                    <xsl:with-param name="total" select="$total_figs"/>
                                    <xsl:with-param name="title">Figures</xsl:with-param>
                                    <xsl:with-param name="content_type">figures</xsl:with-param>
                                </xsl:apply-templates>

                                <xsl:apply-templates select="." mode="generic-tab-title-and-total">
                                    <xsl:with-param name="previous_tab_total"><xsl:value-of select="$total_figs"/></xsl:with-param>
                                    <xsl:with-param name="total" select="$total_tables"/>
                                    <xsl:with-param name="title">Tables</xsl:with-param>
                                    <xsl:with-param name="content_type">tables</xsl:with-param>
                                </xsl:apply-templates>

                                <xsl:apply-templates select="." mode="generic-tab-title-and-total">
                                    <xsl:with-param name="previous_tab_total"><xsl:value-of select="number($total_figs)+number($total_formulas)"/></xsl:with-param>
                                    <xsl:with-param name="total" select="$total_formulas"/>
                                    <xsl:with-param name="title">Formulas</xsl:with-param>
                                    <xsl:with-param name="content_type">schemes</xsl:with-param>
                                </xsl:apply-templates>
                             </ul>
                             <div class="clearfix"></div>
                             <div class="tab-content">
                                <xsl:apply-templates select="." mode="generic-tab-panel">
                                    <xsl:with-param name="previous_tab_total">0</xsl:with-param>
                                    <xsl:with-param name="total" select="$total_figs"/>
                                    <xsl:with-param name="content_type">figures</xsl:with-param>
                                </xsl:apply-templates>

                                <xsl:apply-templates select="." mode="generic-tab-panel">
                                    <xsl:with-param name="previous_tab_total"><xsl:value-of select="$total_figs"/></xsl:with-param>
                                    <xsl:with-param name="total" select="$total_tables"/>
                                    <xsl:with-param name="content_type">tables</xsl:with-param>
                                </xsl:apply-templates>

                                <xsl:apply-templates select="." mode="generic-tab-panel">
                                    <xsl:with-param name="previous_tab_total"><xsl:value-of select="number($total_figs)+number($total_formulas)"/></xsl:with-param>
                                    <xsl:with-param name="total" select="$total_formulas"/>
                                    <xsl:with-param name="content_type">schemes</xsl:with-param>
                                </xsl:apply-templates>
                             </div>
                         </div>
                     </div>
                 </div>
             </div>
         </xsl:if>
    </xsl:template>

    <xsl:template match="article" mode="generic-tab-title-and-total">
        <xsl:param name="previous_tab_total">0</xsl:param>
        <xsl:param name="total"/>
        <xsl:param name="title"/>
        <xsl:param name="content_type"/>

        <xsl:if test="number($total) &gt; 0">
            <!--
                cria aba com rótulo "$title ($total)" 
            -->
            <li role="presentation">
                <xsl:attribute name="class">nav-item</xsl:attribute>
                <a>
                    <xsl:attribute name="href">#<xsl:value-of select="$content_type"/></xsl:attribute>
                    <xsl:attribute name="class">nav-link<xsl:if test="number($previous_tab_total) = 0"> active</xsl:if></xsl:attribute>
                    <xsl:attribute name="data-bs-toggle">tab</xsl:attribute>

                    <xsl:apply-templates select="." mode="interface">
                        <xsl:with-param name="text" select="$title"/>
                    </xsl:apply-templates>
                    (<xsl:value-of select="$total"/>)
                </a>
            </li>
        </xsl:if>
    </xsl:template>

    <xsl:template match="article" mode="generic-tab-panel">
        <xsl:param name="previous_tab_total">0</xsl:param>
        <xsl:param name="total"/>
        <xsl:param name="content_type"/>

        <xsl:if test="number($total) &gt; 0">
            <!--
                cria o conteúdo da aba do rótulo "$title ($total)" 
            -->
            <div>
                <xsl:attribute name="class">tab-pane fade show<xsl:if test="number($previous_tab_total) = 0"> active</xsl:if></xsl:attribute>

                <xsl:attribute name="id"><xsl:value-of select="$content_type"/></xsl:attribute>
                <xsl:attribute name="role">tabpanel</xsl:attribute>
                <xsl:attribute name="aria-labelledby"><xsl:value-of select="$content_type"/></xsl:attribute>

                <xsl:variable name="translation" select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']"/>

                <xsl:choose>
                    <xsl:when test="$translation">
                        <xsl:apply-templates select="front | $translation | back" mode="generic-tab-content">
                            <xsl:with-param name="tab_content_type" select="$content_type"/>
                        </xsl:apply-templates>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:apply-templates select="front | body | back" mode="generic-tab-content">
                            <xsl:with-param name="tab_content_type" select="$content_type"/>
                        </xsl:apply-templates>
                    </xsl:otherwise>
                </xsl:choose>

            </div>
        </xsl:if>
    </xsl:template>

    <xsl:template match="fig-group[@id] | fig" mode="tab-content">
        <!--
            Para fig-group e fig, cria no conteúdo da ABA "Figures":
            - a miniatura

            Para fig-group:
            - legendas de uma figura (label e caption em mais de um idioma)

            Para fig:
            - legenda de uma figura (label e caption em um idioma)
        -->
        <div class="row fig">
            <!-- miniatura -->
            <xsl:variable name="location">
                <xsl:apply-templates select=".//alternatives" mode="file-location-thumb"/>
            </xsl:variable>
            <xsl:variable name="figid"><xsl:apply-templates select="." mode="figure-id"/></xsl:variable>
            <div class="col-4">
                <a data-bs-toggle="modal" data-bs-target="#ModalFig{$figid}">
                    <div>
                        <xsl:choose>
                            <xsl:when test="$location != ''">
                                <xsl:attribute name="class">thumbImg</xsl:attribute>
                                <img>
                                    <xsl:attribute name="src"><xsl:value-of select="$location"/></xsl:attribute>
                                    <xsl:apply-templates select="." mode="alt-text"/>
                                </img>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="class">thumbOff</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
                        Thumbnail
                        <div class="zoom"><span class="sci-ico-zoom"></span></div>
                    </div>
                </a>
            </div>
            <!-- legenda(s) -->
            <xsl:apply-templates select="." mode="tab-content-label-and-caption"></xsl:apply-templates>
        </div>
    </xsl:template>

    <xsl:template match="table-wrap-group[table-wrap] | table-wrap[not(@xml:lang)]" mode="tab-content">
        <!--
            Para table-wrap-group e table-wrap, cria no conteúdo da ABA "Tables":
            - a miniatura

            Para table-wrap-group:
            - legendas de uma tabela em mais de 1 idioma
            Para table-wrap:
            - legenda de uma tabela em 1 idioma
        -->
        <xsl:variable name="id"><xsl:apply-templates select="." mode="table-id"/></xsl:variable>
        <div class="row table">
            <!-- miniatura -->
            <div class="col-4">
                <a data-bs-toggle="modal" data-bs-target="#ModalTable{$id}">
                    <div class="thumbOff">
                        Thumbnail
                        <div class="zoom"><span class="sci-ico-zoom"></span></div>
                    </div>
                </a>
            </div>
            <!-- legenda -->
            <xsl:apply-templates select="." mode="tab-content-label-and-caption"></xsl:apply-templates>
        </div>
    </xsl:template>

    <xsl:template match="disp-formula[@id]" mode="tab-content">
        <!--
            cria no conteúdo da ABA "Scheme" a miniatura e legenda de uma fórmula
        -->
        <xsl:variable name="location"><xsl:apply-templates select=".//alternatives" mode="file-location-thumb"/></xsl:variable>
        <xsl:variable name="id"><xsl:apply-templates select="." mode="disp-formula-id"/></xsl:variable>

        <div class="row fig">
            <!-- miniatura -->
            <div class="col-4">
                <a data-bs-toggle="modal" data-bs-target="#ModalScheme{$id}">
                    <div>
                        <xsl:choose>
                            <xsl:when test="$location!=''">
                                <xsl:attribute name="class">thumbImg</xsl:attribute>
                                <img>
                                    <xsl:attribute name="src"><xsl:value-of select="$location"/></xsl:attribute>
                                </img>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="class">thumbOff</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
                        Thumbnail
                        <div class="zoom"><span class="sci-ico-zoom"></span></div>
                    </div>
                </a>
            </div>
            <!-- legenda -->
            <xsl:apply-templates select="." mode="tab-content-label-and-caption"></xsl:apply-templates>
        </div>
    </xsl:template>

    <xsl:template match="fig-group | table-wrap-group" mode="tab-content-label-and-caption">
        <!--
            cria as legendas de uma figura no conteúdo da ABA "Figures"
            cria no conteúdo da ABA "Tables" as legendas de uma tabela
        -->
        <div class="col-8">
            <div class="row">
                <xsl:apply-templates select="fig | table-wrap" mode="tab-content-label-and-caption"/>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="fig | table-wrap" mode="tab-content-label-and-caption">
        <!--
            Cria a legenda de uma figura no conteúdo da ABA "Figures" ou
            Cria a legenda de uma tabela no conteúdo da ABA "Tables"
        -->
        <xsl:apply-templates select="." mode="row-label-caption"/>
    </xsl:template>

    <xsl:template match="disp-formula[@id]" mode="tab-content-label-and-caption">
        <!--
            cria no conteúdo da ABA "Schemes" a legenda de uma fórmula
        -->
        <div class="col-8">
            <div class="row">
                <xsl:apply-templates select="label" mode="row-label-caption"/>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="*[label or caption]" mode="row-label-caption">
        <div class="col-12">
            <caption class="sr-only">
                <strong><xsl:apply-templates select="label"/></strong>
                <xsl:apply-templates select="caption"/>
            </caption>
        </div>
    </xsl:template>

</xsl:stylesheet>