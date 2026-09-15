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
        <div><span class="xref big"><xsl:apply-templates select="*|text()"/></span></div>
    </xsl:template>

    <xsl:template match="*" mode="back-section-title">
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
            <xsl:when test="@sec-type">
                <xsl:apply-templates select="." mode="text-labels">
                    <xsl:with-param name="text"><xsl:value-of select="@sec-type"/></xsl:with-param>
                </xsl:apply-templates>
            </xsl:when>
            <xsl:when test="name()='corresp'">
                <xsl:apply-templates select="." mode="text-labels">
                    <xsl:with-param name="text">corresp</xsl:with-param>
                </xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise></xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="author-notes" mode="author-notes-as-sections">
        <!-- apresenta todas as notas de autores -->
        <xsl:apply-templates select="*" mode="back-section"/>
    </xsl:template>

    <xsl:template match="back/fn | body/fn | back/fn-group" mode="back-section-content">
        <xsl:choose>
            <xsl:when test="@fn-type">
                <xsl:apply-templates select="." mode="back-section"/>
            </xsl:when>
            <xsl:when test="fn[@fn-type]">
                <xsl:apply-templates select="*" mode="back-section"/>
            </xsl:when>
            <xsl:when test="fn">
                <div class="ref-list">
                    <ul class="refList footnote">
                        <xsl:apply-templates select="fn" mode="div-fn-list-item"/>
                    </ul>
                </div>
            </xsl:when>
            <xsl:otherwise>
                <div class="ref-list">
                    <ul class="refList footnote">
                        <xsl:apply-templates select="." mode="div-fn-list-item"/>
                    </ul>
                </div>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="fn[@fn-type] | author-notes/*" mode="back-section-content">
        <xsl:apply-templates select="*[name()!='label']|text()"/>
    </xsl:template>

    <xsl:template match="* | fn[@fn-type or label]" mode="back-section-h">
        <h2 class="h5">
            <xsl:apply-templates select="." mode="back-section-title"/>
        </h2>
    </xsl:template>

    <xsl:template match="fn-group[not(label) and not(@fn-type)]" mode="back-section-menu">
        <!-- inibe a apresentação de opção do menu em branco -->
    </xsl:template>

    <xsl:template match="fn[@fn-type='other']" mode="back-section-menu">
        <!-- inibe a apresentação de opção do menu 'other' -->
    </xsl:template>

    <xsl:template match="fn[@fn-type='other']" mode="back-section-h">
        <!-- inibe a apresentação do título 'other' -->
    </xsl:template>

    <xsl:template match="fn[@fn-type='edited-by'] | fn[@fn-type='data-availability']" mode="back-section-menu">
        <!-- força a sobrescrita de v2.0 -->
        <xsl:variable name="name"><xsl:value-of select="@fn-type"/><xsl:value-of select="@sec-type"/></xsl:variable>
        <xsl:variable name="previous_name"><xsl:if test="preceding-sibling::node()"><xsl:value-of select="preceding-sibling::*[1]/@fn-type"/></xsl:if></xsl:variable>
        
        <xsl:variable name="title"><xsl:apply-templates select="." mode="back-section-title"/></xsl:variable>
        
        <!-- cria menu somente para o primeiro ref-list (há casos de série de ref-list) -->       
        <xsl:if test="$name='' or $previous_name!=$name and $name!='other'">
            <!-- manter pareado class="articleSection" e data-anchor="nome da seção no menu esquerdo" -->
            <xsl:attribute name="class">articleSection</xsl:attribute>
            <xsl:attribute name="data-anchor">
                <xsl:choose>
                    <xsl:when test="contains($title, ':')">
                        <xsl:value-of select="substring($title, 1, string-length($title)-1)"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="$title"/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:attribute>
        </xsl:if>
    </xsl:template>
</xsl:stylesheet>
