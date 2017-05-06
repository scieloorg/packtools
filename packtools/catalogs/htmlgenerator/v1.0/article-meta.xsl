<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    >
    
    <xsl:template match="*" mode="article-meta-doi">
        <xsl:apply-templates select=".//article-meta//article-id[@pub-id-type='doi']"></xsl:apply-templates>        
    </xsl:template>
   
    <xsl:template match="article-id[@pub-id-type='doi']">
        <xsl:variable name="link">https://doi.org/<xsl:value-of select="."/></xsl:variable>
        <div class="row articleMeta">
            <div class="col-md-5 col-sm-12">
                <span>DOI: <xsl:value-of select="."/></span>
            </div>
        </div>    
    </xsl:template>
    
    <xsl:template match="article-meta/title-group/article-title|article-meta/title-group//trans-title">
        <h1 class="article-title">
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>    
        </h1>
    </xsl:template>
    
    
    <xsl:template match="article" mode="article-meta-link-group">
        <div class="linkGroup">
            <a name="authorInfo"></a>
            <div class="row">
                <div class="col-md-4 col-sm-4">
                    <a href="javascript:;" class="link showFloatInfo" data-rel=".linkGroup;#authorInfo;#copyrightInfo" id="authorInfoBtn"><span class="glyphBtn authorInfo"></span> Sobre os autores</a>
                    <!-- FIXME: Sobre autores -->
                </div>
                <div class="col-md-5 col-sm-5">
                    <a href="javascript:;" class="link showFloatInfo" data-rel=".linkGroup;#copyrightInfo;#authorInfo" id="copyrightInfoBtn"><span class="glyphBtn copyrightInfo"></span> Permissões</a>
                    <!-- FIXME: Permissões -->
                </div>
            </div>
            <div class="floatInformation" id="authorInfo">
                <button type="button" class="close showFloatInfo" data-rel=".linkGroup;null;#authorInfo"><span aria-hidden="true">&#215;</span></button>
                <xsl:apply-templates select="." mode="article-meta-affiliations"></xsl:apply-templates>
                <div class="rowBlock">
                    <a href=""><span class="glyphBtn scientiLogo"></span> Curriculum ScienTI</a>
                    <!-- FIXME: Curriculum ScienTI -->
                </div>
                <xsl:apply-templates select="." mode="article-meta-author-notes"></xsl:apply-templates>
            </div>
            <xsl:apply-templates select="." mode="article-meta-licenses"></xsl:apply-templates>
        </div>
    </xsl:template>
    
    <xsl:template match="article" mode="article-meta-licenses">
        <div class="floatInformation" id="copyrightInfo">
            <button type="button" class="close showFloatInfo" data-rel=".linkGroup;null;#copyrightInfo"><span aria-hidden="true">&#215;</span></button>
            <div class="rowBlock">
                <xsl:apply-templates select="." mode="lang-license"></xsl:apply-templates>
            </div>
        </div>
    </xsl:template>
    <xsl:template match="license">
        <xsl:apply-templates select="license-p"></xsl:apply-templates><br/>
        <a href="{@xlink:href}">» <xsl:apply-templates select="." mode="labels-license-view"></xsl:apply-templates></a>
        <!-- FIXME: Veja as permissões desta licença -->
    </xsl:template>
    
</xsl:stylesheet>