<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    
    <xsl:template match="article" mode="text-back">
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG]">
                <xsl:if test="$prev='' and $next=''">
                    <xsl:apply-templates select="back/ref-list" mode="layout"/>
                </xsl:if>
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG]//back/*" mode="layout"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="./back/*" mode="layout"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>        
    </xsl:template>
    
    <xsl:template match="back/*" mode="layout">
        <div class="articleSection">
            <xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="title"></xsl:apply-templates></xsl:attribute>
            <a name="articleSection{$body_index + position()}"></a>
            <div class="row">
                <div class="col-md-12 col-sm-12">
                    <h1><xsl:apply-templates select="." mode="title"/></h1>
                </div>
            </div>
            <xsl:apply-templates select="." mode="content"></xsl:apply-templates>
        </div>
    </xsl:template>
    
    <xsl:template match="sub-article[@article-type='translation']//back[not(ref-list)]/*" mode="layout">
        <xsl:variable name="following"><xsl:apply-templates select="." mode="next"></xsl:apply-templates></xsl:variable>
        <xsl:choose>
            <xsl:when test="$prev!='' and $next!=''">
                <xsl:if test="name()=$prev and $following=$next">
                    <div class="articleSection">
                        <xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="title"></xsl:apply-templates></xsl:attribute>
                        <a name="articleSection{$body_index + position()}"></a>
                        <div class="row">
                            <div class="col-md-12 col-sm-12">
                                <h1><xsl:apply-templates select="." mode="title"/></h1>
                            </div>
                        </div>
                        <xsl:apply-templates select="." mode="content"></xsl:apply-templates>
                    </div>
                    <xsl:apply-templates select="$document/article/back/ref-list" mode="layout"></xsl:apply-templates>
                </xsl:if>
            </xsl:when>
            <xsl:when test="$prev!=''">
                <xsl:if test="$prev=name()">
                    <div class="articleSection">
                        <xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="title"></xsl:apply-templates></xsl:attribute>
                        <a name="articleSection{$body_index + position()}"></a>
                        <div class="row">
                            <div class="col-md-12 col-sm-12">
                                <h1><xsl:apply-templates select="." mode="title"/></h1>
                            </div>
                        </div>
                        <xsl:apply-templates select="." mode="content"></xsl:apply-templates>
                    </div>
                    <xsl:apply-templates select="$document/article/back/ref-list" mode="layout"></xsl:apply-templates>
                </xsl:if>
            </xsl:when>
            <xsl:when test="$next!=''">
                <xsl:if test="$next=name()">
                    <xsl:apply-templates select="$document/article/back/ref-list" mode="layout"></xsl:apply-templates>
                    <div class="articleSection">
                        <xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="title"></xsl:apply-templates></xsl:attribute>
                        <a name="articleSection{$body_index + position()}"></a>
                        <div class="row">
                            <div class="col-md-12 col-sm-12">
                                <h1><xsl:apply-templates select="." mode="title"/></h1>
                            </div>
                        </div>
                        <xsl:apply-templates select="." mode="content"></xsl:apply-templates>
                    </div>
                </xsl:if>
            </xsl:when>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="back/*" mode="content">
        <xsl:apply-templates select="*[name()!='title']|text()" mode="content"></xsl:apply-templates>
    </xsl:template>
</xsl:stylesheet>