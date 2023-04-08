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

    <xsl:template match="fn[@fn-type='edited-by']/label | fn[@fn-type='data-availability']/label | fn[@fn-type='edited-by']/title | fn[@fn-type='data-availability']/title" mode="div-fn-list-item">
        <!-- do nothing for fn edited-by or data-availability -->
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

</xsl:stylesheet>
