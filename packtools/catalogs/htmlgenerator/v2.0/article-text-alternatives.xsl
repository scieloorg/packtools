<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml"
    version="1.0">
    
    <xsl:template match="alternatives">
        <xsl:choose>
            <xsl:when test="inline-graphic[@specific-use='scielo-web']">
                <xsl:apply-templates select="inline-graphic[@specific-use='scielo-web']" />
            </xsl:when>
            <xsl:when test="graphic[@specific-use='scielo-web']">
                <xsl:apply-templates select="graphic[@specific-use='scielo-web' and not(starts-with(@content-type, 'scielo-'))]" />
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="*[name()!='graphic'][1]"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="alternatives" mode="file-location">
        <xsl:choose>
            <xsl:when test="inline-graphic[@specific-use='scielo-web']">
                <xsl:apply-templates select="inline-graphic[@specific-use='scielo-web']" mode="file-location"/>
            </xsl:when>
            <xsl:when test="graphic[@specific-use='scielo-web']">
                <xsl:apply-templates select="graphic[@specific-use='scielo-web' and not(starts-with(@content-type, 'scielo-'))]" mode="file-location" />
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="*[name()!='graphic'][1]" mode="file-location"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
   
</xsl:stylesheet>