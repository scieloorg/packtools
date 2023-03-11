<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    
    <xsl:template match="*" mode="node-name"><xsl:value-of select="name()"/></xsl:template>

    <xsl:template match="ref-list" mode="force-title">
        <xsl:choose>
            <xsl:when test="$article/@xml:lang=$TEXT_LANG and title">
                <xsl:apply-templates select="title"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="." mode="text-labels">
                    <xsl:with-param name="text">ref-list</xsl:with-param>
                </xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="back/*" mode="real-title">
        <!-- 
        Apresentar o título de seção tal como está no XML.
        Não forçar tradução do título,o que ocorria em sub-article do tipo
        translation
        Não criar título a partir do nome da tag ref-list
        -->
        <xsl:apply-templates select="label"/>
        <xsl:if test="label and title">&#160;</xsl:if>
        <xsl:apply-templates select="title"/>
    </xsl:template>
    
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
    
    <xsl:template match="*" mode="menu-section">
        <!-- nao apresenta no menu -->
    </xsl:template>
    
    <xsl:template match="ref-list" mode="menu-section">
        <xsl:variable name="name" select="name()"/>
        <xsl:if test="not(preceding-sibling::node()) or preceding-sibling::node()[name()!=$name]">
            <xsl:attribute name="class">articleSection</xsl:attribute>
            <xsl:attribute name="data-anchor">
                <xsl:apply-templates select="." mode="text-labels">
                    <xsl:with-param name="text">ref-list</xsl:with-param>
                </xsl:apply-templates>
            </xsl:attribute>
            <h1 style="visibility:hidden">
                <xsl:attribute name="class">articleSectionTitle</xsl:attribute>
                <xsl:apply-templates select="." mode="text-labels">
                    <xsl:with-param name="text">ref-list</xsl:with-param>
                </xsl:apply-templates>
            </h1>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="*" mode="back-section-h1">
        <h1>
            <xsl:if test="label or title">
                <xsl:attribute name="class">articleSectionTitle</xsl:attribute>
                <xsl:apply-templates select="." mode="real-title"/>
            </xsl:if>
        </h1>
    </xsl:template>
    
    <xsl:template match="*" mode="back-section">
        <div>
            <xsl:apply-templates select="." mode="menu-section"/>
            <xsl:apply-templates select="." mode="back-section-h1"/>
            <xsl:apply-templates select="." mode="back-section-content"/>
        </div>
    </xsl:template>
    
    <xsl:template match="app-group" mode="back-section">
        <xsl:apply-templates select="app" mode="back-section"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="*" mode="back-section-content">
        <xsl:apply-templates select="*[name()!='title' and name()!='label'] | text()"></xsl:apply-templates>
    </xsl:template>
    
</xsl:stylesheet>
