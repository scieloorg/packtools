<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:template match="article" mode="article-meta-contrib">
        <xsl:choose>
            <xsl:when
                test=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]//front-stub//contrib-group">
                <xsl:apply-templates
                    select=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]" mode="contrib-group"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="." mode="contrib-group"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="article" mode="contrib-group">
        <xsl:if test="not(body//sig)">
            <xsl:apply-templates select=".//article-meta//contrib-group"/>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="sub-article" mode="contrib-group">
        <xsl:if test="not(body//sig)">
            <xsl:apply-templates select=".//front-stub//contrib-group"></xsl:apply-templates>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="contrib-group">
        <div class="contribGroup">
            <xsl:apply-templates select="contrib" mode="article-meta-contrib"/>
            <xsl:if test="contrib[*]">
                <a href="" class="outlineFadeLink" data-toggle="modal"
                    data-target="#ModalTutors">
                    <xsl:apply-templates select="." mode="interface">
                        <xsl:with-param name="text">About the authors</xsl:with-param>
                    </xsl:apply-templates>
                </a>
            </xsl:if>
        </div>
    </xsl:template>
    
    <xsl:template match="sub-article[body//sig]//contrib-group">
    </xsl:template>

    <xsl:template match="contrib" mode="article-meta-contrib">
        <xsl:variable name="id">
            <xsl:value-of select="position()"/>
        </xsl:variable>
        
        <span class="dropdown">
            <a id="contribGroupTutor{$id}">
                <xsl:if test="role or xref or contrib-id">
                    <xsl:attribute name="class">dropdown-toggle</xsl:attribute>
                    <xsl:attribute name="data-toggle">dropdown</xsl:attribute>
                </xsl:if>
                <span>
                    <xsl:apply-templates select="name|collab|on-behalf-of"/>
                </span>
            </a>
            <xsl:apply-templates select="." mode="contrib-dropdown-menu">
                <xsl:with-param name="id">
                    <xsl:value-of select="$id"/>
                </xsl:with-param>
            </xsl:apply-templates>
        </span>
    </xsl:template>

    <xsl:template match="contrib" mode="contrib-dropdown-menu">
        <xsl:param name="id"/>
        <xsl:if test="role or xref or contrib-id">
            <ul class="dropdown-menu" role="menu" aria-labelledby="contribGrupoTutor{$id}">
                <xsl:apply-templates select="role"/>
                <xsl:apply-templates select="xref"/>
                <xsl:apply-templates select="contrib-id"/>
            </ul>
        </xsl:if>
    </xsl:template>

    <xsl:template match="contrib/name">
        <xsl:apply-templates select="prefix"/>
        <xsl:text> </xsl:text>
        <xsl:apply-templates select="given-names"/>
        <xsl:text> </xsl:text>
        <xsl:apply-templates select="surname"/>
        <xsl:text> </xsl:text>
        <xsl:apply-templates select="suffix"/>
    </xsl:template>

    <xsl:template match="contrib-id">
        <xsl:variable name="url">
            <xsl:apply-templates select="." mode="url"/>
        </xsl:variable>
        <xsl:variable name="location">
            <xsl:value-of select="$url"/>
            <xsl:value-of select="."/>
        </xsl:variable>
        <a href="" class="btnContribLinks {@contrib-id-type}">
            <xsl:value-of select="$location"/>
        </a>
    </xsl:template>

    <xsl:template match="contrib-id" mode="url"/>
    <xsl:template match="contrib-id[@contrib-id-type='orcid']" mode="url"
        >http://orcid.org/</xsl:template>
    <xsl:template match="contrib-id[@contrib-id-type='lattes']" mode="url"
        >http://lattes.cnpq.br/</xsl:template>
    <xsl:template match="contrib-id[@contrib-id-type='scopus']" mode="url"
        >https://www.scopus.com/authid/detail.uri?authorId=</xsl:template>
    <xsl:template match="contrib-id[@contrib-id-type='researchid']" mode="url"
        >http://www.researcherid.com/rid/</xsl:template>

    <xsl:template match="aff//*" mode="aff">
        <xsl:apply-templates select="*|text()" mode="aff"/>
    </xsl:template>

    <xsl:template match="aff//text()" mode="aff">
        <xsl:value-of select="."/>,&#160; </xsl:template>

    <xsl:template match="aff/*[position()=last()]/text()" mode="aff">
        <xsl:value-of select="."/>
    </xsl:template>

    <xsl:template match="aff/text()" mode="aff">
        <xsl:value-of select="."/>
    </xsl:template>

    <xsl:template match="aff">
        <xsl:choose>
            <xsl:when test="institution[@content-type='original']">
                <xsl:apply-templates select="institution[@content-type='original']"/>
            </xsl:when>
            <xsl:when
                test="institution[@content-type='orgname'] and contains(text(),institution[@content-type='orgname'])">
                <xsl:apply-templates select="text()" mode="aff"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="*[name()!='label']" mode="aff"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>
