<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">

    <xsl:template match="ref-list">
        <div class="articleSection" data-anchor="Referências">
            <a name="articleSection3"></a>
            <div class="row">
                <div class="col-md-12 col-sm-12">
                    <h1>References</h1>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12 col-sm-12 ref-list">
                       <xsl:apply-templates select="ref"></xsl:apply-templates>
                </div>
            </div></div>
    </xsl:template>
    
    <xsl:template match="ref">
            <div>
                <xsl:apply-templates select="mixed-citation"></xsl:apply-templates>
            </div>
    </xsl:template>
    
    <xsl:template match="ref/label">
        <sup class="xref big"><xsl:value-of select="."/></sup>
    </xsl:template>
    
    <xsl:template match="person-group">
        <xsl:apply-templates select="name"></xsl:apply-templates><xsl:choose>
            <xsl:when test="position()=last()">. </xsl:when>
            <xsl:otherwise>; </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template match="person-group/name">
        <xsl:apply-templates select="surname"></xsl:apply-templates>, <xsl:apply-templates select="given-names"></xsl:apply-templates>
    </xsl:template>
</xsl:stylesheet>