<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml" >
    
    
    <xsl:output method="html"  indent="yes" xml:space="preserve" encoding="UTF-8" omit-xml-declaration="no"></xsl:output>
    
    <xsl:include href="config_vars.xsl"/>    
    <xsl:include href="generic.xsl"/>
    
    <xsl:include href="config_lang.xsl"/>
    <xsl:include href="config_labels.xsl"/>
    
    <xsl:include href="generic_href.xsl"/>
    <xsl:include href="generic_styles.xsl"/>
    
    <xsl:include href="functions-block.xsl"/>
        
    <xsl:include href="journal-meta.xsl"/>
    
    <xsl:include href="front.xsl"/>
    <xsl:include href="front-aff.xsl"/>
    <xsl:include href="front-abstract.xsl"/>
    <xsl:include href="front-contrib.xsl"/>
    
    <xsl:include href="body.xsl"/>
    <xsl:include href="body-formula.xsl"/>
    <xsl:include href="body-table.xsl"/>
    <xsl:include href="body-fig.xsl"/>
    
    <xsl:include href="back.xsl"/>
    <xsl:include href="ref.xsl"/>
    
    <xsl:include href="frame.xsl"/>
    
    <xsl:template match="article" mode="article">
        <section class="articleCtt">
            <div class="container">
                <div class="row">
                    <div class="col-md-9 col-sm-8 articleBlock">
                        <!-- FIXME -->
                        <xsl:apply-templates select="." mode="journal-meta-bibstrip"></xsl:apply-templates>
                        <xsl:apply-templates select="." mode="lang-article-title"></xsl:apply-templates>
                        <xsl:apply-templates select=".//article-meta//article-id[@pub-id-type='doi']"></xsl:apply-templates>
                        <xsl:apply-templates select=".//article-meta//contrib-group"></xsl:apply-templates>
                        <xsl:apply-templates select="." mode="front-link-group"></xsl:apply-templates>
                    </div>
                    <xsl:apply-templates select="." mode="functions-block"></xsl:apply-templates>
                    <xsl:apply-templates select="." mode="body"></xsl:apply-templates>
                    <xsl:apply-templates select="." mode="back"></xsl:apply-templates>
                </div>
            </div>
        </section>
    </xsl:template>
</xsl:stylesheet>
