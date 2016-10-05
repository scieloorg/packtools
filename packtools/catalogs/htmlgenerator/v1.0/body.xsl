<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="article" mode="body">
        <div class="row articleTxt">
            <ul class="col-md-2 hidden-sm articleMenu">
            </ul>
            <article id="articleText" class="col-md-10 col-md-offset-2 col-sm-12">
                <xsl:apply-templates select="." mode="front-abstract"></xsl:apply-templates>
                <xsl:apply-templates select="." mode="body-body"></xsl:apply-templates>
            </article>
        </div>
    </xsl:template>
    <xsl:template match="*" mode="body-body">
        <div class="articleSection" data-anchor="Texto">
            <!-- FIXME: body ou sub-article/body -->
            <xsl:apply-templates select="./body"></xsl:apply-templates>
        </div>
    </xsl:template>
    
    <xsl:template match="body">
        <xsl:apply-templates select="*"></xsl:apply-templates>    
    </xsl:template>
    
    <xsl:template match="body/*">
        <xsl:apply-templates select="*|text()"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="body/sec[@sec-type]">
        <xsl:apply-templates select="*">
            <xsl:with-param name="position" select="position()"></xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="body/sec/title">
        <xsl:param name="position"></xsl:param>
        <div class="row">
            <a name="as1-heading{$position - 1}"></a>
            <div class="col-md-8 col-sm-9 text">
                <h1>
                    <xsl:if test="../@sec-type">
                        <xsl:attribute name="id">text-<xsl:value-of select="../@sec-type"/></xsl:attribute>
                    </xsl:if>
                    <xsl:apply-templates select="*|text()"/>
                </h1>
            </div>
        </div>
    </xsl:template>
</xsl:stylesheet>