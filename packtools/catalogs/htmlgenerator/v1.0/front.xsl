<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml"
    version="1.0">
    
    <xsl:template match="article-meta/title-group/article-title|article-meta/title-group//trans-title">
        <h1 class="article-title">
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>    
        </h1>
    </xsl:template>
    <xsl:template match="article-id[@pub-id-type='doi']">
        <xsl:variable name="link">https://doi.org/<xsl:value-of select="."/></xsl:variable>
        <div class="row articleMeta">
            <div class="col-md-5 col-sm-12">
                <span>DOI: <xsl:value-of select="."/></span>
            </div>
            <div class="col-md-7 col-sm-12">
                <label class="showTooltip" data-placement="left" title="Clique para copiar a URL">
                    <span class="glyphBtn articleLink "></span> <input type="text" name="link-share" class="fakeLink" value="{$link}" data-clipboard-text="{$link}" data-toggle="tooltip" id="linkShare" />
                </label>
            </div>
        </div>    
    </xsl:template>
    
    <xsl:template match="issn">
        <div>
            <span><xsl:apply-templates select="@pub-type"></xsl:apply-templates> <xsl:value-of select="."/></span>
        </div>
    </xsl:template>
    
    <xsl:template match="article" mode="front-issn">
        <div class="col-md-4 col-sm-6 right">
            <xsl:apply-templates select=".//journal-meta//issn"></xsl:apply-templates>
        </div>
    </xsl:template>
    
    <xsl:template match="article" mode="front-link-group">
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
                <xsl:apply-templates select="." mode="front-affiliations"></xsl:apply-templates>
                <div class="rowBlock">
                    <a href=""><span class="glyphBtn scientiLogo"></span> Curriculum ScienTI</a>
                    <!-- FIXME: Curriculum ScienTI -->
                </div>
                <xsl:apply-templates select="." mode="front-author-notes"></xsl:apply-templates>
            </div>
            <xsl:apply-templates select="." mode="front-licenses"></xsl:apply-templates>
        </div>
    </xsl:template>
    
    <xsl:template match="article" mode="front-licenses">
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
    
    <xsl:template match="article" mode="front-share-etc">
        <div class="col-md-3 col-sm-4 functionsBlock">
            <xsl:apply-templates select="." mode="front-share"></xsl:apply-templates>
            <xsl:apply-templates select="." mode="front-versions"></xsl:apply-templates>
            <xsl:apply-templates select="." mode="front-translations"></xsl:apply-templates>
            <xsl:apply-templates select="." mode="front-similar"></xsl:apply-templates>
        </div>
    </xsl:template>
    
    <xsl:template match="article" mode="front-share">
        <!-- FIXME: Compartilhe -->
        <div class="share">
            <a href="javascript:window.print();" class="sharePrint showTooltip" data-placement="top" title="Imprimir"><span class="glyphBtn print"></span></a>
            <a href="#" class="showTooltip" data-placement="top" title="RSS" target="blank"><span class="glyphBtn rssMini"></span></a>
            <span class="divisor"></span>
            <xsl:apply-templates select="." mode="labels-share"/>
            <a href="" class="sendViaMail showTooltip" data-placement="top" title="Enviar link por e-mail"><span class="glyphBtn sendMail"></span></a>
            <a href="" class="shareFacebook showTooltip" data-placement="top" title="Compartilhar no Facebook"><span class="glyphBtn facebook"></span></a>
            <a href="" class="shareTwitter showTooltip" data-placement="top" title="Compartilhar no Twitter"><span class="glyphBtn twitter"></span></a>
            <a href="" class="showTooltip dropdown-toggle" data-toggle="dropdown" data-placement="top" title="Outras redes sociais"><span class="glyphBtn otherNetworks"></span></a>
            <ul class="dropdown-menu">
                <li class="dropdown-header">Outras redes sociais</li>
                <li><a href="" class="shareGooglePlus"><span class="glyphBtn googlePlus"></span> Google+</a></li>
                <li><a href="" class="shareLinkedIn"><span class="glyphBtn linkedIn"></span> LinkedIn</a></li>
                <li><a href="" class="shareReddit"><span class="glyphBtn reddit"></span> Reddit</a></li>
                <li><a href="" class="shareStambleUpon"><span class="glyphBtn stambleUpon"></span> StambleUpon</a></li>
                <li><a href="" class="shareCiteULike"><span class="glyphBtn citeULike"></span> CiteULike</a></li>
                <li><a href="" class="shareMendeley"><span class="glyphBtn mendeley"></span> Mendeley</a></li>
            </ul>
        </div>
    </xsl:template>
    
    <xsl:template match="article" mode="front-versions">
        <!-- FIXME: Versões -->
        <div class="collapseBlock">
            <a href="javascript:;" class="collapseTitle">
                <span class="glyphBtn versionIcon"></span> Versões
                <span class="glyphBtn collapseIcon opened"></span>
            </a>
            <div class="collapseContent">
                <ul>
                    <li><a href="">Texto em inglês</a></li>
                    <li><a href="">Texto em espanhol</a></li>
                </ul>
            </div>
        </div>
    </xsl:template>
    
    <xsl:template match="article" mode="front-translations">
        <!-- FIXME: translations -->
        <div class="collapseBlock">
            <a href="javascript:;" class="collapseTitle">
                <span class="glyphBtn translationIcon"></span> Tradução automática
                <span class="glyphBtn collapseIcon opened"></span>
            </a>
            <div class="collapseContent">
                <ul>
                    <li><a href="">Google</a></li>
                    <li><a href="">Microsoft</a></li>
                </ul>
            </div>
        </div>
    </xsl:template>
    
    <xsl:template match="article" mode="front-similar">
        <!-- FIXME: similar -->
        <div class="collapseBlock">
            <a href="javascript:;" class="collapseTitle">
                <span class="glyphBtn similarIcon"></span> Artigos similares
                <span class="glyphBtn collapseIcon opened"></span>
            </a>
            <div class="collapseContent">
                <ul>
                    <li><a href="">SciELO</a></li>
                    <li><a href="">Google Scholar</a></li>
                </ul>
            </div>
        </div>	
    </xsl:template>
</xsl:stylesheet>