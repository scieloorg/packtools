<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml" >
    
    <xsl:param name="article_lang" />
    <xsl:param name="is_translation" />
    <xsl:param name="issue_label" />
    <xsl:param name="styles_css_path" />
    <xsl:param name="CSS_PATH">/Users/roberta.takenaka/Downloads/SciELO-prototipo-15-05-13/static/css</xsl:param>
    <xsl:param name="JS_PATH">/Users/roberta.takenaka/Downloads/SciELO-prototipo-15-05-13/static/js</xsl:param>
    
    <xsl:output method="html" indent="yes" encoding="UTF-8" omit-xml-declaration="no" standalone="yes"  ></xsl:output>
    
    <xsl:include href="generic.xsl"/>
    <xsl:include href="frame.xsl"/>
    <xsl:include href="lang.xsl"/>
    <xsl:include href="front.xsl"/>
    <xsl:include href="abstract.xsl"/>
    
    <xsl:template match="article" mode="article">
        <section class="articleCtt">
            <div class="container">
                <div class="row">
                    <div class="col-md-9 col-sm-8 articleBlock">
                        <!-- FIXME -->
                        <div class="row editionMeta">
                            <div class="col-md-8 col-sm-6">
                                <span>Braz J Med Biol Res vol.46 no.1 Ribeirão Preto Jan. 2013 Epub Jan 11, 2013</span>
                            </div>
                            <xsl:apply-templates select=".//journal-meta//issn"></xsl:apply-templates>
                        </div>
                        <xsl:apply-templates select="." mode="article-title"></xsl:apply-templates>
                        <xsl:apply-templates select=".//article-meta//article-id[@pub-id-type='doi']"></xsl:apply-templates>
                        
                    </div>
                </div>
            </div>
        </section>
    </xsl:template>
    
    <xsl:template match="issn">
        <div class="col-md-4 col-sm-6 right">
            <span><xsl:apply-templates select="@pub-type"></xsl:apply-templates> <xsl:value-of select="."/></span>
        </div>
    </xsl:template>
   
   
</xsl:stylesheet>
