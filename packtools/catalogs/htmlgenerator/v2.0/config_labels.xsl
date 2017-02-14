<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:variable name="INTERFACE_TEXTS"></xsl:variable>
    <xsl:template match="*" mode="interface">
        <xsl:param name="text"></xsl:param>
        <xsl:choose>
            <xsl:when test="$INTERFACE_TEXTS!=''">
                <xsl:value-of select="$INTERFACE_TEXTS[$text]"/>
            </xsl:when>
            <xsl:otherwise><xsl:value-of select="$text"/></xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template match="*" mode="labels-license-view">
        Veja as permissões desta licença
    </xsl:template>
    <xsl:template match="*" mode="labels-share">
        Compartilhe
    </xsl:template>
    <xsl:variable name="INTERFACE_CLICK_TO_COPY_URL">
        Clique para copiar a URL
    </xsl:variable>
    <xsl:variable name="INTERFACE_COPY_LINK">
        copiar link
    </xsl:variable>
    
    
</xsl:stylesheet>