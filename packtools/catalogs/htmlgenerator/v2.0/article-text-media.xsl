<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">
    
    <xsl:template match="media">
        <xsl:variable name="location"><xsl:value-of select="@xlink:href"></xsl:value-of></xsl:variable>
        <xsl:variable name="s"><xsl:value-of select="substring($location,string-length($location)-3)"/></xsl:variable>
        <xsl:variable name="ext"><xsl:if test="contains($s,'.')">.<xsl:value-of select="substring-after($s,'.')"/></xsl:if></xsl:variable>
        
        <xsl:choose>
            <xsl:when test="@mimetype='video'">
                <video width="100%" controls="1">
                    <source src="{$location}" type="{@mimetype}/{@mime-subtype}"/>
                    Your browser does not support the video element.
                </video>
            </xsl:when>
            <xsl:when test="@mimetype='audio'">
                <audio width="100%" controls="1">
                    <source src="{$location}" type="{@mimetype}/{@mime-subtype}"/>
                    Your browser does not support the audio element.
                </audio>
            </xsl:when>
            <xsl:otherwise>
                <a target="_blank">
                    <xsl:attribute name="href"><xsl:value-of select="$location"/></xsl:attribute>
                    <xsl:apply-templates select="*|text()"/>
                </a>
                <embed width="100%" height="400" >
                    <xsl:attribute name="type"><xsl:value-of select="@mimetype"/>/<xsl:value-of select="@mime-subtype"/></xsl:attribute>
                    <xsl:attribute name="src"><xsl:value-of select="$location"/></xsl:attribute> 
                </embed>
            </xsl:otherwise>
        </xsl:choose>      
    </xsl:template>
    
</xsl:stylesheet>