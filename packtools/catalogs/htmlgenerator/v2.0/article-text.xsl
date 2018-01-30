<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink" >
                
    <xsl:template match="*" mode="text-body">
        
        <xsl:variable name="alttile">
            <xsl:choose>
                <xsl:when test=".//sub-article[@article-type!='translation'] or .//response">
                    <xsl:apply-templates select="." mode="text-labels">
                        <xsl:with-param name="text"><xsl:value-of select="@article-type"/><xsl:value-of select="@response-type"/></xsl:with-param>
                    </xsl:apply-templates>
                </xsl:when>
                <xsl:otherwise>Text</xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']">
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//body">
                    <xsl:with-param name="alt_title" select="$alttile"></xsl:with-param>
                </xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="./body">
                    <xsl:with-param name="alt_title" select="$alttile"></xsl:with-param></xsl:apply-templates>                    
            </xsl:otherwise>
        </xsl:choose>            
    </xsl:template>
    
    <xsl:template match="body">
        <xsl:param name="alt_title"></xsl:param>
        <div>
            <xsl:if test="$alt_title!=''">
                <xsl:attribute name="class">articleSection</xsl:attribute>
                <xsl:attribute name="data-anchor"><xsl:value-of select="$alt_title"></xsl:value-of></xsl:attribute>
                
            </xsl:if>
            <xsl:apply-templates select="*"/>
        </div>
    </xsl:template>
    
    <xsl:template match="body/p">
        <p></p>
        <xsl:choose>
            <xsl:when test="p">
                <div>
                    <xsl:apply-templates select="*|text()"></xsl:apply-templates>
                </div>
            </xsl:when>
            <xsl:otherwise>
                <p>
                    <xsl:apply-templates select="*|text()"></xsl:apply-templates>
                </p>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="body/sec/title">
        <h1 class="articleSectionTitle">
            <xsl:apply-templates select="*|text()"/>
        </h1>
    </xsl:template>
    
    <xsl:template match="sec/sec/title">
        <h2>
            <xsl:apply-templates select="*|text()"/>
        </h2>
    </xsl:template>
    
    <xsl:template match="sec/sec/sec/title">
        <h3>
            <xsl:apply-templates select="*|text()"/>
        </h3>
    </xsl:template>
             
    <xsl:template match="sig-block">
        <p class="articleSignature">
            <xsl:apply-templates select="*"></xsl:apply-templates>
        </p>
    </xsl:template>
    
    <xsl:template match="sig">
        <xsl:choose>
            <xsl:when test="position()=1">
                <xsl:apply-templates></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <small><xsl:apply-templates select="*|text()"/></small>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="speech/speaker">
        <div class="row"><strong><xsl:apply-templates select="*|text()"></xsl:apply-templates></strong></div>
    </xsl:template>

    <xsl:template match="speech/p">
        <div class="row"><xsl:apply-templates select="*|text()"></xsl:apply-templates></div>
    </xsl:template>
</xsl:stylesheet>