<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">

    <xsl:template match="article" mode="article-meta-abstract">
        <!-- apresenta todos os resumos que existir -->
        <xsl:variable name="q" select="count(.//abstract[.//text()])+count(.//trans-abstract[.//text()])"/>
        <xsl:if test="$q &gt; 0">
            <!-- apresenta a âncora e o título, ou seja, Abstract, Resumo, ou Resumen -->
            <xsl:apply-templates select="." mode="create-anchor-and-title-for-abstracts-without-title"/>

            <!-- apresenta os resumos diferentes de key-points -->
            <xsl:apply-templates select="." mode="standard-abstract"/>
        </xsl:if>

        <!-- graphical -->
        <xsl:choose>
            <xsl:when
                test="sub-article//abstract[@abstract-type='graphical']">
                <xsl:apply-templates
                    select="sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]" mode="graphical-abstract"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="front/article-meta" mode="graphical-abstract"/>
            </xsl:otherwise>
        </xsl:choose>

        <!-- key-points -->
        <xsl:choose>
            <xsl:when
                test="sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]">
                <xsl:apply-templates
                    select="sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]" mode="key-points-block"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="front/article-meta" mode="key-points-block"/>
            </xsl:otherwise>
        </xsl:choose>
        
    </xsl:template>

    <xsl:template match="article | sub-article" mode="key-points-block">
        <xsl:apply-templates select="front/article-meta | front-stub" mode="key-points-block"/>
    </xsl:template>

    <xsl:template match="front/article-meta | front-stub" mode="key-points-block">
        <!-- apresenta os resumos do tipo key-points (highlights) -->
        <xsl:apply-templates select=".//abstract[@abstract-type='key-points']" mode="layout"/>
        <xsl:apply-templates select=".//trans-abstract[@abstract-type='key-points']" mode="layout"/>
        <!-- apresenta os resumos do tipo highlights (highlights) -->
        <xsl:apply-templates select=".//abstract[.//list]" mode="layout"/>
        <xsl:apply-templates select=".//trans-abstract[.//list]" mode="layout"/>
    </xsl:template>
    
    <xsl:template match="article | sub-article" mode="standard-abstract">
        <!--
            apresenta todos os resumos padrão
            priorizando o resumo no idioma selecionado
        -->
        <xsl:choose>
            <xsl:when
                test="sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]">
                <xsl:apply-templates
                    select="sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]/front-stub" mode="standard-abstract"/>
                <xsl:apply-templates
                    select="$article/front/article-meta" mode="standard-abstract"/>
                <xsl:apply-templates
                    select="$article/sub-article[@article-type='translation' and @xml:lang!=$TEXT_LANG]/front-stub" mode="standard-abstract"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="front-stub | front/article-meta" mode="standard-abstract"/>
                <xsl:apply-templates
                    select="sub-article[@article-type='translation']/front-stub" mode="standard-abstract"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="front-stub | front/article-meta" mode="standard-abstract">
        <!-- apresenta os resumos padrão -->
        <xsl:apply-templates select=".//abstract[not(@abstract-type) and not(.//list)]" mode="layout"/>
        <xsl:apply-templates select=".//trans-abstract[not(@abstract-type) and not(.//list)]" mode="layout"/>
    </xsl:template>

    <xsl:template match="article | sub-article" mode="graphical-abstract">
        <xsl:apply-templates select="front/article-meta | front-stub" mode="graphical-abstract"/>
    </xsl:template>

    <xsl:template match="front/article-meta | front-stub" mode="graphical-abstract">
        <xsl:apply-templates select=".//abstract[@abstract-type='graphical']" mode="layout"/>
    </xsl:template>

    <xsl:template match="article" mode="article-meta-no-abstract-keywords">
        <!-- Apresenta keywords para artigos sem resumo -->
        <xsl:if test="not(.//abstract)">
            <xsl:choose>
                <xsl:when test="sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]//kwd-group">
                    <xsl:apply-templates select="sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]//kwd-group" mode="keywords"/>
                </xsl:when>
                <xsl:when test="front/article-meta//kwd-group">
                    <xsl:apply-templates select="front/article-meta//kwd-group" mode="keywords"/>
                </xsl:when>
            </xsl:choose>
        </xsl:if>
    </xsl:template>

    <xsl:template match="article" mode="create-anchor-and-title-for-abstracts-without-title">
        <xsl:variable name="q_titles" select="count(.//abstract[title])+count(.//trans-abstract[title])"/>
        <xsl:if test="$q_titles = 0">
            <xsl:variable name="q_abstracts" select="count(.//abstract[.//text()])+count(.//trans-abstract[.//text()])"/>

            <!-- obtém o título traduzido para Abstracts ou Abstract -->
            <xsl:variable name="title">
                <xsl:apply-templates select="." mode="text-labels">
                    <xsl:with-param name="text">
                        <xsl:choose>
                            <xsl:when test="$q_abstracts=1">Abstract</xsl:when>
                            <xsl:otherwise>Abstracts</xsl:otherwise>
                        </xsl:choose>
                    </xsl:with-param>
                </xsl:apply-templates>
            </xsl:variable>
            
            <!-- insere a âncora e o título -->
            <xsl:apply-templates select="." mode="create-anchor-and-title-for-abstracts-without-title-div-h-number">
                <xsl:with-param name="title"><xsl:value-of select="$title"/></xsl:with-param>
            </xsl:apply-templates>
        </xsl:if>
    </xsl:template>

    <xsl:template match="article" mode="create-anchor-and-title-for-abstracts-without-title-div-h-number">
        <xsl:param name="title"/>
        <!-- manter pareado class="articleSection" e data-anchor="nome da seção no menu esquerdo" -->
        <div class="articleSection" data-anchor="{$title}">
            <h1 class="articleSectionTitle"><xsl:value-of select="$title"/></h1>
        </div>
    </xsl:template>

    <xsl:template match="*[contains(name(),'abstract')]" mode="index">
        <xsl:param name="lang"/>
        <xsl:if test="normalize-space(@xml:lang)=normalize-space($lang)"><xsl:value-of select="position()"/></xsl:if>
    </xsl:template>
    
    <xsl:template match="abstract | trans-abstract" mode="layout">
        <xsl:variable name="lang" select="@xml:lang"/>
        <xsl:variable name="index"><xsl:apply-templates select="..//*[contains(name(),'abstract') and title]" mode="index"><xsl:with-param name="lang" select="$lang"></xsl:with-param></xsl:apply-templates></xsl:variable>
        <div>
            <!-- Apresenta a âncora e o título, ou seja, Abstract, Resumo, ou Resumen -->
            <xsl:apply-templates select="." mode="anchor-and-title"/>

            <!-- Apresenta os demais elementos do resumo -->
            <xsl:apply-templates select="*[name()!='title']"/>

            <!--
            Apresenta as palavras-chave no idioma correspondente, se aplicável
            -->
            <xsl:choose>
                <xsl:when test="not(@abstract-type) and not(.//list)">
                    <!-- apresenta palavras chave com o resumo padrão -->
                    <xsl:apply-templates select="." mode="keywords"/>
                </xsl:when>
                <xsl:otherwise>
                    <!-- do nothing -->
                </xsl:otherwise>
            </xsl:choose>
        </div>
        <xsl:if test="not(title)">
        <hr/>
        </xsl:if>
    </xsl:template>

    <xsl:template match="abstract[not(@xml:lang)] | trans-abstract[not(@xml:lang)]" mode="keywords">
        <!-- apresenta as palavras-chaves no idioma de article/@xml:lang ou sub-article/@xml:lang -->
        <xsl:variable name="lang">
            <xsl:choose>
                <xsl:when test="../../@xml:lang"><xsl:value-of select="../../@xml:lang"/></xsl:when>
                <xsl:when test="../../../@xml:lang"><xsl:value-of select="../../../@xml:lang"/></xsl:when>
            </xsl:choose>
        </xsl:variable>
        <xsl:apply-templates select="../kwd-group[@xml:lang=$lang]" mode="keywords"/>
    </xsl:template>

    <xsl:template match="abstract[@xml:lang] | trans-abstract[@xml:lang]" mode="keywords">
        <!-- apresenta as palavras-chaves no idioma correspondente -->
        <xsl:variable name="lang" select="@xml:lang"/>
        <xsl:apply-templates select="../kwd-group[@xml:lang=$lang]" mode="keywords"/>
    </xsl:template>

    <xsl:template match="abstract[not(title)] | trans-abstract[not(title)]" mode="anchor-and-title">
    </xsl:template>

    <xsl:template match="abstract[title] | trans-abstract[title]" mode="anchor-and-title">
        <!-- Apresenta a âncora e o título, ou seja, Abstract, Resumo, ou Resumen -->

        <!-- âncora -->
        <!-- manter pareado class="articleSection" e data-anchor="nome da seção no menu esquerdo" -->
        <xsl:attribute name="class">articleSection</xsl:attribute>
        <xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="title"/></xsl:attribute>
        <xsl:if test="@xml:lang='ar'">
            <xsl:attribute name="dir">rtl</xsl:attribute>
        </xsl:if>

        <!-- título -->
        <h1>
            <xsl:attribute name="class">articleSectionTitle</xsl:attribute>
            <xsl:apply-templates select="." mode="title"></xsl:apply-templates>
        </h1>
    </xsl:template>

    <xsl:template match="abstract/title | trans-abstract/title">
        <xsl:apply-templates select="*|text()"/>
    </xsl:template>
    
    <xsl:template match="abstract/sec/title | trans-abstract/sec/title">
        <h2><xsl:apply-templates select="*|text()"/></h2>
    </xsl:template>
    
    <xsl:template match="kwd-group"></xsl:template>
    <xsl:template match="kwd-group" mode="keywords">
        <p><xsl:apply-templates select="*"/></p>
    </xsl:template>
    
    <xsl:template match="kwd-group/title">
        <strong><xsl:value-of select="."/></strong><br/>
    </xsl:template>
    
    <xsl:template match="kwd"><xsl:apply-templates select="*|text()"></xsl:apply-templates><xsl:if test="position()!=last()">; </xsl:if>
    </xsl:template>
    
    <xsl:template match="article" mode="article-meta-abstract-gs">
        <!-- PÁGINA DO RESUMO -->
        <!-- APRESENTA O RESUMO NO IDIOMA CORRESPONDENTE -->
        <xsl:choose>
            <xsl:when
                test="@xml:lang=$gs_abstract_lang">
                <xsl:apply-templates
                    select="front/article-meta/abstract" mode="layout"/>
            </xsl:when>
            <xsl:when
                test="sub-article[@article-type='translation' and @xml:lang=$gs_abstract_lang]">
                <xsl:apply-templates
                    select="sub-article[@article-type='translation' and @xml:lang=$gs_abstract_lang]/front-stub/abstract" mode="layout"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select=".//trans-abstract[@xml:lang=$gs_abstract_lang]" mode="layout"/>
            </xsl:otherwise>
        </xsl:choose>

        <xsl:if test="sub-article and count(.//abstract[@abstract-type='graphical'])=1">
            <!-- um resumo gráfico para todas as versões -->
            <xsl:apply-templates select=".//abstract[@abstract-type='graphical']" mode="layout"/>
        </xsl:if>
    </xsl:template>
      
</xsl:stylesheet>