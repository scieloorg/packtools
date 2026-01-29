<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/generic.xsl"/>

    <xsl:template match="@id" mode="add_span_id">
        <span id="{.}"/>
    </xsl:template>

    <xsl:template match="attrib">
        <small class="d-block">
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </small>
    </xsl:template>

    <xsl:template match="ext-link">
        <xsl:param name="symbol"></xsl:param>
        <xsl:choose>
            <xsl:when test="@xlink:href">
                <xsl:variable name="access_text">
                    <xsl:apply-templates select="." mode="interface">
                        <xsl:with-param name="text">access_link</xsl:with-param>
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
                <xsl:variable name="link_text">
                    <xsl:apply-templates select="*|text()"></xsl:apply-templates>
                </xsl:variable>
                <xsl:variable name="aria_label">
                    <xsl:value-of select="$access_text"/>
                    <xsl:text> </xsl:text>
                    <xsl:value-of select="$link_text"/>
                    <xsl:text>. </xsl:text>
                    <xsl:value-of select="$new_tab_text"/>
                    <xsl:text>. </xsl:text>
                    <xsl:value-of select="$external_resource_text"/>
                    <xsl:text>.</xsl:text>
                </xsl:variable>
                <a href="{@xlink:href}" target="_blank" aria-label="{normalize-space($aria_label)}">
                    <xsl:value-of select="$symbol"/>
                    <xsl:apply-templates select="*|text()"></xsl:apply-templates>
                </a>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="*|text()"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>