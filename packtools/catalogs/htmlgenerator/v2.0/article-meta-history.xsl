<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    
    
    <xsl:template match="*" mode="dates-notes">
        <xsl:param name="position"></xsl:param>
        <div class="articleSection">
            <xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="text-labels">
                <xsl:with-param name="text">History</xsl:with-param>
                </xsl:apply-templates></xsl:attribute>
            <a name="articleSection{$body_index + $q_back + $q_body_fn + $q_subarticle + 1}"></a>
            
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
                        <xsl:apply-templates select="." mode="history-dates"></xsl:apply-templates>
                        <xsl:apply-templates select="." mode="aop-date"></xsl:apply-templates>
                        <xsl:apply-templates select="." mode="publication-date"></xsl:apply-templates>
                        <xsl:apply-templates select="." mode="errata-date"></xsl:apply-templates>
                        <xsl:apply-templates select="." mode="retraction-date"></xsl:apply-templates>
                        <xsl:apply-templates select="." mode="manisfestation-date"></xsl:apply-templates>
                    </ul>
                </div>
            </div>
        </div>
    </xsl:template>
    
    <xsl:template match="*" mode="history-dates">
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG]//history">
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG]//history/date" mode="list-item"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select=".//article-meta/history/date" mode="list-item"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="history/date" mode="list-item">
        <li><strong><xsl:apply-templates select="." mode="label"></xsl:apply-templates></strong><br/> <xsl:apply-templates select="."></xsl:apply-templates></li>
    </xsl:template>
    
    <xsl:template match="*" mode="aop-date">
        <xsl:if test=".//article-meta/pub-date[@pub-type='epub']">
            <li>
                <strong>
                    <xsl:apply-templates select="." mode="text-labels">
                        <xsl:with-param name="text">Online publication</xsl:with-param>
                    </xsl:apply-templates>
                </strong><br/> 
                <xsl:apply-templates select=".//article-meta/pub-date[@pub-type='epub']"></xsl:apply-templates>
            </li>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="*" mode="publication-date">
        <xsl:if test=".//article-meta/pub-date[@pub-type='epub-ppub'] or .//article-meta/pub-date[@pub-type='ppub'] or .//article-meta/pub-date[@pub-type='collection']">
            <li><strong>
                <xsl:apply-templates select="." mode="text-labels">
                <xsl:with-param name="text"><xsl:choose>
                    <xsl:when test=".//article-meta/pub-date[@pub-type='epub-ppub']">Publication</xsl:when>
                    <xsl:otherwise>Issue publication</xsl:otherwise>
                </xsl:choose></xsl:with-param>
            </xsl:apply-templates></strong><br/> 
                <xsl:choose>
                    <xsl:when test=".//article-meta/pub-date[@pub-type='epub-ppub']">
                        <xsl:apply-templates select=".//article-meta/pub-date[@pub-type='epub-ppub']"></xsl:apply-templates>             
                    </xsl:when>
                    <xsl:when test=".//article-meta/pub-date[@pub-type='collection']">
                        <xsl:apply-templates select=".//article-meta/pub-date[@pub-type='collection']"></xsl:apply-templates>             
                    </xsl:when>
                    <xsl:when test=".//article-meta/pub-date[@pub-type='ppub']">
                        <xsl:apply-templates select=".//article-meta/pub-date[@pub-type='ppub']"></xsl:apply-templates>             
                    </xsl:when>
                </xsl:choose>
            </li>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="*" mode="errata-date">
        <!-- FIXME -->
        <!-- li><strong>Errata:</strong><br/> 01/11/2013</li -->
    </xsl:template>
    
    <xsl:template match="*" mode="retraction-date">
        <!-- FIXME -->
        <!-- li><strong>Retratação:</strong><br/> 01/11/2013</li -->
    </xsl:template>
    
    <xsl:template match="*" mode="manisfestation-date">
        <!-- FIXME -->
        <!-- li><strong>Manifestação de preocupação:</strong><br/> 01/11/2013</li -->
    </xsl:template>
    
    <xsl:template match="*[month or year or day or season]">
        <xsl:apply-templates select="day"></xsl:apply-templates>&#160;
        <xsl:choose>
            <xsl:when test="season">
                <xsl:apply-templates select="season"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test="month">
                <xsl:apply-templates select="month" mode="label"></xsl:apply-templates>
            </xsl:when>
        </xsl:choose>
        &#160;<xsl:apply-templates select="year"></xsl:apply-templates>
    </xsl:template>
</xsl:stylesheet>