<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" 
    version="1.0">
    <xsl:template match="article" mode="article-meta-permissions">
        <xsl:choose>
            <xsl:when test="front/article-meta//license[@xml:lang=$TEXT_LANG]">
                <xsl:apply-templates select="front/article-meta//license[@xml:lang=$TEXT_LANG]"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test="front/article-meta//license[@xml:lang='en']">
                <xsl:apply-templates select="front/article-meta//license[@xml:lang='en']"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test="front/article-meta//license">
                <xsl:apply-templates select="front/article-meta//license[1]"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="front/article-meta//permissions"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>        
    </xsl:template>
    
    <xsl:template match="license">
        <xsl:variable name="url">https://licensebuttons.net/l/</xsl:variable>
        <xsl:variable name="path"><xsl:apply-templates select="." mode="license-acron-version"></xsl:apply-templates></xsl:variable>
        <xsl:variable name="icon"><xsl:value-of select="translate($path,'/',' ')"/></xsl:variable>
        
        <div class="col-sm-3 col-md-2">
            <a href="{@xlink:href}" target="_blank" title="">
                <img src="{$url}{$path}/88x31.png" alt="Creative Common - {$icon}"/>
            </a>
        </div>
        <div class="col-sm-9 col-md-10">
            <a href="{@xlink:href}" target="_blank" title="">
                <xsl:apply-templates select="license-p"/> 
            </a>
        </div>
    </xsl:template>
    
    <xsl:template match="permissions">
        <xsl:apply-templates select="copyright-statement"></xsl:apply-templates>
        <xsl:if test="not(copyright-statement)">
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="article" mode="article-meta-permissions-data-original-title">
        <xsl:variable name="path"><xsl:apply-templates select="." mode="license-acron-version"></xsl:apply-templates></xsl:variable>
        <xsl:variable name="icon"><xsl:value-of select="translate($path,'/',' ')"/></xsl:variable>
        <xsl:value-of select="$icon"/>
    </xsl:template>
    
    <xsl:template match="article" mode="license-acron-version">
        <xsl:if test=".//license[1]">
            <xsl:apply-templates select=".//license[1]" mode="license-acron-version"></xsl:apply-templates>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="license" mode="license-acron-version">
        <xsl:variable name="icon_path"><xsl:value-of select="substring-after(@xlink:href,'creativecommons.org/licenses/')"/></xsl:variable>
        <xsl:variable name="icon"><xsl:choose>
            <xsl:when test="contains($icon_path,'/legalcode')"><xsl:value-of select="substring-before($icon_path,'/legalcode')"/></xsl:when>
            <xsl:when test="contains($icon_path,'/deen')"><xsl:value-of select="substring-before($icon_path,'/deen')"/></xsl:when>
            <xsl:otherwise><xsl:value-of select="$icon_path"/></xsl:otherwise>
        </xsl:choose></xsl:variable><xsl:value-of select="$icon"/>
    </xsl:template>
    
</xsl:stylesheet>