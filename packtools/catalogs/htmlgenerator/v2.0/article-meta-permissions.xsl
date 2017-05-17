<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" 
    version="1.0">
    <xsl:template match="article" mode="article-meta-permissions">
        <xsl:choose>
            <xsl:when test=".//article-meta//license[@xml:lang=$TEXT_LANG]">
                <xsl:apply-templates select=".//article-meta//license[@xml:lang=$TEXT_LANG]"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test=".//article-meta//license[@xml:lang='en']">
                <xsl:apply-templates select=".//article-meta//license[@xml:lang='en']"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test=".//article-meta//license">
                <xsl:apply-templates select=".//article-meta//license[1]"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select=".//article-meta//permissions"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>        
    </xsl:template>
    
    <xsl:template match="license">
        <xsl:variable name="url">https://licensebuttons.net/l/</xsl:variable>
        <xsl:variable name="icon_path"><xsl:value-of select="substring-after(@xlink:href,'creativecommons.org/licenses/')"/></xsl:variable>
        <xsl:variable name="icon"><xsl:choose>
            <xsl:when test="contains($icon_path,'/deen')"><xsl:value-of select="substring-before($icon_path,'/deen')"/></xsl:when>
            <xsl:otherwise><xsl:value-of select="$icon_path"/></xsl:otherwise>
        </xsl:choose></xsl:variable>
        • <a href="{@xlink:href}" target="_blank"><img src="{$url}{$icon}/80x15.png" alt="Creative Common - {$icon}"/> </a>
    </xsl:template>
    
    <xsl:template match="permissions">
        • <xsl:apply-templates select="copyright-statement"></xsl:apply-templates>
        <xsl:if test="not(copyright-statement)">
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </xsl:if>
    </xsl:template>
</xsl:stylesheet>