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
                <div class="formula-container">
                    <xsl:apply-templates select="*|text()"></xsl:apply-templates>
                </div>
            </div>
        </div>
    </xsl:template>

	<xsl:template match="disp-formula/label">
		<span class="label"><xsl:value-of select="."/></span>
	</xsl:template>

    <xsl:template match="tex-math">
        <span class="formula-body">
            <xsl:choose>
                <xsl:when test="contains(.,'\begin{document}') and contains(.,'\end{document}')">
                    <xsl:value-of select="substring-after(substring-before(.,'\end{document}'),'\begin{document}')"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="."/>
                </xsl:otherwise>
            </xsl:choose>
        </span>
    </xsl:template>
    
</xsl:stylesheet>