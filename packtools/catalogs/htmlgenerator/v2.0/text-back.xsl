<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="article" mode="text-back">
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG]">
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG]//back/*" mode="layout"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="./back/*" mode="layout"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
        
    </xsl:template>
    
    <xsl:template match="back/*" mode="layout">
        <div class="articleSection">
            <xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="title"></xsl:apply-templates></xsl:attribute>
            <a name="articleSection{$body_index + position()}"></a>
            <div class="row">
                <div class="col-md-12 col-sm-12">
                    <h1><xsl:apply-templates select="." mode="title"/></h1>
                </div>
            </div>
            <xsl:apply-templates select="." mode="content"></xsl:apply-templates>
        </div>
    </xsl:template>
    
    <xsl:template match="back/*" mode="content">
        <xsl:apply-templates select="*[name()!='title']|text()"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="back/ref-list" mode="content">
        <div class="row">
            <div class="col-md-12 col-sm-12 ref-list">
                <ul class="refList">
                    <xsl:apply-templates select="ref"></xsl:apply-templates>
                </ul>
            </div>
        </div>
    </xsl:template>
    
    <xsl:template match="fn">
        <xsl:param name="position"></xsl:param>
        
        <a name="{@id}"/>
        <div id="{@id}" class="footnote">
            <xsl:apply-templates select="*|text()">
                <xsl:with-param name="position" select="position()"></xsl:with-param>
            </xsl:apply-templates>
        </div>
    </xsl:template>
    
    <xsl:template match="fn" mode="text">
        <xsl:apply-templates select="p" mode="footnote-in-text"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="*" mode="footnote-in-text">
        <xsl:apply-templates select="*|text()" mode="footnote-in-text"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="*" mode="dates-notes">
        <xsl:param name="position"></xsl:param>
        <div class="articleSection">
            <xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="text-labels">
                <xsl:with-param name="text">History</xsl:with-param>
            </xsl:apply-templates></xsl:attribute>
            <a name="articleSection{$body_index + $q_back + 1}"></a>
            
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
        <xsl:apply-templates select=".//history/date" mode="list-item"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="history/date" mode="list-item">
        <li><strong><xsl:apply-templates select="." mode="label"></xsl:apply-templates></strong><br/> <xsl:apply-templates select="."></xsl:apply-templates></li>
    </xsl:template>
    
    <xsl:template match="*" mode="aop-date">
        <xsl:choose>
            <xsl:when test=".//article-meta/pub-date[@pub-type='epub'] and .//article-meta/pub-date[@pub-type='ppub']">
                <li><strong>Publicação Avançada:</strong><br/> <xsl:apply-templates select=".//article-meta/pub-date[@pub-type='epub']"></xsl:apply-templates></li>                
            </xsl:when>
            <xsl:when test=".//article-meta/pub-date[@pub-type='epub'] and count(.//article-meta/pub-date)=1">
                <li><strong>Publicação Avançada:</strong><br/> <xsl:apply-templates select=".//pub-date[@pub-type='epub']"></xsl:apply-templates></li>                
            </xsl:when>
        </xsl:choose>
    </xsl:template>
    <xsl:template match="*" mode="publication-date">
        <xsl:if test=".//article-meta/pub-date[@pub-type='epub-ppub'] or .//article-meta/pub-date[@pub-type='ppub'] or .//article-meta/pub-date[@pub-type='collection']">
            <li><strong>Publicação em número:</strong><br/> 
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
        <xsl:apply-templates select="day"></xsl:apply-templates>
        <xsl:if test="day">/</xsl:if>
        <xsl:apply-templates select="month|season"></xsl:apply-templates>
        <xsl:if test="month or season">/</xsl:if>
        <xsl:apply-templates select="year"></xsl:apply-templates>
    </xsl:template>
</xsl:stylesheet>