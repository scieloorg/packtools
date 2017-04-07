<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:variable name="prev"><xsl:apply-templates select="article/back/ref-list" mode="previous"/></xsl:variable>
    <xsl:variable name="next"><xsl:apply-templates select="article/back/ref-list" mode="next"/></xsl:variable>
    
    <xsl:template match="article/back/ref-list" mode="previous">
        <xsl:apply-templates select="preceding-sibling::node()[1]" mode="node-name"/>
    </xsl:template>
    
    <xsl:template match="article/back/ref-list" mode="next">
        <xsl:apply-templates select="following-sibling::node()[1]" mode="node-name"/>
    </xsl:template>
    
    <xsl:template match="*" mode="node-name"><xsl:value-of select="name()"/></xsl:template>
    
    <xsl:template match="ref">
        <xsl:comment>  <xsl:apply-templates select="mixed-citation"/> </xsl:comment>
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
    
    <xsl:template match="ref-list" mode="title">
        <xsl:apply-templates select="." mode="label"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="back/ref-list" mode="content">
        <div class="row">
            <div class="col-md-12 col-sm-12 ref-list">
                <ul class="refList">
                    <xsl:apply-templates select="ref"></xsl:apply-templates>
                </ul>
            </div>
        </div>        
    </xsl:template>
    
    <xsl:template match="mixed-citation[*]/text() | mixed-citation[not(*)]/text()">
        <xsl:if test="position()=1"><xsl:comment> <xsl:value-of select="."/> </xsl:comment></xsl:if>
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
    
    <xsl:template match="person-group">
        <xsl:apply-templates select="name"></xsl:apply-templates><xsl:choose>
            <xsl:when test="position()=last()">. </xsl:when>
            <xsl:otherwise>; </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template match="person-group/name">
        <xsl:apply-templates select="surname"></xsl:apply-templates>, <xsl:apply-templates select="given-names"></xsl:apply-templates>
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
    
    <xsl:template match="ref" mode="xref">
        <xsl:variable name="url"><xsl:apply-templates select="." mode="url"></xsl:apply-templates></xsl:variable>
        <xsl:choose>
            <xsl:when test="$url!=''">
                <a href="{normalize-space($url)}" target="_blank">
                    <xsl:apply-templates select="mixed-citation" mode="xref"></xsl:apply-templates>
                </a>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="mixed-citation" mode="xref"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="mixed-citation" mode="xref">
        <xsl:apply-templates select="*|text()" mode="xref"/>
    </xsl:template>
    
    <xsl:template match="mixed-citation//*" mode="xref">
        <xsl:apply-templates select="*|text()" mode="xref"/>
    </xsl:template>
    
    <xsl:template match="ext-link | pub-id | comment" mode="xref">
        <xsl:value-of select="."/>
    </xsl:template>
    
    <xsl:template match="mixed-citation//ext-link">
        <xsl:apply-templates select="*|text()"></xsl:apply-templates>
    </xsl:template>
</xsl:stylesheet>