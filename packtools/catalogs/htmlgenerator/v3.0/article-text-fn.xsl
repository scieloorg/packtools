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

    <xsl:template match="body//fn | back/fn | author-notes/fn | back/fn-group" mode="back-section-content">
        <div class="row">
            <div class="col">
                <ul class="refList articleFootnotes">
                    <xsl:apply-templates select="fn" mode="div-fn-list-item"/>
                    <xsl:if test="not(fn)">
                        <xsl:apply-templates select="." mode="div-fn-list-item"/>
                    </xsl:if>
                </ul>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="fn[@fn-type='edited-by'] | fn[ @fn-type='data-availability']" mode="back-section-h">
        <!--
            Apresenta o título da seção no texto completo
        -->
        <xsl:variable name="name" select="@fn-type"/>
        <xsl:if test="not(preceding-sibling::node()) or preceding-sibling::*[1][not(@fn-type)] or preceding-sibling::*[1][@fn-type!=$name]">
            <h2 class="h5">
                <xsl:apply-templates select="." mode="text-labels">
                    <xsl:with-param name="text"><xsl:value-of select="@fn-type"/></xsl:with-param>
                </xsl:apply-templates>
            </h2>
        </xsl:if>
    </xsl:template>

</xsl:stylesheet>
