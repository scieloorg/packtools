<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    
    <xsl:include href="verse-group.xsl"/>

    <xsl:template match="*" mode="node-name"><xsl:value-of select="name()"/></xsl:template>

    <xsl:template match="ref-list" mode="standard-title">
        <xsl:apply-templates select="." mode="text-labels">
            <xsl:with-param name="text">ref-list</xsl:with-param>
        </xsl:apply-templates>
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
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']/back" mode="back"/>
                <xsl:if test="not(.//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']/back)">
                    <xsl:apply-templates select="$article/back/ref-list" mode="back-section"/>
                </xsl:if>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="back" mode="back"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
   
    <xsl:template match="back" mode="back">
        <xsl:apply-templates select="*" mode="back-section"/>
    </xsl:template>
    
    <xsl:template match="sub-article[@article-type='translation']/back" mode="back">
        <xsl:choose>
            <xsl:when test="ref-list or not($article/back/ref-list)">
                <!-- apresenta os elementos de back -->
                <xsl:apply-templates select="*" mode="back-section"/>
            </xsl:when>
            <xsl:otherwise>
                <!-- apresenta os elementos de back -->
                <!-- como não existe sub-article/back/ref-list, apresenta ref-list de article/back/ref-list -->
                <xsl:apply-templates select="." mode="back-section-insert-article-reflist"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
   
    <xsl:template match="back" mode="back-section-insert-article-reflist">
        <!-- apresenta os elementos de back -->
        <!-- como não existe sub-article/back/ref-list, apresenta ref-list de article/back/ref-list -->
        <xsl:variable name="count"><xsl:value-of select="count($article/back/*)"/></xsl:variable>
        
        <xsl:choose>
            <xsl:when test="$article/back/*[position()=1 and name()='ref-list']">
                <!-- insere no início -->
                <xsl:apply-templates select="." mode="add-reflist-from-article-back"/>
                <xsl:apply-templates select="*" mode="back-section"/>
            </xsl:when>
            <xsl:when test="$article/back/*[position()=$count and name()='ref-list']">
                <!-- insere no final -->
                <xsl:apply-templates select="*" mode="back-section"/>
                <xsl:apply-templates select="." mode="add-reflist-from-article-back"/>
            </xsl:when>
            <xsl:otherwise>
                <!-- insere antes de fn / fn-group -->
                <xsl:apply-templates select="*[name()!='fn-group' and name()!='fn']" mode="back-section"/>
                <xsl:apply-templates select="." mode="add-reflist-from-article-back"/>
                <xsl:apply-templates select="*[name()='fn-group' or name()='fn']" mode="back-section"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="back" mode="add-reflist-from-article-back">
        <xsl:apply-templates select="$article/back/ref-list" mode="back-section"/>
    </xsl:template>

    <xsl:template match="*" mode="back-section-menu">
        <xsl:if test="title or label">
            <!-- manter pareado class="articleSection" e data-anchor="nome da seção no menu esquerdo" -->
            <xsl:attribute name="class">articleSection</xsl:attribute>
            <xsl:attribute name="data-anchor">
                <xsl:apply-templates select="label"/>
                <xsl:if test="label and title">&#160;</xsl:if>
                <xsl:apply-templates select="title"/>
            </xsl:attribute>
        </xsl:if>
    </xsl:template>

    <xsl:template match="ref-list" mode="back-section-menu">
        <xsl:variable name="name" select="name()"/>
        <!-- cria menu somente para o primeiro ref-list (há casos de série de ref-list) -->
        <xsl:if test="not(preceding-sibling::node()) or preceding-sibling::*[1][name()!=$name]">
            <!-- manter pareado class="articleSection" e data-anchor="nome da seção no menu esquerdo" -->
            <xsl:attribute name="class">articleSection</xsl:attribute>
            <xsl:attribute name="data-anchor">
                <xsl:apply-templates select="." mode="text-labels">
                    <xsl:with-param name="text">ref-list</xsl:with-param>
                </xsl:apply-templates>
            </xsl:attribute>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="*" mode="back-section-h">
        <xsl:if test="title or label">
            <h1 class="articleSectionTitle">
                <xsl:apply-templates select="label"/>
                <xsl:if test="label and title">&#160;</xsl:if>
                <xsl:apply-templates select="title"/>
            </h1>
        </xsl:if>
    </xsl:template>
        
    <xsl:template match="*" mode="back-section">
        <xsl:apply-templates select="@id" mode="add_span_id"/>
        <div>
            <xsl:apply-templates select="." mode="back-section-menu"/>
            <xsl:apply-templates select="." mode="back-section-h"/>
            <xsl:apply-templates select="." mode="back-section-content"/>
        </div>
    </xsl:template>

    <xsl:template match="app-group" mode="back-section">
        <xsl:apply-templates select="app" mode="back-section"/>
    </xsl:template>
    
    <xsl:template match="*" mode="back-section-content">
        <xsl:apply-templates select="*[name()!='title' and name()!='label'] | text()"/>
    </xsl:template>

</xsl:stylesheet>
