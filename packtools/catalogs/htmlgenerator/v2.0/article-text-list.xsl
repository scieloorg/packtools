<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink" >
    
    <xsl:template match="*" mode="list-item">
        <li>
            <xsl:apply-templates/>
        </li>
    </xsl:template>
    
    <xsl:template match="*" mode="list-item">
        <li>
            <xsl:apply-templates select="."></xsl:apply-templates>
        </li>
    </xsl:template>
    
    <xsl:template match="list">
        <xsl:param name="position"></xsl:param>
        <xsl:choose>
            <xsl:when test="@list-type!='bullet'">
                <ol>
                    <xsl:apply-templates select="@*|*">
                        <xsl:with-param name="position" select="position()"></xsl:with-param>
                    </xsl:apply-templates>
                </ol>
            </xsl:when>
            <xsl:otherwise>
                <ul>
                    <xsl:apply-templates select="@*|*">
                        <xsl:with-param name="position" select="position()"></xsl:with-param>
                    </xsl:apply-templates>
                </ul>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="@list-type">
        <!-- 1|a|A|i|I -->
        <xsl:attribute name="type">
            <xsl:choose>
                <xsl:when test=".='roman-lower'">i</xsl:when>
                <xsl:when test=".='roman-upper'">I</xsl:when>
                <xsl:when test=".='alpha-lower'">a</xsl:when>
                <xsl:when test=".='alpha-upper'">A</xsl:when>
                <xsl:otherwise>1</xsl:otherwise>                
            </xsl:choose>
        </xsl:attribute>
    </xsl:template>
    
    <xsl:template match="list-item">
        <xsl:param name="position"></xsl:param>
        
        <li>
            <xsl:apply-templates select="*|text()">
                <xsl:with-param name="position" select="position()"></xsl:with-param>
            </xsl:apply-templates>
        </li>
    </xsl:template>
    
    
</xsl:stylesheet>