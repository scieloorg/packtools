<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/generic-pub-date.xsl"/>

    <xsl:template match="article-meta | sub-article | response" mode="generic-pub-date">
       <xsl:if test=".//pub-date">
        <!-- manter pareado class="articleSection" e data-anchor="nome da seção no menu esquerdo" -->
        <div class="articleSection">
             <xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="text-labels">
                 <xsl:with-param name="text">Publication Dates</xsl:with-param>
             </xsl:apply-templates></xsl:attribute>
             <h2 class="h5"><xsl:apply-templates select="." mode="text-labels">
                 <xsl:with-param name="text">Publication Dates</xsl:with-param>
             </xsl:apply-templates></h2>
             <div class="row">
                 <div class="col-md-12 col-sm-12">
                     <ul class="articleTimeline">
                         <xsl:apply-templates select="." mode="generic-pub-date-publication-date"></xsl:apply-templates>
                         <xsl:apply-templates select="." mode="generic-pub-date-collection-date"></xsl:apply-templates>
                     </ul>
                 </div>
             </div>
         </div>
       </xsl:if>
    </xsl:template>

</xsl:stylesheet>