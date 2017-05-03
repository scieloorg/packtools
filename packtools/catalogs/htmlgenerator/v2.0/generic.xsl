<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:mml="http://www.w3.org/1998/Math/MathML"
  exclude-result-prefixes="xlink mml">

    <xsl:template match="*">
        <xsl:comment> * <xsl:value-of select="name()"/> </xsl:comment>
        <xsl:apply-templates select="*|text()"/>
    </xsl:template>
    
    <xsl:template match="text()">
        <xsl:value-of select="."/>
    </xsl:template>
    
    <xsl:template match="@*">
        <xsl:attribute name="{name()}"><xsl:value-of select="."/></xsl:attribute>
    </xsl:template>
    
    <xsl:template match="p | sub | sup">
        <xsl:param name="position"></xsl:param>
        <xsl:element name="{name()}">
            <xsl:apply-templates select="*|text()">
                <xsl:with-param name="position" select="position()"></xsl:with-param>
            </xsl:apply-templates>
        </xsl:element>
    </xsl:template>
    
    <xsl:template match="p[.//p]">
        <div>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </div>
    </xsl:template>
    
    <xsl:template match="bold">
        <b><xsl:apply-templates></xsl:apply-templates></b>
    </xsl:template>
    
    <xsl:template match="italic">
        <i><xsl:apply-templates></xsl:apply-templates></i>
    </xsl:template>
    
    <xsl:template match="break">
        <br/>
    </xsl:template>
    
    
    <xsl:template match="ext-link">
        <xsl:choose>
            <xsl:when test="@xlink:href">
                <a href="{@xlink:href}" target="_blank"><xsl:apply-templates select="*|text()"></xsl:apply-templates></a>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="*|text()"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="email">
        <a href="mailto:{.}"><xsl:value-of select="."/></a>
    </xsl:template>
    
    <xsl:template match="disp-quote">
        <div>
            <blockquote>
                <xsl:apply-templates select="*|text()"></xsl:apply-templates>
            </blockquote>
        </div>
    </xsl:template>
    
    <xsl:template match="source | article-title | chapter-title">
        <cite><xsl:apply-templates select="*|text()"></xsl:apply-templates></cite>
    </xsl:template>
    
    <xsl:template match="def-list">
        <dl>
            <xsl:apply-templates select="*"></xsl:apply-templates>
        </dl>
    </xsl:template>
    
    <xsl:template match="term">
        <dt>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </dt>
    </xsl:template>
    
    <xsl:template match="def">
        <dd> 
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </dd>
    </xsl:template>
</xsl:stylesheet>
