<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/html-modals.xsl"/>

    <xsl:template match="article" mode="modal-header-content">
        <xsl:param name="graphic_elements_title"/>

        <h5 class="modal-title"><xsl:value-of select="$graphic_elements_title"/></h5>
        <button class="btn-close" data-bs-dismiss="modal">
            <xsl:attribute name="aria-label">
                <xsl:apply-templates select="." mode="interface">
                    <xsl:with-param name="text">Close</xsl:with-param>
                </xsl:apply-templates>
            </xsl:attribute>
        </button>
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
            <div class="col-md-4">
                <a data-bs-toggle="modal" data-bs-target="#ModalFig{$figid}">
                    <div>
                        <xsl:choose>
                            <xsl:when test="$location != ''">
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
            <div class="col-md-4">
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
            <div class="col-md-4">
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
</xsl:stylesheet>