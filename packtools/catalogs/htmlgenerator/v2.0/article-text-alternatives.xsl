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
            <xsl:when test="graphic[@specific-use='scielo-web' and not(starts-with(@content-type, 'scielo-'))]">
                <xsl:apply-templates select="graphic[@specific-use='scielo-web' and not(starts-with(@content-type, 'scielo-'))]" />
            </xsl:when>
            <xsl:when test=".//graphic[not(@specific-use) and not(@content-type) and @xlink:href!='']">
                <xsl:apply-templates select=".//graphic[not(@specific-use) and not(@content-type) and @xlink:href!=''][1]" />
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

            <xsl:when test="graphic[@specific-use='scielo-web' and starts-with(@content-type, 'scielo-')]">
                <xsl:apply-templates select="graphic[@specific-use='scielo-web' and starts-with(@content-type, 'scielo-')]" mode="file-location" />
            </xsl:when>

            <xsl:when test="graphic[not(@specific-use) and not(@content-type)]">
                <xsl:apply-templates select="graphic[not(@specific-use) and not(@content-type)]" mode="file-location" />
            </xsl:when>

            <xsl:otherwise>
                <xsl:apply-templates select="*[name()!='graphic'][1]" mode="file-location"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="alternatives" mode="file-location-thumb">
        <xsl:choose>

            <xsl:when test="inline-graphic[@xlink:href!='' and @specific-use='scielo-web']">
                <xsl:apply-templates select="inline-graphic[@xlink:href!='' and @specific-use='scielo-web']" mode="file-location-thumb"/>
            </xsl:when>
            <xsl:when test="inline-graphic[@xlink:href!='' and not(@specific-use='scielo-web')]">
                <xsl:apply-templates select="inline-graphic[@xlink:href!='' and not(@specific-use='scielo-web')]" mode="file-location-thumb"/>
            </xsl:when>

            <xsl:when test="graphic[@xlink:href!='' and @specific-use='scielo-web' and starts-with(@content-type, 'scielo-')]">
                <xsl:apply-templates select="graphic[@xlink:href!='' and @specific-use='scielo-web' and starts-with(@content-type, 'scielo-')]" mode="file-location-thumb" />
            </xsl:when>
            <xsl:when test="graphic[@xlink:href!='' and @specific-use='scielo-web' and not(starts-with(@content-type, 'scielo-'))]">
                <xsl:apply-templates select="graphic[@xlink:href!='' and @specific-use='scielo-web' and not(starts-with(@content-type, 'scielo-'))]" mode="file-location-thumb" />
            </xsl:when>
            <xsl:when test=".//graphic[@xlink:href!='']">
                <xsl:apply-templates select=".//graphic[@xlink:href!=''][1]" mode="file-location-thumb" />
            </xsl:when>

            <xsl:otherwise>
                <xsl:apply-templates select="*[name()!='graphic'][1]" mode="file-location-thumb"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

</xsl:stylesheet>