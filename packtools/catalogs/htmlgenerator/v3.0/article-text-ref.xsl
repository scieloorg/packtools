<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/article-text-ref.xsl"/>

    <xsl:template match="ref-list">
        <xsl:choose>
            <xsl:when test="ref-list">
                <xsl:apply-templates select="*"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <!-- 
                    <div class="row">
                        <div class="col-md-12 col-sm-12">
                            <ol class="articleFootnotes">
                                
                            </ol>
                        </div>
                    </div>
                -->
                <div class="row">
                    <div class="col-md-12 col-sm-12">
                        <ol class="articleFootnotes">
                            <xsl:apply-templates select="." mode="ref-items"/>
                        </ol>
                    </div>
                </div>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
 
    <xsl:template match="ref">
        <!--
            <li>
                <a class="" name="1_ref"></a>
                Pellerin, R.J., Waminal, N.E. & Kim, H.H. 2019. FISH mapping of rDNA and telomeric repeats in 10 Senna species. Horticulture, Environment, and Biotechnology 60: 253-260. <a href="#refId_1">↩</a>
            </li>                                                 
        -->
        <xsl:variable name="id"><xsl:value-of select="@id"/></xsl:variable>
        
        <li>
            <xsl:apply-templates select="label"/>
            <a class="" name="{@id}_ref"/>
            <xsl:apply-templates select="mixed-citation"/>
            <xsl:if test="element-citation//pub-id[@pub-id-type='doi'] or element-citation//ext-link">
                <br/>
                <xsl:apply-templates select="element-citation//pub-id[@pub-id-type='doi']" mode="ref"></xsl:apply-templates>
                <xsl:apply-templates select="element-citation//ext-link" mode="ref"></xsl:apply-templates>
            </xsl:if>
            <xsl:if test="$article//xref[@rid=$id]">
                <a href="#refId_{@id}">↩</a>
            </xsl:if>
        </li>
    </xsl:template>
</xsl:stylesheet>