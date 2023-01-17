<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    
    <xsl:include href="../v2.0/article-text-fn.xsl"/>

    <xsl:template match="fn[@fn-type='edited-by'] | fn[@fn-type='data-availability']" mode="open-science-notes">
        <xsl:variable name="title"><xsl:apply-templates select="label"/><xsl:if test="not(label)"><xsl:apply-templates select="." mode="text-labels">
                 <xsl:with-param name="text"><xsl:value-of select="@fn-type"/></xsl:with-param>
             </xsl:apply-templates></xsl:if></xsl:variable>
        <div>
            <xsl:attribute name="class">articleSection</xsl:attribute>
            <xsl:attribute name="data-anchor"><xsl:value-of select="translate($title, ':', '')"/></xsl:attribute>
            <h3><xsl:value-of select="translate($title, ':', '')"/></h3>
            <xsl:apply-templates select="." mode="a_name"/>
            <xsl:apply-templates select="*[name()!='label']|text()"/>
            <xsl:apply-templates select="." mode="xref_href"/>
        </div>
    </xsl:template>

    <xsl:template match="fn" mode="a_name">
        <xsl:if test="@id">
            <a name="refId_{@id}"/>
        </xsl:if>
    </xsl:template>

    <xsl:template match="fn" mode="xref_href">
        <xsl:variable name="id"><xsl:value-of select="@id"/></xsl:variable>
        <xsl:if test="$id != '' and $article//xref[@rid=$id]">
            <a href="#{@id}_ref">↩</a>
        </xsl:if>
    </xsl:template>

    <xsl:template match="fn[@id] | author-notes/*[@id]">
        <xsl:variable name="id"><xsl:value-of select="@id"/></xsl:variable>
        
        <div class="articleSection articleReferenceFootNotes" data-anchor="NotasRodape">
            <hr/>
            <div class="row">
                <div class="col-md-12 col-sm-12">
                    <ol class="articleFootnotes">
                        <li>
                            <a class="" name="{@id}_ref"></a>
                            <xsl:apply-templates select="*|text()"/>
                            <xsl:if test="$id != '' and $article//xref[@rid=$id]">
                                <a href="#{@id}_ref">↩</a>
                            </xsl:if>
                        </li>
                    </ol>
                </div>
            </div>
        </div>
    </xsl:template>
</xsl:stylesheet>
