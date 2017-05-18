<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    
    <xsl:template match="ref-list" mode="back-section-content">
        <xsl:apply-templates select="."></xsl:apply-templates>
    </xsl:template>
   
    <xsl:template match="ref-list">
        <xsl:choose>
            <xsl:when test="ref-list">
                <xsl:apply-templates select="*"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <div class="row">
                    <div class="col-md-12 col-sm-12 ref-list">
                        <ul class="refList">
                            <xsl:apply-templates select="." mode="ref-items"></xsl:apply-templates>
                        </ul>
                    </div>
                </div>   
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="ref-list" mode="ref-items">
        <xsl:apply-templates select="ref"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="sub-article[@article-type='translation']/back//ref-list[ref]" mode="ref-items">
        <xsl:apply-templates select="$article/back/ref-list/ref"/>
    </xsl:template>
    
    <xsl:template match="sub-article[@article-type='translation']/response/back//ref-list[ref]" mode="ref-items">
        <xsl:apply-templates select="$article/response/back/ref-list/ref"/>
    </xsl:template>
    
    <xsl:template match="ref">
        <xsl:if test="not(contains(.,'-'))">
            <xsl:comment>  
                <xsl:apply-templates select="mixed-citation"/> ??? 
            </xsl:comment>
        </xsl:if>
        
        <li>
            <xsl:if test="label">
                <xsl:apply-templates select="label"></xsl:apply-templates>
            </xsl:if>            
            <div>
                <xsl:choose>
                    <xsl:when test="mixed-citation[*]">
                        <xsl:apply-templates select="mixed-citation"/>
                    </xsl:when>
                    <xsl:otherwise><xsl:apply-templates select="mixed-citation"/></xsl:otherwise>
                </xsl:choose>
            </div>
        </li>
    </xsl:template>
    
    <xsl:template match="mixed-citation[*]/text() | mixed-citation[not(*)]/text()">
        <xsl:if test="position()=1">
            <xsl:if test="not(contains(.,'-'))">
                <xsl:comment> 
                    <xsl:value-of select="."/>  ???                 
                </xsl:comment>
            </xsl:if>
        </xsl:if>
        <xsl:variable name="label">
            <xsl:if test="position()=1">
                <xsl:choose>
                    <xsl:when test="starts-with(.,concat(../../label,'.'))">
                        <xsl:value-of select="concat(../../label,'.')"/>
                    </xsl:when>
                    <xsl:when test="starts-with(.,concat(../../label,' .'))">
                        <xsl:value-of select="concat(../../label,' .')"/>
                    </xsl:when>
                    <xsl:when test="starts-with(.,../../label)">
                        <xsl:value-of select="../../label"/>
                    </xsl:when>
                </xsl:choose>
            </xsl:if>
        </xsl:variable>
        <xsl:choose>
            <xsl:when test="normalize-space($label)!=''"><xsl:value-of select="substring-after(.,$label)"/></xsl:when>
            <xsl:when test="starts-with(.,'.')"><xsl:value-of select="substring-after(.,'.')"/></xsl:when>
            <xsl:otherwise><xsl:value-of select="."/></xsl:otherwise>
        </xsl:choose> 
    </xsl:template>
    
    <xsl:template match="ref/label">
        <sup class="xref big"><xsl:value-of select="."/></sup>
    </xsl:template>
    
    <xsl:template match="ref" mode="url">
        <xsl:choose>
            <xsl:when test=".//ext-link"><xsl:value-of select=".//ext-link[1]"/></xsl:when>
            <xsl:when test=".//pub-id[@pub-id-type='doi']">https://doi.org/<xsl:value-of select=".//pub-id[@pub-id-type='doi']"/></xsl:when>
            <xsl:when test=".//comment[starts-with(.,'http')]"><xsl:value-of select=".//comment[starts-with(.,'http')]"/></xsl:when>
            <xsl:when test=".//comment[contains(.,'doi:')]">https://doi.org/<xsl:value-of select="normalize-space(substring-after(.//comment[contains(.,'doi:')],'doi:'))"/></xsl:when>
            <xsl:when test=".//comment[contains(.,'DOI:')]">https://doi.org/<xsl:value-of select="normalize-space(substring-after(.//comment[contains(.,'DOI:')],'DOI:'))"/></xsl:when>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="mixed-citation//ext-link">
        <xsl:apply-templates select="*|text()"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="ref" mode="table-wrap-foot">
        <xsl:if test="not(contains(.,'-'))">        <xsl:comment>  
            <xsl:apply-templates select="mixed-citation"/> ??? 
        </xsl:comment>
        </xsl:if>
        
        <li>
            <sup class="xref xrefblue big"><xsl:value-of select="label"></xsl:value-of></sup>
            <div>
                <xsl:choose>
                    <xsl:when test="mixed-citation[*]">
                        <xsl:apply-templates select="mixed-citation"/>
                    </xsl:when>
                    <xsl:otherwise><xsl:apply-templates select="mixed-citation"/></xsl:otherwise>
                </xsl:choose>
            </div>
        </li>
    </xsl:template>
</xsl:stylesheet>