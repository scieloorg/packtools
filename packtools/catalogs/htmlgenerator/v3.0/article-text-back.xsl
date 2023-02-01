<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/article-text-back.xsl"/>

    <xsl:template match="fn-group" mode="back-section">
        <!--
            Insere o "título" da seção de notas de rodapé
        -->
        <div class="articleSection">
            <div class="row">
                <div class="col">
                    <ul class="refList articleFootnotes">
                        <xsl:apply-templates select="*|text()" mode="back-section-content"/>
                    </ul>
                </div>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="back/fn" mode="back-section">
        <!--
            Insere o "título" da seção de notas de rodapé
        -->
        <div>
            <xsl:attribute name="class">articleSection</xsl:attribute>
            <div class="row">
                <div class="col">
                    <ul class="refList articleFootnotes">
                        <xsl:apply-templates select="."/>
                    </ul>
                </div>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="*[title] | *[label]" mode="back-section">
        <div>
            <xsl:attribute name="class">articleSection</xsl:attribute>
            <xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="title"/></xsl:attribute>
            <h3>
                <xsl:attribute name="class">articleSectionTitle</xsl:attribute>
                <xsl:apply-templates select="." mode="title"/>
            </h3>
            <xsl:apply-templates select="*|text()" mode="back-section-content"/>
        </div>
    </xsl:template>

    <xsl:template match="text()" mode="back-section-content">
        <xsl:value-of select="."/>
    </xsl:template>

    <xsl:template match="*" mode="back-section-content">
        <xsl:apply-templates select="."/>
    </xsl:template>

    <xsl:template match="title|label" mode="back-section-content">
        <!-- do nothing -->
    </xsl:template>
</xsl:stylesheet>