<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">

    <xsl:template match="article" mode="article-text-sub-articles">
        <xsl:apply-templates select="response[@xml:lang=$TEXT_LANG] | sub-article[@xml:lang=$TEXT_LANG and @article-type!='translation']"></xsl:apply-templates>
    </xsl:template>

    <!--xsl:template match="front-stub/aff | article/*/front/aff |front-stub/history | article/*/front/history ">        
    </xsl:template>
    
    <xsl:template match="front-stub//subject | article/*/front//subject">
     </xsl:template>
    <xsl:template match="front-stub//article-title | article/*/front//article-title">
        <h2>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </h2>
    </xsl:template>
    <xsl:template match="front-stub//trans-title | article/*/front//trans-title">
        <h3>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </h3>
    </xsl:template-->
    
    <xsl:template match="sub-article[@article-type!='translation'] | response">
        <div class="articleSection">
            <xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="text-labels">
                <xsl:with-param name="text" select="concat(@article-type,@response-type)"/>
            </xsl:apply-templates></xsl:attribute>
            <a name="articleSection{$q_front + $q_back + $q_body_fn + 1 + position()}"/>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>      
        </div>
        <xsl:apply-templates select="front-stub | front" mode="generic-history"></xsl:apply-templates>
    </xsl:template>

</xsl:stylesheet>