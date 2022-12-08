<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:variable name="related_preprint" select="//related-article[@related-article-type='preprint']"/>
    <xsl:template match="article-meta | sub-article | response" mode="generic-history">
       <xsl:if test=".//history">
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
                     </ul>
                 </div>
             </div>
         </div>
       </xsl:if>
    </xsl:template>

    <xsl:template match="article-meta" mode="generic-history-history-dates">
        <xsl:choose>
            <xsl:when test="$article//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//history">
                <xsl:apply-templates select="$article//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//history/date" mode="generic-history-list-item"></xsl:apply-templates>
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
        <li>
            <strong>
                <xsl:apply-templates select="@date-type" mode="history-item-label"/>
            </strong><br/>
            <xsl:apply-templates select="."></xsl:apply-templates>
            <xsl:if test="@date-type='preprint' and $related_preprint">
                <br/>
                <xsl:apply-templates select="$related_preprint[1]" mode="article-meta-related-article-link"/>
            </xsl:if>
        </li>
    </xsl:template>

    <xsl:template match="@date-type" mode="history-item-label">
        <xsl:apply-templates select="." mode="text-labels">
            <xsl:with-param name="text"><xsl:value-of select="."/></xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="@date-type[.='preprint']" mode="history-item-label">
        <xsl:apply-templates select="." mode="text-labels">
            <xsl:with-param name="text">date-type-<xsl:value-of select="."/></xsl:with-param>
        </xsl:apply-templates>
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