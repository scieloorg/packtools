<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:variable name="TEXT_LABELS"></xsl:variable>
    <xsl:variable name="INTERFACE_LABELS"></xsl:variable>
    <xsl:template match="*|@*|text()" mode="text-labels">
        <xsl:param name="text"></xsl:param>
        <xsl:choose>
            <xsl:when test="$TEXT_LABELS!=''">
                <xsl:value-of select="$TEXT_LABELS[$text]"/>
            </xsl:when>
            <xsl:otherwise><xsl:value-of select="$text"/></xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template match="*|@*|text()" mode="interface">
        <xsl:param name="text"></xsl:param>
        <xsl:choose>
            <xsl:when test="$INTERFACE_LABELS!=''">
                <xsl:value-of select="$INTERFACE_LABELS[$text]"/>
            </xsl:when>
            <xsl:otherwise><xsl:value-of select="$text"/></xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="*" mode="labels-license-view">
        Veja as permissões desta licença
    </xsl:template>
    <xsl:template match="*" mode="labels-share">
        Compartilhe
    </xsl:template>
    <xsl:variable name="INTERFACE_CLICK_TO_COPY_URL">
        Clique para copiar a URL
    </xsl:variable>
    <xsl:variable name="INTERFACE_COPY_LINK">
        copiar link
    </xsl:variable>
    
    <xsl:template match="@pub-type" mode="label">
        <xsl:apply-templates select="." mode="interface">
            <xsl:with-param name="text"><xsl:choose>
                <xsl:when test=".='epub'">Online</xsl:when>
                <xsl:otherwise>Print</xsl:otherwise>
            </xsl:choose></xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>
    <xsl:template match="pub-date" mode="label">
        <xsl:apply-templates select="." mode="interface">
            <xsl:with-param name="text">Published on</xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>
    <xsl:template match="month" mode="label">
        <xsl:choose>
            <xsl:when test="number(.)=1">
                <xsl:choose>
                    <xsl:when test="$ARTICLE_LANG='es'">Ene</xsl:when>
                    <xsl:otherwise>Jan</xsl:otherwise>
                </xsl:choose>
            </xsl:when>
            <xsl:when test="number(.)=2">
                <xsl:choose>
                    <xsl:when test="$ARTICLE_LANG='pt'">Fev</xsl:when>
                    <xsl:otherwise>Feb</xsl:otherwise>
                </xsl:choose>
            </xsl:when>
            <xsl:when test="number(.)=3">Mar</xsl:when>
            <xsl:when test="number(.)=4"><xsl:choose>
                <xsl:when test="$ARTICLE_LANG='en'">Apr</xsl:when>
                <xsl:otherwise>Abr</xsl:otherwise>
            </xsl:choose></xsl:when>
            <xsl:when test="number(.)=5"><xsl:choose>
                <xsl:when test="$ARTICLE_LANG='en'">May</xsl:when>
                <xsl:when test="$ARTICLE_LANG='es'">Mayo</xsl:when>
                <xsl:otherwise>Maio</xsl:otherwise>
            </xsl:choose></xsl:when>
            <xsl:when test="number(.)=6"><xsl:choose>
                <xsl:when test="$ARTICLE_LANG='en'">June</xsl:when>
                <xsl:otherwise>Jun</xsl:otherwise>
            </xsl:choose></xsl:when>
            <xsl:when test="number(.)=7"><xsl:choose>
                <xsl:when test="$ARTICLE_LANG='en'">July</xsl:when>
                <xsl:otherwise>Jul</xsl:otherwise>
            </xsl:choose></xsl:when>
            <xsl:when test="number(.)=8"><xsl:choose>
                <xsl:when test="$ARTICLE_LANG='en'">Aug</xsl:when>
                <xsl:otherwise>Ago</xsl:otherwise>
            </xsl:choose></xsl:when>
            <xsl:when test="number(.)=9"><xsl:choose>
                <xsl:when test="$ARTICLE_LANG='en'">Sep</xsl:when>
                <xsl:otherwise>Set</xsl:otherwise>
            </xsl:choose></xsl:when>
            <xsl:when test="number(.)=10"><xsl:choose>
                <xsl:when test="$ARTICLE_LANG='pt'">Out</xsl:when>
                <xsl:otherwise>Oct</xsl:otherwise>
            </xsl:choose></xsl:when>
            <xsl:when test="number(.)=11">Nov</xsl:when>
            <xsl:when test="number(.)=12"><xsl:choose>
                <xsl:when test="$ARTICLE_LANG='pt'">Dez</xsl:when>
                <xsl:when test="$ARTICLE_LANG='es'">Dic</xsl:when>
                <xsl:otherwise>Dec</xsl:otherwise>
            </xsl:choose></xsl:when>           
        </xsl:choose>
    </xsl:template> 
    <xsl:template match="abstract | trans-abstract" mode="label">
        <xsl:variable name="lang"><xsl:choose>
            <xsl:when test="@xml:lang"><xsl:value-of select="@xml:lang"/></xsl:when>
            <xsl:otherwise><xsl:value-of select="$ARTICLE_LANG"/></xsl:otherwise>
        </xsl:choose></xsl:variable>
        <xsl:choose>
            <xsl:when test="$lang='es'">Resumen</xsl:when>
            <xsl:when test="$lang='pt'">Resumo</xsl:when>
            <xsl:otherwise>Abstract</xsl:otherwise>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>