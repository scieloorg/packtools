<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/article-meta-permissions.xsl"/>

<xsl:template match="license">
        <xsl:variable name="url">https://licensebuttons.net/l/</xsl:variable>
        <xsl:variable name="path"><xsl:apply-templates select="." mode="license-acron-version"></xsl:apply-templates></xsl:variable>
        <xsl:variable name="icon"><xsl:value-of select="translate($path,'/',' ')"/></xsl:variable>
        
        <xsl:variable name="access_text">
            <xsl:apply-templates select="." mode="interface">
                <xsl:with-param name="text">access_license</xsl:with-param>
            </xsl:apply-templates>
        </xsl:variable>
        <xsl:variable name="new_tab_text">
            <xsl:apply-templates select="." mode="interface">
                <xsl:with-param name="text">opens_new_tab</xsl:with-param>
            </xsl:apply-templates>
        </xsl:variable>
        <xsl:variable name="external_resource_text">
            <xsl:apply-templates select="." mode="interface">
                <xsl:with-param name="text">external_resource</xsl:with-param>
            </xsl:apply-templates>
        </xsl:variable>
        <xsl:variable name="aria_label">
            <xsl:value-of select="$access_text"/>
            <xsl:text> Creative Common - </xsl:text>
            <xsl:value-of select="$icon"/>
            <xsl:text>. </xsl:text>
            <xsl:value-of select="$new_tab_text"/>
            <xsl:text>. </xsl:text>
            <xsl:value-of select="$external_resource_text"/>
            <xsl:text>.</xsl:text>
        </xsl:variable>
        
        <div class="col-sm-3 col-md-2">
            <a href="{@xlink:href}" target="_blank" aria-label="{normalize-space($aria_label)}">
                <img src="{$url}{$path}/88x31.png" alt="Creative Common - {$icon}"/>
            </a>
        </div>
        <div class="col-sm-9 col-md-10">
            <a href="{@xlink:href}" target="_blank" aria-label="{normalize-space($aria_label)}">
                <xsl:apply-templates select="license-p"/> 
            </a>
        </div>
    </xsl:template>
</xsl:stylesheet>