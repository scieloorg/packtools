<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/article-meta-contrib.xsl"/>

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

    <xsl:template match="article-meta/contrib-group | front/contrib-group | front-stub/contrib-group" mode="about-the-contrib-group-button">
        <!--
            Adiciona o botão 'About the contributor', trocando 'author',
            pelo tipo de contribuição
        -->
        <xsl:if test="contrib/*[name()!='name' and name()!='collab']">
            <xsl:variable name="id"><xsl:apply-templates select="." mode="modal-id"></xsl:apply-templates></xsl:variable>
            <a href="" class="btn btn-secondary btn-sm outlineFadeLink"
                data-bs-toggle="modal"
                data-bs-target="#ModalTutors{$id}">
                <xsl:apply-templates select="." mode="interface">
                    <xsl:with-param name="text"><xsl:apply-templates select="contrib[1]" mode="about-the-contrib-group-button-text"/><xsl:if test="count(contrib)&gt;1">s</xsl:if></xsl:with-param>
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


    <xsl:template match="contrib" mode="contrib-dropdown-menu">
        <xsl:param name="id"/>
        <xsl:if test="role or xref or contrib-id or bio">
            <ul class="dropdown-menu" role="menu" aria-labelledby="contribGrupoTutor{$id}">
                <xsl:apply-templates select="." mode="contrib-dropdown-menu-general"/>
                <xsl:apply-templates select="xref[@ref-type='corresp']" mode="contrib-dropdown-menu-corresp"/>
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

    <xsl:template match="*" mode="contrib-dropdown-menu-corresp">
        <xsl:apply-templates select="*|text()"/>
    </xsl:template>

    <xsl:template match="xref[@ref-type='corresp']" mode="contrib-dropdown-menu-corresp">
        <xsl:variable name="rid"><xsl:value-of select="@rid"/></xsl:variable>
        <!--
            <li><div class="corresp"> <h3><sup>4</sup></h3> Autor para correspondência: <a href="mailto:author@gmail.com">author@gmail.com</a> </div></li>
        -->

        <li>
            <xsl:apply-templates select="$article//*[@id=$rid]" mode="contrib-dropdown-menu-corresp"/>
        </li>
    </xsl:template>    

    <xsl:template match="author-notes/corresp" mode="contrib-dropdown-menu-corresp">
        <div class="corresp">
            <xsl:apply-templates select="*|text()"/>
        </div>
    </xsl:template>

</xsl:stylesheet>