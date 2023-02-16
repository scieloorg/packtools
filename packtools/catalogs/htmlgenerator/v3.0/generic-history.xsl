<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/generic-history.xsl"/>

    <xsl:template match="article-meta | sub-article | response" mode="generic-history">
       <xsl:if test=".//history">
        <div class="articleSection">
             <xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="text-labels">
                 <xsl:with-param name="text">History</xsl:with-param>
             </xsl:apply-templates></xsl:attribute>
             <h3 class="articleSectionTitle"><xsl:apply-templates select="." mode="text-labels">
                 <xsl:with-param name="text">History</xsl:with-param>
             </xsl:apply-templates></h3>
             <div class="row">
                 <div class="col-md-12 col-sm-12">
                     <ul class="articleTimeline">
                         <xsl:apply-templates select="." mode="generic-history-history-dates"></xsl:apply-templates>
                     </ul>
                 </div>
             </div>
            <xsl:apply-templates select="." mode="preprint-link-without-date-row"/>
         </div>
       </xsl:if>
    </xsl:template>
</xsl:stylesheet>