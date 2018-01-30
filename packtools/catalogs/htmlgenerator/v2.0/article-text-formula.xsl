<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml"
    version="1.0">
    
    <xsl:template match="disp-formula">
        <div class="row formula" id="e{@id}">
            <a name="{@id}"></a>
            <div class="col-md-12">
                <xsl:apply-templates select="*|text()"></xsl:apply-templates>
            </div>
        </div>
    </xsl:template>
    
    <xsl:template match="tex-math">
        <span>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </span>
    </xsl:template>
    
</xsl:stylesheet>