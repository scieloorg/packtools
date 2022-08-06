<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    
    <xsl:template match="*" mode="node-name"><xsl:value-of select="name()"/></xsl:template>

    <xsl:template match="article" mode="text-back">
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']">
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']/back/*" mode="back"/>
                <xsl:if test="count(.//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']/back/*) &lt; $REFLIST_POSITION">
                    <!--
                    <xsl:comment> ref-list inserted </xsl:comment>
                    -->
                    <xsl:apply-templates select="$article/back/ref-list" mode="back-section"/>
                </xsl:if>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="./back/*" mode="back"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>        
    </xsl:template>
    
   
    <xsl:template match="*" mode="back">
        <!--
        <xsl:comment> <xsl:value-of select="name()"/>, mode="back" </xsl:comment>
        <xsl:comment> position()=<xsl:value-of select="position()"/> </xsl:comment>
        <xsl:comment> $REFLIST_POSITION=<xsl:value-of select="$REFLIST_POSITION"/> </xsl:comment>
        <xsl:comment> $REFLIST_INDEX=<xsl:value-of select="$REFLIST_INDEX"/> </xsl:comment>
        -->
        <xsl:apply-templates select="." mode="back-section"/>
    </xsl:template>
    
    <xsl:template match="sub-article[@article-type='translation']/back[not(ref-list)]/*" mode="back">
        <!--
        <xsl:comment> sub-article/<xsl:value-of select="name()"/>, mode="back" </xsl:comment>
        <xsl:comment> position()=<xsl:value-of select="position()"/> </xsl:comment>
        <xsl:comment> $REFLIST_POSITION=<xsl:value-of select="$REFLIST_POSITION"/> </xsl:comment>
        <xsl:comment> $REFLIST_INDEX=<xsl:value-of select="$REFLIST_INDEX"/> </xsl:comment>
        -->
        
        <xsl:if test="position()=$REFLIST_POSITION">
            <!--
            <xsl:comment> ref-list inserted </xsl:comment>
            -->
            <xsl:apply-templates select="$article/back/ref-list" mode="back-section"/>
        </xsl:if>
         <xsl:apply-templates select="." mode="back-section"/>
    </xsl:template>
    
    <xsl:template match="*" mode="back-section">
        <div>
            <xsl:if test="label or title">
                <xsl:attribute name="class">articleSection</xsl:attribute>
                <xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="title"></xsl:apply-templates></xsl:attribute>    
            </xsl:if>
            <h1>
                <xsl:if test="label or title">
                    <xsl:attribute name="class">articleSectionTitle</xsl:attribute>
                    <xsl:apply-templates select="." mode="title"></xsl:apply-templates>    
                </xsl:if>
            </h1>
            <xsl:apply-templates select="." mode="back-section-content"></xsl:apply-templates>
        </div>
    </xsl:template>
    
    <xsl:template match="app-group" mode="back-section">
        <xsl:apply-templates select="app" mode="back-section"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="*" mode="back-section-content">
        <xsl:apply-templates select="*[name()!='title' and name()!='label'] | text()"></xsl:apply-templates>
    </xsl:template>
    
</xsl:stylesheet>
