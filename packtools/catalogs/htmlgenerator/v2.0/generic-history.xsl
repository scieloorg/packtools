<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:variable name="related_preprint" select="//related-article[@related-article-type='preprint']"/>

    <xsl:template match="article-meta" mode="generic-history">
        <xsl:choose>
            <xsl:when test="$article//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']/front-stub/history">
                <xsl:apply-templates select="$article//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']/front-stub/history" mode="history-section"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="history" mode="history-section"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="sub-article | response" mode="generic-history">
       <xsl:apply-templates select="front-stub/history | front/history" mode="history-section"/>       
    </xsl:template>

    <xsl:template match="history" mode="history-section">
        <!-- manter pareado class="articleSection" e data-anchor="nome da seção no menu esquerdo" -->
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
                        <xsl:apply-templates select="date" mode="generic-history-list-item"/>
                    </ul>
                </div>
            </div>
            <xsl:apply-templates select="." mode="preprint-link-row"/>
        </div>
    </xsl:template>

    <xsl:template match="date" mode="generic-history-list-item">
        <li>
            <strong>
                <xsl:apply-templates select="@date-type" mode="history-item-label"/>
            </strong><br/>
            <xsl:apply-templates select="." mode="format-date"/>
            <xsl:apply-templates select="." mode="preprint-link"/>
        </li>
    </xsl:template>

    <xsl:template match="date" mode="preprint-link">
        <!-- do nothing, no preprint link -->
    </xsl:template>

    <xsl:template match="date[@date-type='preprint']" mode="preprint-link">
        <xsl:if test="$related_preprint">
            <br/>
            <xsl:apply-templates select="$related_preprint[1]" mode="article-meta-related-article-link"/>
        </xsl:if>
    </xsl:template>

    <xsl:template match="history" mode="preprint-link-row">
        <xsl:if test="$related_preprint[1] and not(.//date[@date-type='preprint'])">
            <div class="row">
                <div class="col-md-12 col-sm-12">
                    <ul class="articleTimeline">
                        <li>
                            <strong>
                                <xsl:apply-templates select="." mode="text-labels">
                                    <xsl:with-param name="text">This document has a preprint version</xsl:with-param>
                                </xsl:apply-templates>
                            </strong><br/>
                            <xsl:apply-templates select="$related_preprint[1]" mode="article-meta-related-article-link"/>
                        </li>
                    </ul>
                </div>
            </div>
        </xsl:if>
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

    <xsl:template match="date | pub-date" mode="format-date">
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

    <xsl:template match="date | pub-date">
        <xsl:apply-templates select="." mode="format-date"/>
    </xsl:template>
</xsl:stylesheet>