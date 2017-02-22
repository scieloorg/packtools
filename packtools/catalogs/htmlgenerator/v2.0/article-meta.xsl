<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    >
    <xsl:template match="article" mode="article-meta-title">
        <xsl:apply-templates select=".//article-meta//article-title"></xsl:apply-templates>
    </xsl:template>
    <xsl:template match="*" mode="article-meta-doi">
        <xsl:apply-templates select=".//article-meta//article-id[@pub-id-type='doi']"></xsl:apply-templates>        
    </xsl:template>
   
    <xsl:template match="article-id[@pub-id-type='doi']">
        <xsl:variable name="link">https://doi.org/<xsl:value-of select="."/></xsl:variable>
        <span>DOI: <span class="doi"><xsl:value-of select="."/></span></span>
        <label class="showTooltip" data-placement="left">
            <xsl:attribute name="title"><xsl:apply-templates select="." mode="interface"><xsl:with-param name="text">Clique para copiar a URL</xsl:with-param></xsl:apply-templates></xsl:attribute>
            <span class="glyphBtn articleLink hidden-sm hidden-md"></span> <input type="text" name="link-share" class="fakeLink" data-clipboard-text="{$link}" data-toggle="tooltip" id="linkShare" >
                <xsl:attribute name="value"><xsl:apply-templates select="." mode="interface"><xsl:with-param name="text">copiar link</xsl:with-param></xsl:apply-templates></xsl:attribute>
            </input>
        </label>
    </xsl:template>
    
    <xsl:template match="article" mode="issue-meta-pub-dates">
        <xsl:choose>
            <xsl:when test=".//article-meta/pub-date[@pub-type='collection']">
                <xsl:apply-templates  select=".//article-meta/pub-date[@pub-type='collection']"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test=".//article-meta/pub-date[@pub-type='ppub']">
                <xsl:apply-templates  select=".//article-meta/pub-date[@pub-type='ppub']"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test=".//article-meta/pub-date[@pub-type='ppub-epub']">
                <xsl:apply-templates  select=".//article-meta/pub-date[@pub-type='ppub-epub']"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test=".//article-meta/pub-date[@pub-type='epub-ppub']">
                <xsl:apply-templates  select=".//article-meta/pub-date[@pub-type='epub-ppub']"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates  select=".//article-meta/pub-date"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="article" mode="article-meta-pub-dates">
        <xsl:apply-templates select=".//article-meta/pub-date[1]" mode="label"></xsl:apply-templates>&#160;
        
        <xsl:choose>
            <xsl:when test=".//article-meta/pub-date[@pub-type='epub']">
                <xsl:apply-templates  select=".//article-meta/pub-date[@pub-type='epub']"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates  select=".//article-meta/pub-date"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="article-meta/pub-date">
        <xsl:choose>
            <xsl:when test="season">
                <xsl:apply-templates select="season"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test="day">
                <xsl:apply-templates select="month" mode="label"></xsl:apply-templates>
                <xsl:text> </xsl:text>
                <xsl:apply-templates select="day"></xsl:apply-templates>, 
            </xsl:when>
            <xsl:otherwise><xsl:apply-templates select="month" mode="label"></xsl:apply-templates></xsl:otherwise>
        </xsl:choose>
        <xsl:text> </xsl:text>
        <xsl:apply-templates select="year"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="article" mode="article-meta-license">
        <!-- FIXME -->
        <img src="../static/img/cc-license-small.png" alt="Creative Common - BY | NC"/>
    </xsl:template>
    
    
</xsl:stylesheet>