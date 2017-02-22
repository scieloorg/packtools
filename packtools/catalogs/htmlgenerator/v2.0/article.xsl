<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml" >
    
    
    <xsl:output method="html"  indent="yes"  encoding="UTF-8" omit-xml-declaration="no"></xsl:output>
    
    <xsl:include href="config_vars.xsl"/>  
    
    <xsl:variable name="document" select="./article"/>
    <xsl:include href="generic.xsl"/>
    
    <xsl:include href="config_lang.xsl"/>
    <xsl:include href="config_labels.xsl"/>
    
    <xsl:include href="generic_href.xsl"/>
    <xsl:include href="generic_styles.xsl"/>
    
    <xsl:include href="functions-block.xsl"/>
        
    <xsl:include href="journal-meta.xsl"/>
    <xsl:include href="article-meta.xsl"/>
    <xsl:include href="article-meta-contrib.xsl"/>
    
    <xsl:include href="article-meta-aff.xsl"/>
    <xsl:include href="article-meta-abstract.xsl"/>
    
    <xsl:include href="text.xsl"/>
    <xsl:include href="text-formula.xsl"/>
    <xsl:include href="text-table.xsl"/>
    <xsl:include href="text-fig.xsl"/>
    
    <xsl:include href="text-back.xsl"/>
    <xsl:include href="text-ref.xsl"/>
    <xsl:include href="modals.xsl"/>
    
    <xsl:include href="frame.xsl"/>
    
    <xsl:template match="article" mode="article">
        <section class="articleCtt">
            <div class="container">
                <div class="articleTxt">
                    <div class="editionMeta">
                        <span>
                            <xsl:apply-templates select="." mode="journal-meta-bibstrip-title"></xsl:apply-templates>
                            <xsl:text> </xsl:text>
                            <xsl:apply-templates select="." mode="journal-meta-bibstrip-issue"></xsl:apply-templates>
                            <!-- FIXME location --> 
                            <xsl:apply-templates select="." mode="issue-meta-pub-dates"></xsl:apply-templates>
                        </span>
                        <xsl:text> </xsl:text>
                        <xsl:apply-templates select="." mode="journal-meta-issn"></xsl:apply-templates>
                    </div>
                    <h1 class="article-title">
                        <xsl:apply-templates select="." mode="article-meta-title"></xsl:apply-templates>
                    </h1>
                    <div class="articleMeta">
                        <div>
                            <!-- FIXME -->
                            <xsl:apply-templates select="." mode="article-meta-pub-dates"></xsl:apply-templates> - 
                            <xsl:apply-templates select="." mode="article-meta-license"></xsl:apply-templates>
                        </div>
                        <div>
                            <xsl:apply-templates select="." mode="article-meta-doi"></xsl:apply-templates>
                        </div>
                    </div>
                        
                    <xsl:apply-templates select="." mode="article-meta-contrib"></xsl:apply-templates>
                    
                    <div class="row">
                        <ul class="col-md-2 hidden-sm articleMenu">
                            <xsl:comment> </xsl:comment>
                        </ul>
                        
                    <xsl:apply-templates select="." mode="text"></xsl:apply-templates>
                    </div>
                </div>
            </div>
        </section>
    </xsl:template>
</xsl:stylesheet>
