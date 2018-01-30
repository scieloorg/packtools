<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    
    <xsl:template match="article-meta | sub-article | response" mode="generic-history">
       <xsl:if test=".//history or front//pub-date or front-stub//pub-date">
        <div class="articleSection">
             <xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="text-labels">
                 <xsl:with-param name="text">History</xsl:with-param>
             </xsl:apply-templates></xsl:attribute>
             <h1 class="articleSectionTitle"><xsl:apply-templates select="." mode="text-labels">
                 <xsl:with-param name="text">History</xsl:with-param>
             </xsl:apply-templates></h1>
             <div class="row">
                 <div class="col-md-12 col-sm-12">
                     <ul class="articleTimeline">
                         <xsl:apply-templates select="." mode="generic-history-history-dates"></xsl:apply-templates>
                         <xsl:apply-templates select="." mode="generic-history-epub-date"></xsl:apply-templates>
                         <xsl:apply-templates select="." mode="generic-history-publication-date"></xsl:apply-templates>
                         <xsl:apply-templates select="." mode="generic-history-errata-date"></xsl:apply-templates>
                         <xsl:apply-templates select="." mode="generic-history-retraction-date"></xsl:apply-templates>
                         <xsl:apply-templates select="." mode="generic-history-manisfestation-date"></xsl:apply-templates>
                     </ul>
                 </div>
             </div>
         </div>
       </xsl:if>
    </xsl:template>
    
    <!--xsl:template match="front-stub | *[name()!='article']/front" mode="generic-history">
        <div>
            <div class="row">
                <div class="col-md-12 col-sm-12">
                    <h1><xsl:apply-templates select="." mode="text-labels">
                        <xsl:with-param name="text">History</xsl:with-param>
                    </xsl:apply-templates></h1>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12 col-sm-12">
                    <ul class="articleTimeline">
                        <xsl:apply-templates select="." mode="generic-history-history-dates"></xsl:apply-templates>
                        <xsl:apply-templates select="." mode="generic-history-epub-date"></xsl:apply-templates>
                        <xsl:apply-templates select="." mode="generic-history-publication-date"></xsl:apply-templates>
                        <xsl:apply-templates select="." mode="generic-history-errata-date"></xsl:apply-templates>
                        <xsl:apply-templates select="." mode="generic-history-retraction-date"></xsl:apply-templates>
                        <xsl:apply-templates select="." mode="generic-history-manisfestation-date"></xsl:apply-templates>
                    </ul>
                </div>
            </div>
        </div>
    </xsl:template-->
    
    <xsl:template match="article-meta" mode="generic-history-history-dates">
        <xsl:choose>
            <xsl:when test="$article//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//history">
                <xsl:apply-templates select="$article//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//history/date" mode="list-item"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="history/date" mode="generic-history-list-item"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="sub-article | response" mode="generic-history-history-dates">
        <xsl:apply-templates select=".//history/date" mode="generic-history-list-item"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="history/date" mode="generic-history-list-item">
        <li><strong><xsl:apply-templates select="." mode="generated-label"></xsl:apply-templates></strong><br/> <xsl:apply-templates select="."></xsl:apply-templates></li>
    </xsl:template>
    
    <xsl:template match="article-meta " mode="generic-history-epub-date">
        <xsl:if test="pub-date[@pub-type='epub']">
            <li>
                <strong>
                    <xsl:apply-templates select="." mode="text-labels">
                        <xsl:with-param name="text">Online publication</xsl:with-param>
                    </xsl:apply-templates>
                </strong><br/> 
                <xsl:apply-templates select="pub-date[@pub-type='epub']"></xsl:apply-templates>
            </li>
        </xsl:if>
    </xsl:template>

    <xsl:template match="sub-article | response" mode="generic-history-epub-date">
        <xsl:if test=".//pub-date[@pub-type='epub']">
            <li>
                <strong>
                    <xsl:apply-templates select="." mode="text-labels">
                        <xsl:with-param name="text">Online publication</xsl:with-param>
                    </xsl:apply-templates>
                </strong><br/> 
                <xsl:apply-templates select=".//pub-date[@pub-type='epub']"></xsl:apply-templates>
            </li>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="article-meta" mode="generic-history-publication-date">
        <xsl:if test="pub-date[@pub-type='epub-ppub'] or pub-date[@pub-type='ppub'] or pub-date[@pub-type='collection']">
                <li><strong>
                    <xsl:apply-templates select="." mode="text-labels">
                        <xsl:with-param name="text"><xsl:choose>
                            <xsl:when test="pub-date[@pub-type='epub-ppub']">Publication</xsl:when>
                            <xsl:otherwise>Issue publication</xsl:otherwise>
                        </xsl:choose></xsl:with-param>
                    </xsl:apply-templates></strong><br/> 
                    <xsl:choose>
                        <xsl:when test="pub-date[@pub-type='epub-ppub']">
                            <xsl:apply-templates select="pub-date[@pub-type='epub-ppub']"></xsl:apply-templates>             
                        </xsl:when>
                        <xsl:when test="pub-date[@pub-type='collection']">
                            <xsl:apply-templates select="pub-date[@pub-type='collection']"></xsl:apply-templates>             
                        </xsl:when>
                        <xsl:when test="pub-date[@pub-type='ppub']">
                            <xsl:apply-templates select="pub-date[@pub-type='ppub']"></xsl:apply-templates>             
                        </xsl:when>
                    </xsl:choose>
                </li>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="sub-article | response" mode="generic-history-publication-date">
        <xsl:if test=".//pub-date[@pub-type='epub-ppub'] or .//pub-date[@pub-type='ppub'] or .//pub-date[@pub-type='collection']">
                <li><strong>
                    <xsl:apply-templates select="." mode="text-labels">
                        <xsl:with-param name="text"><xsl:choose>
                            <xsl:when test=".//pub-date[@pub-type='epub-ppub']">Publication</xsl:when>
                            <xsl:otherwise>Issue publication</xsl:otherwise>
                        </xsl:choose></xsl:with-param>
                    </xsl:apply-templates></strong><br/> 
                    <xsl:choose>
                        <xsl:when test=".//pub-date[@pub-type='epub-ppub']">
                            <xsl:apply-templates select=".//pub-date[@pub-type='epub-ppub']"></xsl:apply-templates>             
                        </xsl:when>
                        <xsl:when test=".//pub-date[@pub-type='collection']">
                            <xsl:apply-templates select=".//pub-date[@pub-type='collection']"></xsl:apply-templates>             
                        </xsl:when>
                        <xsl:when test=".//pub-date[@pub-type='ppub']">
                            <xsl:apply-templates select=".//pub-date[@pub-type='ppub']"></xsl:apply-templates>             
                        </xsl:when>
                    </xsl:choose>
                </li>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="*" mode="generic-history-errata-date">
        <!-- FIXME -->
        <!-- li><strong>Errata:</strong><br/> 01/11/2013</li -->
    </xsl:template>
    
    <xsl:template match="*" mode="generic-history-retraction-date">
        <!-- FIXME -->
        <!-- li><strong>Retratação:</strong><br/> 01/11/2013</li -->
    </xsl:template>
    
    <xsl:template match="*" mode="generic-history-manisfestation-date">
        <!-- FIXME -->
        <!-- li><strong>Manifestação de preocupação:</strong><br/> 01/11/2013</li -->
    </xsl:template>
    
    <xsl:template match="*[month or year or day or season]">
        <xsl:apply-templates select="day"></xsl:apply-templates>
        <xsl:if test="day">&#160;</xsl:if>
        <xsl:choose>
            <xsl:when test="season">
                <xsl:apply-templates select="season"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test="month">
                <xsl:apply-templates select="month" mode="text-labels">
                    <xsl:with-param name="text"><xsl:value-of select="month"/></xsl:with-param>
                </xsl:apply-templates>
            </xsl:when>
        </xsl:choose>
        <xsl:if test="month or season">&#160;</xsl:if>
        <xsl:apply-templates select="year"></xsl:apply-templates>
    </xsl:template>
</xsl:stylesheet>