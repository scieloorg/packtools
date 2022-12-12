<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    
    <xsl:template match="article" mode="journal-meta-bibstrip-title">
        <xsl:choose>
            <xsl:when test="$ARTICLE_BIBSTRIP!=''">
                <xsl:value-of select="$ARTICLE_BIBSTRIP"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="front/journal-meta//abbrev-journal-title"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="article" mode="journal-meta-bibstrip-issue">
        <xsl:if test="front/article-meta">
            <xsl:if test="front/article-meta/volume!='00'">
                <xsl:apply-templates select="front/article-meta/volume"/>
            </xsl:if><xsl:text> </xsl:text>
            <xsl:if test="front/article-meta/issue!='00'">
                (<xsl:apply-templates select="front/article-meta/issue"/>)
            </xsl:if>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="article" mode="journal-meta-issn">
        <xsl:apply-templates select="front/article-meta//issn">
            <xsl:sort select="@pub-type"/>
        </xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="issn">
        <span>ISSN&#160;<xsl:value-of select="."/>&#160;(<xsl:apply-templates select="@pub-type" mode="generated-label"/>)</span>&#160;
    </xsl:template>
    
</xsl:stylesheet>