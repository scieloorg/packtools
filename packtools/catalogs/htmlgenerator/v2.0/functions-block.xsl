<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="article" mode="functions-block">
        <div class="col-md-3 col-sm-4 functionsBlock">
            <xsl:apply-templates select="." mode="functions-block-share"></xsl:apply-templates>
            <xsl:apply-templates select="." mode="functions-block-versions"></xsl:apply-templates>
            <xsl:apply-templates select="." mode="functions-block-translations"></xsl:apply-templates>
            <xsl:apply-templates select="." mode="functions-block-similar"></xsl:apply-templates>
        </div>
    </xsl:template>
    
    <xsl:template match="article" mode="functions-block-share">
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
    
    <xsl:template match="article" mode="functions-block-versions">
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
    
    <xsl:template match="article" mode="functions-block-translations">
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
    
    <xsl:template match="article" mode="functions-block-similar">
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