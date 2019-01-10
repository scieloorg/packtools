<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    
    <xsl:template match="article" mode="text-fn">  
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//body//*[(fn or fn-group) and name()!='table-wrap-foot']">
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//body" mode="text-fn"/>
            </xsl:when>
            <xsl:when test="body//*[(fn or fn-group) and name()!='table-wrap-foot']">
                <xsl:apply-templates select="./body" mode="text-fn"/>
            </xsl:when>
        </xsl:choose>            
    </xsl:template>
    
    <xsl:template match="body" mode="text-fn">
        <div class="articleSection">
            <h2></h2>
            <div class="ref-list">
                <ul class="refList footnote"> 
                    <!--
                    <xsl:comment> body note </xsl:comment>
                    -->
                    <xsl:apply-templates select=".//*[(fn or fn-group) and name()!='table-wrap-foot']/*[contains(name(),'fn')]" mode="display-body-footnotes"></xsl:apply-templates>
                </ul>
            </div>
        </div>        
    </xsl:template>
    
    <xsl:template match="fn/label">
        <xsl:choose>
            <xsl:when test="string-length(normalize-space(text())) &gt; 3">
                <h3><span class="xref big"><xsl:apply-templates select="*|text()"></xsl:apply-templates></span></h3>
            </xsl:when>
            <xsl:otherwise>
                <span class="xref big"><xsl:apply-templates select="*|text()"></xsl:apply-templates></span>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="fn/p">
        <div>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </div>
    </xsl:template>
    
    <xsl:template match="body//*[(fn or fn-group) and name()!='table-wrap-foot']/fn | body//*[(fn or fn-group) and name()!='table-wrap-foot']/fn-group">
        <!--
        <xsl:comment> skip p/fn </xsl:comment>
        -->
    </xsl:template>
    
    <xsl:template match="*" mode="display-body-footnotes">
    </xsl:template>
    
    <xsl:template match="fn|fn-group" mode="display-body-footnotes">
        <!--
        <xsl:comment> list body//fn </xsl:comment>
        -->
        <li>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </li>
    </xsl:template>
    
    <xsl:template match="back/fn | back/fn-group" mode="back-section-content">
            <div class="ref-list">
                <ul class="refList footnote">
                    <xsl:apply-templates select="*[name()!='title']|text()"></xsl:apply-templates>
                </ul>
            </div>
    </xsl:template>
    
    <xsl:template match="back/fn-group/fn">
        <li>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </li>
    </xsl:template>
    
    <xsl:template match="fn-group/fn/title">
        <h2><xsl:apply-templates select="*|text()"></xsl:apply-templates></h2>        
    </xsl:template>
        
</xsl:stylesheet>
