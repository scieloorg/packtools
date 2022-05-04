<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml"
    version="1.0">
    
    <xsl:template match="disp-formula">
        <xsl:variable name="id"><xsl:apply-templates select="." mode="disp-formula-id"/></xsl:variable>
        <div class="row formula" id="e{$id}">
            <a name="{$id}"></a>
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

    <xsl:template match="disp-formula/alternatives | inline-formula/alternatives">
        <xsl:choose>
            <xsl:when test="$MATH_ELEM_PREFERENCE='tex-math' and tex-math">
                <xsl:apply-templates select="tex-math" />
            </xsl:when>
            <xsl:when test="$MATH_ELEM_PREFERENCE='math' and math">
                <xsl:apply-templates select="math" />
            </xsl:when>
            <xsl:when test="$MATH_ELEM_PREFERENCE='mml:math' and mml:math">
                <xsl:apply-templates select="mml:math" />
            </xsl:when>
            <xsl:when test="tex-math and (math or mml:math)">
                <!-- obtém o primeiro -->
                <xsl:apply-templates select="*[1]" />
            </xsl:when>
            <xsl:when test="tex-math">
                <xsl:apply-templates select="tex-math" />
            </xsl:when>
            <xsl:when test="mml:math">
                <xsl:apply-templates select="mml:math" />
            </xsl:when>
            <xsl:when test="math">
                <xsl:apply-templates select="math" />
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="." mode="display-graphic"/>
            </xsl:otherwise>
        </xsl:choose>    
    </xsl:template>

    <xsl:template match="inline-formula/tex-math | inline-formula/alternatives/tex-math">
        <xsl:choose>
            <xsl:when test="contains(.,'\begin{document}') and contains(.,'\end{document}')">
                <xsl:value-of select="normalize-space(substring-after(substring-before(.,'\end{document}'),'\begin{document}'))"/>
            </xsl:when>
            <xsl:when test="starts-with(.,'\begin') and contains(.,'\end')">
                <xsl:value-of select="."/>
            </xsl:when>
            <xsl:when test="starts-with(.,'\(') and ends-with(.,'\)')">
                <xsl:value-of select="."/>
            </xsl:when>
            <xsl:when test="starts-with(.,'$') and ends-with(.,'$')">
                <xsl:value-of select="."/>
            </xsl:when>
            <xsl:otherwise>\(<xsl:value-of select="."/>\)</xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="disp-formula/tex-math | disp-formula/alternatives/tex-math">
        <span class="formula-body">
            <xsl:choose>
                <xsl:when test="contains(.,'\begin{document}') and contains(.,'\end{document}')">
                    <span>
                    <xsl:value-of select="normalize-space(substring-after(substring-before(.,'\end{document}'),'\begin{document}'))"/></span>
                </xsl:when>
                <xsl:when test="starts-with(.,'\begin') and contains(.,'\end')">
                    <xsl:value-of select="."/>
                </xsl:when>
                <xsl:when test="starts-with(.,'\[') and ends-with(.,'\]')">
                    <xsl:value-of select="."/>
                </xsl:when>
                <xsl:when test="starts-with(.,'$$') and ends-with(.,'$$')">
                    <xsl:value-of select="."/>
                </xsl:when>
                <xsl:otherwise>\[<xsl:value-of select="."/>\]</xsl:otherwise>
            </xsl:choose>
        </span>
    </xsl:template>
    
</xsl:stylesheet>