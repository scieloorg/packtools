<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    
    <xsl:include href="../v2.0/article-text-fn.xsl"/>

    <xsl:template match="@id" mode="anchor">
        <a name="{.}_ref"/>
    </xsl:template>

    <xsl:template match="fn" mode="div-fn-list-item">
        <li>
            <xsl:apply-templates select="@id" mode="anchor"/>
            <xsl:apply-templates select="*|text()" mode="div-fn-list-item"/>
        </li>
    </xsl:template>

    <xsl:template match="fn/label" mode="div-fn-list-item">
        <span class="xref big"><xsl:apply-templates select="*|text()"/></span>
    </xsl:template>

    <xsl:template match="fn-group | fn" mode="back-section-content">
        <div class="row">
            <div class="col">
                <ul class="refList articleFootnotes">
                    <xsl:apply-templates select="*[name()!='label']" mode="div-fn-list-item"/>
                </ul>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="fn | corresp | fn[@fn-type='edited-by'] | fn[@fn-type='data-availability']" mode="back-section-h">
        <!--
            Apresenta o título da seção no texto completo
        -->
        <xsl:variable name="name" select="@fn-type"/>
        <xsl:if test="not(preceding-sibling::node()) or preceding-sibling::*[1][not(@fn-type)] or preceding-sibling::*[1][@fn-type!=$name]">
            <h2 class="h5">
                <xsl:apply-templates select="." mode="back-section-title"/>
            </h2>
        </xsl:if>
    </xsl:template>

    <xsl:template match="fn | author-notes/*" mode="back-section-title">
        <xsl:choose>
            <xsl:when test="label">
                <xsl:apply-templates select="label"/>
            </xsl:when>
            <xsl:when test="title">
                <xsl:apply-templates select="title"/>
            </xsl:when>
            <xsl:when test="@fn-type">
                <xsl:apply-templates select="." mode="text-labels">
                    <xsl:with-param name="text">author-notes-fn-<xsl:value-of select="@fn-type"/></xsl:with-param>
                </xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="." mode="text-labels">
                    <xsl:with-param name="text"><xsl:value-of select="name()"/></xsl:with-param>
                </xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="author-notes" mode="author-notes-as-sections">
        <!-- apresenta todas as notas de autores -->
        <xsl:apply-templates select="*" mode="back-section"/>
    </xsl:template>

    <xsl:template match="fn | corresp" mode="back-section-menu">
        <xsl:variable name="name" select="@fn-type"/>
        <!--
        Evita que no menu apareça o mesmo título mais de uma vez 
        -->
        <xsl:if test="not(preceding-sibling::node()) or preceding-sibling::*[1][not(@fn-type)] or preceding-sibling::*[1][@fn-type!=$name]">
            <!-- manter pareado class="articleSection" e data-anchor="nome da seção no menu esquerdo" -->
            <xsl:attribute name="class">articleSection</xsl:attribute>
            <xsl:attribute name="data-anchor">
                <xsl:apply-templates select="." mode="back-section-title"/>
            </xsl:attribute>
        </xsl:if>
    </xsl:template>

    <xsl:template match="author-notes/*" mode="back-section-content">
        <xsl:apply-templates select="*[name()!='label']" mode="div-fn-list-item"/>
    </xsl:template>

</xsl:stylesheet>
