<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">

    <xsl:template match="article-meta | sub-article | response" mode="generic-pub-date">
       <xsl:if test=".//pub-date">
        <div class="articleSection">
             <xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="text-labels">
                 <xsl:with-param name="text">Publication Dates</xsl:with-param>
             </xsl:apply-templates></xsl:attribute>
             <h1 class="articleSectionTitle"><xsl:apply-templates select="." mode="text-labels">
                 <xsl:with-param name="text">Publication Dates</xsl:with-param>
             </xsl:apply-templates></h1>
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

    <xsl:template match="article-meta | sub-article | response" mode="generic-pub-date-publication-date">
        <xsl:if test="pub-date[@pub-type='epub-ppub'] or pub-date[@date-type='pub'] or pub-date[@pub-type='epub']">
                <li><strong>
                    <xsl:apply-templates select="." mode="text-labels">
                        <xsl:with-param name="text">Publication in this collection</xsl:with-param>
                    </xsl:apply-templates>
                    </strong><br/>
                    <xsl:choose>
                        <xsl:when test="pub-date[@pub-type='epub-ppub']">
                            <xsl:apply-templates select="pub-date[@pub-type='epub-ppub']"></xsl:apply-templates>
                        </xsl:when>
                        <xsl:when test="pub-date[@pub-type='epub']">
                            <xsl:apply-templates select="pub-date[@pub-type='epub']"></xsl:apply-templates>
                        </xsl:when>
                        <xsl:when test="pub-date[@date-type='pub']">
                            <xsl:apply-templates select="pub-date[@date-type='pub']"></xsl:apply-templates>
                        </xsl:when>
                    </xsl:choose>
                </li>
        </xsl:if>
    </xsl:template>

    <xsl:template match="article-meta | sub-article | response" mode="generic-pub-date-collection-date">
        <xsl:if test="pub-date[@pub-type='collection'] or pub-date[@date-type='collection']">
                <li><strong>
                    <xsl:apply-templates select="." mode="text-labels">
                        <xsl:with-param name="text">Date of issue</xsl:with-param>
                    </xsl:apply-templates></strong><br/>
                    <xsl:choose>
                        <xsl:when test="pub-date[@date-type='collection']">
                            <xsl:apply-templates select="pub-date[@date-type='collection']"></xsl:apply-templates>
                        </xsl:when>
                        <xsl:when test="pub-date[@pub-type='collection']">
                            <xsl:apply-templates select="pub-date[@pub-type='collection']"></xsl:apply-templates>
                        </xsl:when>
                    </xsl:choose>
                </li>
        </xsl:if>
    </xsl:template>


</xsl:stylesheet>