<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">

    <xsl:template match="*" mode="position">
        <xsl:param name="name"></xsl:param>
        <xsl:if test="name()=$name"><xsl:value-of select="position()"/></xsl:if>
    </xsl:template>
    
    <xsl:template match="sec[@sec-type]" mode="index">
        <xsl:param name="sectype"/>
        <xsl:if test="@sec-type=$sectype"><xsl:value-of select="number(position()-1)"/></xsl:if>
    </xsl:template>
    
    <xsl:template match="body" mode="index">
        <xsl:param name="sectype"/>
        <xsl:apply-templates select=".//sec[@sec-type]" mode="index">
            <xsl:with-param name="sectype"><xsl:value-of select="$sectype"/></xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="back/*" mode="index">
        <xsl:param name="title"/>
        <xsl:if test="title">
            <xsl:if test="normalize-space(title)=normalize-space($title)"><xsl:value-of select="position()"/></xsl:if>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="back" mode="index">
        <xsl:param name="title"/>
        
        <xsl:if test="$title!=''">
            <xsl:variable name="index"><xsl:apply-templates select="*[title]" mode="index">
                <xsl:with-param name="title"><xsl:value-of select="$title"/></xsl:with-param>
            </xsl:apply-templates></xsl:variable>
            <xsl:choose>
                <xsl:when test="ref-list">
                    <xsl:value-of select="$index"/>
                </xsl:when>
                <xsl:when test="not(ref-list) and $REFLIST_INDEX!=''">
                    <xsl:choose>
                        <xsl:when test="$index &lt; $REFLIST_INDEX">
                            <xsl:value-of select="$index"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:value-of select="$index+1"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="$index"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:if>
    </xsl:template>
    
</xsl:stylesheet>