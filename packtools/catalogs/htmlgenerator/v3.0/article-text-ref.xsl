<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/article-text-ref.xsl"/>

    <xsl:template match="back/ref-list" mode="back-section">
        <xsl:apply-templates select="."/>
    </xsl:template>
   
    <xsl:template match="ref-list">
        <xsl:choose>
            <xsl:when test="ref-list">
                <xsl:apply-templates select="*"/>
            </xsl:when>
            <xsl:otherwise>
                <div>
                <!-- manter pareado class="articleSection" e data-anchor="nome da seção no menu esquerdo" -->
                <div>
                    <xsl:call-template name="article-section-header">
                        <xsl:with-param name="title"><xsl:apply-templates select="." mode="title"/></xsl:with-param>
                    </xsl:call-template>
                    <div class="row">
                        <div class="col ref-list">
                            <ul class="refList articleFootnotes">
                                <xsl:apply-templates select="." mode="ref-items"/>
                            </ul>
                        </div>
                    </div>
                </div>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
 
    <xsl:template match="ref/label">
        <sup class="xref"><xsl:value-of select="."/></sup>
    </xsl:template>
 
    <xsl:template match="ref">
        <!--
            <li>
                <a class="" name="B1_ref"></a>
                Pellerin, R.J., Waminal, N.E. & Kim, H.H. 2019. FISH mapping of rDNA and telomeric repeats in 10 Senna species. Horticulture, Environment, and Biotechnology 60: 253-260.
            </li>                                                 
        -->
        <xsl:variable name="id"><xsl:value-of select="@id"/></xsl:variable>
        
        <li>
            <a class="" name="{@id}_ref"/>
            <xsl:apply-templates select="label | mixed-citation"/>
            <xsl:if test="element-citation//pub-id[@pub-id-type='doi'] or element-citation//ext-link">
                <br/>
                <xsl:apply-templates select="element-citation//pub-id[@pub-id-type='doi']" mode="ref"/>
                <xsl:apply-templates select="element-citation//ext-link" mode="ref"/>
            </xsl:if>
        </li>
    </xsl:template>

    <xsl:template match="ext-link | pub-id" mode="ref">
        <xsl:apply-templates select=".">
            <xsl:with-param name="symbol">» </xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="pub-id[@pub-id-type='doi']">
        <xsl:param name="symbol"></xsl:param>
        <xsl:variable name="access_text">
            <xsl:apply-templates select="." mode="interface">
                <xsl:with-param name="text">access_doi</xsl:with-param>
            </xsl:apply-templates>
        </xsl:variable>
        <xsl:variable name="new_tab_text">
            <xsl:apply-templates select="." mode="interface">
                <xsl:with-param name="text">opens_new_tab</xsl:with-param>
            </xsl:apply-templates>
        </xsl:variable>
        <xsl:variable name="external_resource_text">
            <xsl:apply-templates select="." mode="interface">
                <xsl:with-param name="text">external_resource</xsl:with-param>
            </xsl:apply-templates>
        </xsl:variable>
        <xsl:variable name="doi_url">https://doi.org/<xsl:value-of select="."/></xsl:variable>
        <xsl:variable name="aria_label">
            <xsl:value-of select="$access_text"/>
            <xsl:text> </xsl:text>
            <xsl:value-of select="$doi_url"/>
            <xsl:text>. </xsl:text>
            <xsl:value-of select="$new_tab_text"/>
            <xsl:text>. </xsl:text>
            <xsl:value-of select="$external_resource_text"/>
            <xsl:text>.</xsl:text>
        </xsl:variable>
        <a target="_blank" href="{$doi_url}" aria-label="{normalize-space($aria_label)}">
            <xsl:value-of select="$symbol"/><xsl:value-of select="$doi_url"/>
        </a>
    </xsl:template>
</xsl:stylesheet>