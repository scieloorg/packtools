<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="issn">
        <div>
            <span><xsl:apply-templates select="@pub-type"></xsl:apply-templates> <xsl:value-of select="."/></span>
        </div>
    </xsl:template>
     
    <xsl:template match="article" mode="journal-meta-issn">
        <div class="col-md-4 col-sm-6 right">
            <xsl:apply-templates select=".//journal-meta//issn"></xsl:apply-templates>
        </div>
    </xsl:template>
    <xsl:template match="article" mode="journal-meta-bibstrip-title">
        <xsl:apply-templates select=".//journal-meta//abbrev-journal-title"></xsl:apply-templates>
    </xsl:template>
    <xsl:template match="article" mode="journal-meta-bibstrip-issue">
        <xsl:if test=".//article-meta">
            <xsl:if test=".//article-meta/volume!='00'">
                <xsl:apply-templates select=".//article-meta/volume"/>
            </xsl:if><xsl:text> </xsl:text>
            <xsl:if test=".//article-meta/issue!='00'">
                (<xsl:apply-templates select=".//article-meta/issue"/>)
            </xsl:if>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="article" mode="journal-meta-pub-dates">
        <xsl:apply-templates  select=".//article-meta/pub-date" mode="journal-meta-pub-dates"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="article-meta/pub-date" mode="journal-meta-pub-dates">
        <xsl:if test="@pub-type='epub'">Epub </xsl:if>
        <xsl:choose>
            <xsl:when test="season">
                <xsl:apply-templates select="season"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test="day">
                <xsl:apply-templates select="month"></xsl:apply-templates>
                <xsl:text> </xsl:text>
                <xsl:apply-templates select="day"></xsl:apply-templates>, 
            </xsl:when>
            <xsl:otherwise><xsl:apply-templates select="month" mode="lang-month"></xsl:apply-templates></xsl:otherwise>
        </xsl:choose>
        <xsl:text> </xsl:text>
        <xsl:apply-templates select="year"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="article" mode="journal-meta-bibstrip">
        <div class="row editionMeta">
            <div class="col-md-8 col-sm-6">
                <span><xsl:apply-templates select="." mode="journal-meta-bibstrip-title"></xsl:apply-templates>
                    <xsl:text> </xsl:text>
                    <xsl:apply-templates select="." mode="journal-meta-bibstrip-issue"></xsl:apply-templates>
                    <!-- FIXME location --> 
                    <xsl:apply-templates select="." mode="journal-meta-pub-dates"></xsl:apply-templates></span>
            </div>
            <xsl:apply-templates select="." mode="journal-meta-issn"></xsl:apply-templates>
        </div>
    </xsl:template>
    
    
</xsl:stylesheet>