<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">

    <xsl:template match="article" mode="count_abstract_title">
        <xsl:choose>
            <xsl:when test=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]//abstract">
                <xsl:apply-templates select=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]" mode="count_abstract_title"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="count(front/article-meta//abstract[title])+count(front/article-meta//trans-abstract[title])"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template match="sub-article[@article-type='translation']" mode="count_abstract_title">
        <xsl:value-of select="count(.//abstract[title])+count(.//trans-abstract[title])"/>
    </xsl:template>
    
    <xsl:template match="article" mode="count_abstracts">
        <xsl:choose>
            <xsl:when test=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]//abstract">1</xsl:when>
            <xsl:when test="front/article-meta//abstract">1</xsl:when>
            <xsl:otherwise>0</xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="article | sub-article[@article-type='translation']" mode="count_history">
        <xsl:choose>
            <xsl:when test=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]//history">
                <xsl:apply-templates select=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]" mode="count_history"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="count(.//history)"></xsl:value-of>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="article" mode="count_back_elements">
        <xsl:choose>
            <xsl:when test=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]">
                <xsl:apply-templates select=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]" mode="count_back_elements"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="count(back/*[title])"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="sub-article[@article-type='translation']" mode="count_back_elements">
        <xsl:choose>
            <xsl:when test="back/ref-list">
                <xsl:value-of select="count(back/*[title])"/>
            </xsl:when>
            <xsl:when test="../back/ref-list[title]">
                <xsl:value-of select="count(back/*[title])+1"/>
            </xsl:when>
            <xsl:otherwise><xsl:value-of select="count(back/*[title])"/></xsl:otherwise>
        </xsl:choose>       
    </xsl:template>
    
    <xsl:template match="article | sub-article[@article-type='translation']" mode="count_subarticle">
        <xsl:choose>
            <xsl:when test=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]">
                <xsl:apply-templates select=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]" mode="count_subarticle"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="count(.//sub-article[@article-type!='translation' and @xml:lang=$TEXT_LANG])+count(.//response)"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="article" mode="count_body_fn">
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//body//*[(fn or fn-group) and name()!='table-wrap']">1</xsl:when>
            <xsl:when test="./body//*[(fn or fn-group) and name()!='table-wrap']">1</xsl:when>
            <xsl:otherwise>0</xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="*" mode="position">
        <xsl:param name="name"></xsl:param>
        <xsl:if test="name()=$name"><xsl:value-of select="position()"/></xsl:if>
    </xsl:template>
    
    <xsl:template match="sec[@sec-type]" mode="index">
        <xsl:param name="sectype"/>
        <xsl:if test="@sec-type=$sectype"><xsl:value-of select="number(position()-1)"/></xsl:if>
    </xsl:template>
    
    <xsl:template match="body" mode="index">
        <xsl:param name="sectype"/>
        <xsl:apply-templates select=".//sec[@sec-type]" mode="index">
            <xsl:with-param name="sectype"><xsl:value-of select="$sectype"/></xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="back/*" mode="index">
        <xsl:param name="title"/>
        <xsl:if test="title">
            <xsl:if test="normalize-space(title)=normalize-space($title)"><xsl:value-of select="position()"/></xsl:if>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="back" mode="index">
        <xsl:param name="title"/>
        
        <xsl:if test="$title!=''">
            <xsl:variable name="index"><xsl:apply-templates select="*[title]" mode="index">
                <xsl:with-param name="title"><xsl:value-of select="$title"/></xsl:with-param>
            </xsl:apply-templates></xsl:variable>
            <xsl:choose>
                <xsl:when test="ref-list">
                    <xsl:value-of select="$index"/>
                </xsl:when>
                <xsl:when test="not(ref-list) and $REFLIST_INDEX!=''">
                    <xsl:choose>
                        <xsl:when test="$index &lt; $REFLIST_INDEX">
                            <xsl:value-of select="$index"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:value-of select="$index+1"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="$index"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:if>
    </xsl:template>
    
</xsl:stylesheet>