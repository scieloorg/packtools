<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml"
    version="1.0">

    <xsl:template match="math">
        <xsl:copy-of select="."/>
    </xsl:template>

    
    <xsl:template match="mml:math">
        <!-- Remove o namespace mml para que os browser possam renderizar as fórmulas -->
        <xsl:element name="{local-name()}">
            <xsl:apply-templates select="@*|*|text()" mode="no-namespace"/>
        </xsl:element>
    </xsl:template>
    <xsl:template match="@*" mode="no-namespace">
        <xsl:attribute name="{name()}">
            <xsl:value-of select="."/>
        </xsl:attribute>
    </xsl:template>
    <xsl:template match="*" mode="no-namespace">
        <!-- Remove o namespace mml para que os browser possam renderizar as fórmulas -->
        <xsl:element name="{local-name()}">
            <xsl:apply-templates select="@*|*|text()" mode="no-namespace"/>
        </xsl:element>
    </xsl:template>
    <xsl:template match="text()" mode="no-namespace">
        <xsl:value-of select="."/>
    </xsl:template>
</xsl:stylesheet>