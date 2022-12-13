<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/article-meta.xsl"/>

    <xsl:template match="article-id[@pub-id-type='doi']" mode="display">
        <xsl:variable name="link">https://doi.org/<xsl:value-of select="."/></xsl:variable>
        <a href="{$link}" class="_doi" target="_blank"><xsl:value-of select="$link"/></a>
        &#160;
        <a 
            href="javascript:;"
            class="btn btn-secondary btn-sm scielo__btn-with-icon--left copyLink"
            data-clipboard-text="{$link}">
            <span class="material-icons-outlined">link</span>
            <xsl:apply-templates select="." mode="interface">
                <xsl:with-param name="text">copy</xsl:with-param>
            </xsl:apply-templates>
        </a>
    </xsl:template>
</xsl:stylesheet>