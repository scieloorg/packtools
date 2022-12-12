<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:template match="article" mode="article-meta-contrib">
        <xsl:choose>
            <xsl:when
                test=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]//contrib-group">
                <xsl:apply-templates
                    select=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]" mode="contrib-group"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="." mode="contrib-group"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="article" mode="contrib-group">
        <div>
            <xsl:attribute name="class">scielo__contribGroup</xsl:attribute>
            <xsl:apply-templates select="front/article-meta//contrib-group"/>
        </div>
    </xsl:template>
    
    <xsl:template match="sub-article" mode="contrib-group">
        <div>
            <xsl:attribute name="class">scielo__contribGroup</xsl:attribute>
            <xsl:apply-templates select="front-stub/contrib-group | front/contrib-group"></xsl:apply-templates>
            <xsl:if test="not(.//contrib) and ../@article-type='translation'">
                <xsl:apply-templates select="$article//article-meta//contrib"></xsl:apply-templates>
            </xsl:if>
        </div>
    </xsl:template>
    
    <xsl:template match="front/contrib-group | front-stub/contrib-group" mode="modal-id"><xsl:value-of select="../../@id"/></xsl:template>
    <xsl:template match="article-meta/contrib-group | sub-article[@article-type='translation']/*/contrib-group" mode="modal-id"></xsl:template>
    
    <xsl:template match="article-meta/contrib-group | front/contrib-group | front-stub/contrib-group">
        <xsl:variable name="id"><xsl:apply-templates select="." mode="modal-id"></xsl:apply-templates></xsl:variable>
        <xsl:apply-templates select="contrib[@contrib-type='author']" mode="article-meta-contrib"/>
        <xsl:if test="contrib/*[name()!='name' and name()!='collab']">
            <a href="" class="outlineFadeLink" data-bs-toggle="modal"
                data-bs-target="#ModalTutors{$id}">
                <xsl:apply-templates select="." mode="interface">
                    <xsl:with-param name="text">About the author<xsl:if test="count(contrib[@contrib-type='author'])&gt;1">s</xsl:if></xsl:with-param>
                </xsl:apply-templates>
            </a>
        </xsl:if>
    </xsl:template>
   
    <xsl:template match="contrib" mode="article-meta-contrib">
        <xsl:variable name="id">
            <xsl:value-of select="position()"/>
        </xsl:variable>
        <div class="dropdown">
            <button id="contribGroupTutor{$id}">
                <xsl:attribute name="class">btn btn-secondary dropdown-toggle</xsl:attribute>
                <xsl:attribute name="type">button</xsl:attribute>
                <xsl:attribute name="data-bs-toggle">dropdown</xsl:attribute>
                <xsl:attribute name="aria-expanded">false</xsl:attribute>
                <xsl:choose>
                    <xsl:when test="$ABBR_CONTRIB='true'">
                        <xsl:apply-templates select="name|collab|on-behalf-of" mode="abbrev"/>
                    </xsl:when>
                    <xsl:otherwise><xsl:apply-templates select="name|collab|on-behalf-of"/></xsl:otherwise>
                </xsl:choose>
            </button>
            <xsl:apply-templates select="." mode="contrib-dropdown-menu">
                <xsl:with-param name="id">
                    <xsl:value-of select="$id"/>
                </xsl:with-param>
            </xsl:apply-templates>
        </div>
    </xsl:template>

    <xsl:template match="sub-article[@article-type!='translation']//contrib" mode="article-meta-contrib">
        <span class="dropdown"> 
            <xsl:if test="position() != 1"><span> • </span></xsl:if>
            <span>
                <xsl:choose>
                    <xsl:when test="$ABBR_CONTRIB='true'">
                        <xsl:apply-templates select="name|collab|on-behalf-of" mode="abbrev"/>
                    </xsl:when>
                    <xsl:otherwise><xsl:apply-templates select="name|collab|on-behalf-of"/></xsl:otherwise>
                </xsl:choose>
            </span>
            
        </span>
    </xsl:template>

    <xsl:template match="contrib/role | contrib/bio">
        <div>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </div>
    </xsl:template>
    
    <xsl:template match="contrib" mode="contrib-dropdown-menu">
        <xsl:param name="id"/>
        <xsl:if test="role or xref or contrib-id or bio">
            <ul class="dropdown-menu" role="menu" aria-labelledby="contribGrupoTutor{$id}">
                <xsl:apply-templates select="." mode="contrib-dropdown-menu-general"/>
                <xsl:apply-templates select="." mode="contrib-dropdown-menu-corresp"/>
            </ul>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="contrib" mode="contrib-dropdown-menu-general">
        <xsl:if test="role or xref[@ref-type!='corresp'] or contrib-id or bio">
            <li>
                <xsl:apply-templates select="role | bio"/>
                <xsl:apply-templates select="xref[@ref-type!='corresp']" mode="contrib-dropdown-menu"/>
                <xsl:apply-templates select="contrib-id"/>
            </li>
        </xsl:if>
    </xsl:template>

    <xsl:template match="contrib" mode="contrib-dropdown-menu-corresp">
        <xsl:if test="xref[@ref-type='corresp']">
            <li>
                <xsl:apply-templates select="xref[@ref-type!='corresp']" mode="contrib-dropdown-menu"/>
            </li>
        </xsl:if>
    </xsl:template>

    <xsl:template match="contrib/xref" mode="contrib-dropdown-menu">
        <xsl:variable name="rid" select="@rid"/>
        <xsl:apply-templates select="$article//author-notes/corresp[@id=$rid]" mode="contrib-dropdown-menu"/>
            <xsl:apply-templates select="$article//aff[@id=$rid]" mode="contrib-dropdown-menu"/>
        <xsl:apply-templates select="$article//fn[@id=$rid]" mode="xref"/>
    </xsl:template>
    
    <xsl:template match="aff" mode="contrib-dropdown-menu">
            <xsl:apply-templates select="." mode="display"/>
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
    
    <xsl:template match="contrib/name" mode="abbrev">
        <xsl:value-of select="substring(given-names,1,1)"/>
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
        <a href="{$location}" class="btnContribLinks {@contrib-id-type}">
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

    <xsl:template match="aff//*" mode="insert-separator">
        <xsl:apply-templates select="*|text()" mode="insert-separator"/>
    </xsl:template>

    <xsl:template match="aff//text()" mode="insert-separator">
        <xsl:value-of select="."/>,&#160; </xsl:template>

    <xsl:template match="aff/*[position()=last()]/text()" mode="insert-separator">
        <xsl:value-of select="."/>
    </xsl:template>

    <xsl:template match="aff/text()" mode="insert-separator">
        <xsl:value-of select="."/>
    </xsl:template>
    
    <xsl:template match="aff" mode="display">
        <xsl:variable name="text"><xsl:apply-templates select="text()"/></xsl:variable>
        <!--
        <xsl:comment> $text: <xsl:value-of select="$text"/> </xsl:comment>
        <xsl:comment> text(): <xsl:apply-templates select="text()"></xsl:apply-templates></xsl:comment>
        -->
        <xsl:choose>
            <xsl:when test="institution[@content-type='original']">
                <!--
                <xsl:comment> aff original </xsl:comment>
                -->
                <xsl:apply-templates select="institution[@content-type='original']"/>
            </xsl:when>
            <xsl:when
                test="institution[@content-type='orgname'] and contains($text,institution[@content-type='orgname'])">
                <!--
                <xsl:comment> $text </xsl:comment>
                -->
                <xsl:value-of select="$text"/>
            </xsl:when>
            <xsl:when
                test="*[name()!='label']">
                <!--
                <xsl:comment> aff insert separator </xsl:comment>
                -->
                <xsl:apply-templates select="*[name()!='label']" mode="insert-separator"/>
            </xsl:when>
            <xsl:otherwise>
                <!--
                <xsl:comment> $text </xsl:comment>
                -->
                <xsl:value-of select="$text"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template match="role">
        <xsl:if test="position()!=1">, </xsl:if><xsl:apply-templates select="*|text()"></xsl:apply-templates>
    </xsl:template>
</xsl:stylesheet>
