<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/article-text-ref.xsl"/>
    <xsl:template match="ref">
        <!--
            <a class="" name="1_ref"></a>                                
            Pellerin, R.J., Waminal, N.E. & Kim, H.H. 2019. FISH mapping of rDNA and telomeric repeats in 10 Senna species. Horticulture, Environment, and Biotechnology 60: 253-260. <a href="#refId_1">↩</a>                                                 
        -->
        <xsl:variable name="id"><xsl:value-of select="@id"/></xsl:variable>
        <a class="" name="{@id}_ref"/>
        <li>
            <xsl:if test="label">
                <xsl:apply-templates select="label"></xsl:apply-templates>
            </xsl:if>            
            <div>
                <xsl:apply-templates select="mixed-citation"/>
                <xsl:if test="element-citation//pub-id[@pub-id-type='doi'] or element-citation//ext-link">
                    <br/>
                    <xsl:apply-templates select="element-citation//pub-id[@pub-id-type='doi']" mode="ref"></xsl:apply-templates>
                    <xsl:apply-templates select="element-citation//ext-link" mode="ref"></xsl:apply-templates>
                </xsl:if>
                <xsl:if test="$article//xref[@rid=$id]">
                    <a href="#xref_{@id}">↩</a>
                </xsl:if>
            </div>
        </li>
    </xsl:template>
</xsl:stylesheet>