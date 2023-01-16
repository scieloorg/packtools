<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    
    <xsl:template match="fn/p">
        <div>
            <xsl:apply-templates select=".." mode="a_name"/>
            <xsl:apply-templates select="*|text()" mode="fn-texts"/>
            <xsl:apply-templates select=".." mode="xref_href"/>
        </div>
    </xsl:template>

    <xsl:template match="fn[@fn-type='edited-by'] | fn[@fn-type='data-availability']" mode="open-science-notes">
        <xsl:variable name="title"><xsl:apply-templates select="label"/><xsl:if test="not(label)"><xsl:apply-templates select="." mode="text-labels">
                 <xsl:with-param name="text"><xsl:value-of select="@fn-type"/></xsl:with-param>
             </xsl:apply-templates></xsl:if></xsl:variable>
        <div>
            <xsl:attribute name="class">articleSection</xsl:attribute>
            <xsl:attribute name="data-anchor"><xsl:value-of select="translate($title, ':', '')"/></xsl:attribute>
            <h3><xsl:value-of select="translate($title, ':', '')"/></h3>
            <xsl:apply-templates select="." mode="a_name"/>
            <xsl:apply-templates select="*[name()!='label']|text()" mode="fn-texts"/>
            <xsl:apply-templates select="." mode="xref_href"/>
        </div>
    </xsl:template>

    <xsl:template match="fn" mode="a_name">
        <a name="fn_{@id}"/>
    </xsl:template>

    <xsl:template match="fn" mode="xref_href">
        <xsl:variable name="id" select="@id"/>
        <xsl:if test="$article//xref[@rid=$id]">
            <a href="#xref_{@id}">↩</a>
        </xsl:if>
    </xsl:template>

</xsl:stylesheet>
