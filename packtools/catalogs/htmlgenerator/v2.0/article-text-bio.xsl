<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="bio">
        <div style="background-color: #FCF5EA;">
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </div>
    </xsl:template>
    <xsl:template match="bio" mode="back-section">
        <xsl:param name="position"></xsl:param>
        <xsl:comment> mode="back-section" </xsl:comment>
        <xsl:comment> <xsl:value-of select="name()"/> </xsl:comment>
        <xsl:comment> <xsl:value-of select="$position"/> </xsl:comment>
        <xsl:if test="@id">
            <a name="{@id}"/>
        </xsl:if>
        
        <div class="articleSection"  style="background-color: #FCF5EA;">
            <xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="data-anchor"></xsl:apply-templates></xsl:attribute>
            <a name="articleSection{$body_index + $position}"></a>
            <div class="row">
                <div class="col-md-12 col-sm-12">
                    <h1><xsl:apply-templates select="." mode="title"/></h1>
                </div>
            </div>
            <xsl:apply-templates select="." mode="back-section-content"></xsl:apply-templates>
        </div>
    </xsl:template>
</xsl:stylesheet>