<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/article-text-back.xsl"/>

    <xsl:template match="*" mode="back-section">
        <div>
            <xsl:if test="label or title">
                <xsl:attribute name="class">articleSection</xsl:attribute>
                <xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="title"></xsl:apply-templates></xsl:attribute>    
            </xsl:if>
            <h3>
                <xsl:if test="label or title">
                    <xsl:attribute name="class">articleSectionTitle</xsl:attribute>
                    <xsl:apply-templates select="." mode="title"></xsl:apply-templates>    
                </xsl:if>
            </h3>
            <xsl:apply-templates select="." mode="back-section-content"></xsl:apply-templates>
        </div>
    </xsl:template>
</xsl:stylesheet>