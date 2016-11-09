<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml"
    version="1.0">
    
    <xsl:template match="disp-formula">
        <a name="{@id}"></a>
        <span class="formula" id="{@id}">
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </span>
    </xsl:template>
</xsl:stylesheet>