<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <!-- não usar a versão 2.0
    <xsl:include href="../v2.0/article-meta-abstract.xsl"/>
    -->
    <xsl:variable name="total_abstracts" select="count(.//abstract)+count(.//trans-abstract)"/>
    <xsl:variable name="has_abstract_title" select=".//abstract[title]"/>

    <xsl:template match="article" mode="article-meta-abstract">
        <xsl:choose>
            <xsl:when test="sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]">
                <xsl:apply-templates select="sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]" mode="text-abstracts"/>
                <xsl:apply-templates select="." mode="text-abstracts"/>
                <xsl:apply-templates select="sub-article[@article-type='translation' and @xml:lang!=$TEXT_LANG]" mode="text-abstracts"/>
                <xsl:apply-templates select="." mode="text-trans-abstracts"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="." mode="text-abstracts"/>
                <xsl:apply-templates select="sub-article[@article-type='translation']" mode="text-abstracts"/>
                <xsl:apply-templates select="." mode="text-trans-abstracts"/>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:apply-templates select="." mode="article-meta-no-abstract-keywords"/>
    </xsl:template>

    <xsl:template match="article" mode="text-trans-abstracts">
        <xsl:apply-templates select=".//article-meta[trans-abstract]" mode="text-trans-abstracts"/>
    </xsl:template>
    <xsl:template match="article" mode="text-abstracts">
        <xsl:apply-templates select=".//article-meta[abstract]" mode="text-abstracts"/>
    </xsl:template>

    <xsl:template match="sub-article" mode="text-abstracts">
        <xsl:apply-templates select="front-stub[abstract]" mode="text-abstracts"/>
    </xsl:template>

    <xsl:template match="*[abstract]" mode="text-abstracts">
        <xsl:apply-templates select="." mode="create-anchor-and-title-for-abstracts-without-title"/>

        <xsl:apply-templates select="abstract[not(@abstract-type)]" mode="layout"/>
        <xsl:apply-templates select="abstract[@abstract-type='key-points']" mode="layout"/>
        <xsl:apply-templates select="abstract[@abstract-type='graphical']" mode="layout"/>
        <xsl:apply-templates select="abstract[@abstract-type='summary']" mode="layout"/>
    </xsl:template>

    <xsl:template match="*[trans-abstract]" mode="text-trans-abstracts">
        <xsl:apply-templates select="trans-abstract[not(@abstract-type)]" mode="layout"/>
        <xsl:apply-templates select="trans-abstract[@abstract-type='key-points']" mode="layout"/>
        <xsl:apply-templates select="trans-abstract[@abstract-type='graphical']" mode="layout"/>
        <xsl:apply-templates select="trans-abstract[@abstract-type='summary']" mode="layout"/>
    </xsl:template>

    <xsl:template match="*[abstract]" mode="create-anchor-and-title-for-abstracts-without-title">
        <xsl:if test="not($has_abstract_title)">
            <xsl:variable name="title">
                <xsl:apply-templates select="." mode="text-labels">
                    <xsl:with-param name="text">
                        <xsl:choose>
                            <xsl:when test="$total_abstracts=1">Abstract</xsl:when>
                            <xsl:otherwise>Abstracts</xsl:otherwise>
                        </xsl:choose>
                    </xsl:with-param>
                </xsl:apply-templates>
            </xsl:variable>
            <xsl:variable name="title_id">
                <xsl:value-of select="translate($title,'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')"/>
            </xsl:variable>
            <div class="articleSection articleSection--{$title_id}:" data-anchor="{$title}"><a name="articleSection0"></a>
                <h2 class="h5"><xsl:value-of select="$title"/></h2>
            </div>
        </xsl:if>
    </xsl:template>

    <xsl:template match="abstract[not(title)] | trans-abstract[not(title)]" mode="anchor-and-title">
    </xsl:template>

    <xsl:template match="abstract[title] | trans-abstract[title]" mode="anchor-and-title">
        <!-- Apresenta a âncora e o título, ou seja, Abstract, Resumo, ou Resumen -->

        <xsl:if test="not($gs_abstract_lang)">
            <!-- âncora -->
            <!-- manter pareado class="articleSection" e data-anchor="nome da seção no menu esquerdo" -->
            <xsl:call-template name="article-section-header">
                <xsl:with-param name="title"><xsl:apply-templates select="." mode="title"/></xsl:with-param>
            </xsl:call-template>
            <xsl:if test="@xml:lang='ar'">
                <xsl:attribute name="dir">rtl</xsl:attribute>
            </xsl:if>
        </xsl:if>

        <!-- título -->
        <h2>
            <xsl:attribute name="class">h5</xsl:attribute>
            <xsl:apply-templates select="." mode="title"></xsl:apply-templates>
        </h2>
    </xsl:template>

    <xsl:template match="*[contains(name(),'abstract')]" mode="index">
        <xsl:param name="lang"/>
        <xsl:if test="normalize-space(@xml:lang)=normalize-space($lang)"><xsl:value-of select="position()"/></xsl:if>
    </xsl:template>
    
    <!-- ABSTRACT BLOCK -->
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
            <xsl:if test="not(@abstract-type)">
                <!-- apresenta palavras chave com o resumo padrão -->
                <xsl:apply-templates select="." mode="keywords"/>
            </xsl:if>
        </div>
        <xsl:if test="not(title)">
        <hr/>
        </xsl:if>
    </xsl:template>

    <!-- ABSTRACT COMPONENTS -->
    <xsl:template match="abstract/title | trans-abstract/title">
        <xsl:apply-templates select="*|text()"/>
    </xsl:template>

    <xsl:template match="abstract/sec/title | trans-abstract/sec/title | kwd-group/title">
        <strong><xsl:apply-templates select="*|text()"/></strong><xsl:text>&#160;</xsl:text>
    </xsl:template>

    <xsl:template match="abstract/sec | trans-abstract/sec">
        <p>
            <xsl:apply-templates select="*|text()"/>
        </p>
    </xsl:template>

    <xsl:template match="abstract/sec/p | trans-abstract/sec/p">
        <xsl:apply-templates select="*|text()"/>
    </xsl:template>
    
    <!-- KEYWORDS -->
    <xsl:template match="abstract[not(@abstract-type)]" mode="keywords">
        <!-- apresenta as palavras-chaves no idioma correspondente -->
        <xsl:variable name="lang" select="../../../@xml:lang"/>
        <xsl:apply-templates select="../kwd-group[@xml:lang=$lang]" mode="keywords"/>
    </xsl:template>

    <xsl:template match="sub-article//abstract[not(@abstract-type)]" mode="keywords">
        <!-- apresenta as palavras-chaves no idioma correspondente -->
        <xsl:variable name="lang" select="../../@xml:lang"/>
        <xsl:apply-templates select="../kwd-group[@xml:lang=$lang]" mode="keywords"/>
    </xsl:template>

    <xsl:template match="trans-abstract[not(@abstract-type)]" mode="keywords">
        <xsl:variable name="lang" select="@xml:lang"/>
        <xsl:apply-templates select="../kwd-group[@xml:lang=$lang]" mode="keywords"/>
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
 
    <!-- revisar a partir daqui-->
    <xsl:template match="article" mode="article-meta-no-abstract-keywords">
        <!-- Apresenta keywords para artigos sem resumo -->
        <xsl:if test="not(.//abstract) and .//kwd-group">
            <xsl:choose>
                <xsl:when test="sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]//kwd-group">
                    <xsl:apply-templates select="sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]//kwd-group" mode="keywords"/>
                    <xsl:apply-templates select="..//kwd-group[@xml:lang!=$TEXT_LANG]" mode="keywords"/>
                </xsl:when>
                <xsl:when test="front/article-meta//kwd-group">
                    <xsl:apply-templates select="//kwd-group" mode="keywords"/>
                </xsl:when>
            </xsl:choose>
        </xsl:if>
    </xsl:template>

    <xsl:template match="article" mode="article-meta-abstract-gs">
        <xsl:choose>
            <xsl:when test="@xml:lang=$gs_abstract_lang">
                <xsl:apply-templates select="." mode="text-abstracts"/>
            </xsl:when>
            <xsl:when test="sub-article[@article-type='translation' and @xml:lang=$gs_abstract_lang]">
                <xsl:apply-templates select="sub-article[@article-type='translation' and @xml:lang=$gs_abstract_lang]" mode="text-abstracts"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select=".//trans-abstract[@xml:lang=$gs_abstract_lang]" mode="layout"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

</xsl:stylesheet>