<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/article-text-back.xsl"/>

    <xsl:template match="*" mode="back-section-h">
        <xsl:if test="title or label">
            <h3 class="articleSectionTitle">
                <xsl:apply-templates select="label"/>
                <xsl:if test="label and title">&#160;</xsl:if>
                <xsl:apply-templates select="title"/>
            </h3>
        </xsl:if>
    </xsl:template>

</xsl:stylesheet>