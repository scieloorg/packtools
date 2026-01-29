<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/article-text.xsl"/>

    <xsl:template match="body/sec/title">
        <h2 class="h5">
            <xsl:apply-templates select="*|text()"/>
        </h2>
    </xsl:template>
    
    <xsl:template match="sec/sec/title">
        <h3 class="h5">
            <xsl:apply-templates select="*|text()"/>
        </h3>
    </xsl:template>
    
    <xsl:template match="sec/sec/sec/title">
        <h5>
            <xsl:apply-templates select="*|text()"/>
        </h5>
    </xsl:template>
</xsl:stylesheet>