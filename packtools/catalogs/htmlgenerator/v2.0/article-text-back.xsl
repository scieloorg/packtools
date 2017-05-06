<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    
    <xsl:template match="*" mode="position">
        <xsl:param name="name"></xsl:param>
        <xsl:if test="name()=$name"><xsl:value-of select="position()"/></xsl:if>
    </xsl:template>
    
    <xsl:template match="*" mode="previous">
        <xsl:apply-templates select="preceding-sibling::node()[1]" mode="node-name"/>
    </xsl:template>
    
    <xsl:template match="*" mode="next">
        <xsl:apply-templates select="following-sibling::node()[1]" mode="node-name"/>
    </xsl:template>
    
    <xsl:template match="*" mode="node-name"><xsl:value-of select="name()"/></xsl:template>

    <xsl:template match="article" mode="text-back">
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG]">
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG]/back/*" mode="back"/>
                <xsl:if test="count(.//sub-article[@xml:lang=$TEXT_LANG]/back/*) &lt; $reflist_position">
                    <xsl:apply-templates select="$article/back/ref-list" mode="back-section">
                        <xsl:with-param name="position"><xsl:value-of select="$reflist_position"/></xsl:with-param>
                    </xsl:apply-templates>
                </xsl:if>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="./back/*" mode="back"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>        
    </xsl:template>
    
    <xsl:template match="back/*[title]" mode="index">
        <xsl:param name="title"/>
        <xsl:if test="normalize-space(title)=normalize-space($title)"><xsl:value-of select="position()"/></xsl:if>
    </xsl:template>
    
    <xsl:template match="back" mode="index">
        <xsl:param name="title"/>
        <xsl:variable name="index"><xsl:apply-templates select=".//*[title]" mode="index">
            <xsl:with-param name="title"><xsl:value-of select="$title"/></xsl:with-param>
        </xsl:apply-templates></xsl:variable>
        <xsl:choose>
            <xsl:when test="$reflist_position != '' and ref-list">
                <xsl:value-of select="$index"/>
            </xsl:when>
            <xsl:when test="$reflist_position != '' and not(ref-list)">
                <xsl:choose>
                    <xsl:when test="$index &lt; $reflist_position">
                        <xsl:value-of select="$index"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="$index+1"/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:when>
        </xsl:choose>        
    </xsl:template>
    
    <xsl:template match="*" mode="back">
        <xsl:comment> mode="back" </xsl:comment>
        <xsl:comment> <xsl:value-of select="name()"/> </xsl:comment>
        <xsl:apply-templates select="." mode="back-section">
            <xsl:with-param name="position"><xsl:value-of select="position()"/></xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="sub-article[@article-type='translation']/back[not(ref-list)]/*" mode="back">
        <xsl:comment> sub-article/*, mode="back" </xsl:comment>
        <xsl:comment> position()=<xsl:value-of select="position()"/> </xsl:comment>
        <xsl:comment> ref-list position()=<xsl:value-of select="$reflist_position"/> </xsl:comment>
        <xsl:if test="position()=$reflist_position">
            <xsl:apply-templates select="$article/back/ref-list" mode="back-section">
                <xsl:with-param name="position"><xsl:value-of select="position()"/></xsl:with-param>
            </xsl:apply-templates>
        </xsl:if>
         <xsl:apply-templates select="." mode="back-section">
            <xsl:with-param name="position"><xsl:choose>
                <xsl:when test="position() &gt;= number($reflist_position)"><xsl:value-of select="position() + 1"/></xsl:when>
                <xsl:otherwise><xsl:value-of select="position()"></xsl:value-of></xsl:otherwise>
            </xsl:choose></xsl:with-param>
         </xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="*" mode="back-section">
        <xsl:param name="position"></xsl:param>
        <xsl:comment> mode="back-section" </xsl:comment>
        <xsl:comment> <xsl:value-of select="name()"/> </xsl:comment>
        <xsl:comment> title=<xsl:apply-templates select="title//text()"/> </xsl:comment>
        <xsl:comment> title=<xsl:value-of select="title"/> </xsl:comment>
        
        <xsl:variable name="index"><xsl:if test="title"><xsl:apply-templates select="../../back" mode="index">
            <xsl:with-param name="title"><xsl:value-of select="title"/></xsl:with-param>
        </xsl:apply-templates></xsl:if></xsl:variable>
        <xsl:comment> index: <xsl:value-of select="$index"/> </xsl:comment>
        <xsl:if test="$index!=''">
            <a name="articleSection{$q_front+number($index)}"/>
        </xsl:if>
        
        <div class="articleSection">
            <xsl:if test="title">
                <xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="title"></xsl:apply-templates></xsl:attribute>    
            </xsl:if>
            <div class="row">
                <div class="col-md-12 col-sm-12">                    
                    <h1>
                        <xsl:if test="title"><xsl:apply-templates select="." mode="title"/></xsl:if>
                    </h1>
                </div>
            </div>
            <xsl:apply-templates select="." mode="back-section-content"></xsl:apply-templates>
        </div>
    </xsl:template>
    
    <xsl:template match="*" mode="back-section-content">
        <xsl:apply-templates select="*[name()!='title' and name()!='label'] | text()"></xsl:apply-templates>
    </xsl:template>
    
</xsl:stylesheet>