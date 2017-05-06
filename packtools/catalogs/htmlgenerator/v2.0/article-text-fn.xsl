<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    
    <xsl:template match="article" mode="text-fn">  
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG]//body//*[(fn or fn-group) and name()!='table-wrap-foot']">
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG]//body" mode="text-fn"/>
            </xsl:when>
            <xsl:when test="body//*[(fn or fn-group) and name()!='table-wrap-foot']">
                <xsl:apply-templates select="./body" mode="text-fn"/>
            </xsl:when>
        </xsl:choose>            
    </xsl:template>
    <xsl:template match="body" mode="text-fn">
        <div class="articleSection">
            <!--xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="title"/></xsl:attribute-->
            <!--a name="articleSection{$q_front + $q_back + 1}"></a-->
            <div class="row">
                <div class="col-md-12 col-sm-12">
                    <h1><!--xsl:apply-templates select="." mode="title"/--></h1>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12 col-sm-12">
                    <ul class="refList footnote"> 
                        <xsl:comment> body note </xsl:comment>
                        <xsl:apply-templates select=".//*[(fn or fn-group) and name()!='table-wrap-foot']/*[contains(name(),'fn')]" mode="display-body-footnotes"></xsl:apply-templates>
                    </ul>
                </div>
            </div>
        </div>        
    </xsl:template>
    
    <xsl:template match="fn/label">
        <span class="xref big"><xsl:apply-templates select="*|text()"></xsl:apply-templates></span>
    </xsl:template>
    
    <xsl:template match="fn/p">
        <div>
            <p>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
            </p>
        </div>
    </xsl:template>
    
    <xsl:template match="body//*[(fn or fn-group) and name()!='table-wrap-foot']/fn | body//*[(fn or fn-group) and name()!='table-wrap-foot']/fn-group">
        <xsl:comment> skip p/fn </xsl:comment>
    </xsl:template>
    
    <xsl:template match="*" mode="display-body-footnotes">
    </xsl:template>
    
    <xsl:template match="fn|fn-group" mode="display-body-footnotes">
        <xsl:comment> list body//fn </xsl:comment>
        <li>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </li>
    </xsl:template>
    
    <xsl:template match="back/fn" mode="back-section-content">
        <div class="row">
            <div class="col-md-12 col-sm-12">                
                <ul class="refList footnote">
                    <xsl:apply-templates select="." mode="list-item"></xsl:apply-templates>
                </ul>
            </div>
        </div>
        
    </xsl:template>
    
    <xsl:template match="back/fn-group" mode="back-section-content">
        <div class="row">
            <div class="col-md-12 col-sm-12">                
                <ul class="refList footnote">
                    <xsl:apply-templates select="*[name()!='title']|text()"></xsl:apply-templates>
                </ul>
            </div>
        </div>
    </xsl:template>
    
    
</xsl:stylesheet>