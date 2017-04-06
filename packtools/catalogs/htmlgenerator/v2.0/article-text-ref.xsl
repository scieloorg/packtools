<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    
    <xsl:template match="ref">
        <xsl:comment>  <xsl:apply-templates select="mixed-citation"/> </xsl:comment>
        <li>
            <xsl:if test="label">
                <xsl:apply-templates select="label"></xsl:apply-templates>
            </xsl:if>
            
            <div>
                <xsl:choose>
                    <xsl:when test="mixed-citation[*]">
                        <xsl:apply-templates select="mixed-citation"/>
                    </xsl:when>
                    <xsl:otherwise><xsl:apply-templates select="mixed-citation"/></xsl:otherwise>
                </xsl:choose>
            </div>
        </li>
    </xsl:template>
    
    <xsl:template match="mixed-citation[*]/text() | mixed-citation[not(*)]/text()">
        <xsl:if test="position()=1"><xsl:comment> <xsl:value-of select="."/> </xsl:comment></xsl:if>
        <xsl:variable name="label">
            <xsl:if test="position()=1">
                <xsl:choose>
                    <xsl:when test="starts-with(.,concat(../../label,'.'))">
                        <xsl:value-of select="concat(../../label,'.')"/>
                    </xsl:when>
                    <xsl:when test="starts-with(.,concat(../../label,' .'))">
                        <xsl:value-of select="concat(../../label,' .')"/>
                    </xsl:when>
                    <xsl:when test="starts-with(.,../../label)">
                        <xsl:value-of select="../../label"/>
                    </xsl:when>
                </xsl:choose>
            </xsl:if>
        </xsl:variable>
        <xsl:choose>
            <xsl:when test="normalize-space($label)!=''"><xsl:value-of select="substring-after(.,$label)"/></xsl:when>
            <xsl:when test="starts-with(.,'.')"><xsl:value-of select="substring-after(.,'.')"/></xsl:when>
            <xsl:otherwise><xsl:value-of select="."/></xsl:otherwise>
        </xsl:choose> 
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
    
    <xsl:template match="ref" mode="url">
        <xsl:choose>
            <xsl:when test=".//ext-link"><xsl:value-of select=".//ext-link[1]"/></xsl:when>
            <xsl:when test=".//pub-id[@pub-id-type='doi']">https://doi.org/<xsl:value-of select=".//pub-id[@pub-id-type='doi']"/></xsl:when>
            <xsl:when test=".//comment[starts-with(.,'http')]"><xsl:value-of select=".//comment[starts-with(.,'http')]"/></xsl:when>
            <xsl:when test=".//comment[contains(.,'doi:')]">https://doi.org/<xsl:value-of select="normalize-space(substring-after(.//comment[contains(.,'doi:')],'doi:'))"/></xsl:when>
            <xsl:when test=".//comment[contains(.,'DOI:')]">https://doi.org/<xsl:value-of select="normalize-space(substring-after(.//comment[contains(.,'DOI:')],'DOI:'))"/></xsl:when>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="ref" mode="xref">
        <xsl:variable name="url"><xsl:apply-templates select="." mode="url"></xsl:apply-templates></xsl:variable>
        <xsl:choose>
            <xsl:when test="$url!=''">
                <a href="{$url}" target="_blank">
                    <xsl:apply-templates select="mixed-citation"></xsl:apply-templates>
                </a>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="mixed-citation"></xsl:apply-templates></xsl:otherwise>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>