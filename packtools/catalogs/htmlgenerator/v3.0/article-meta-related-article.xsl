<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/article-meta-related-article.xsl"/>

    <xsl:template match="article" mode="article-meta-related-article">
        <!-- seleciona dados de article ou sub-article -->
        <xsl:if test=".//related-article[@related-article-type!='preprint']">
            <!-- preprint não deve tanto destaque quanto os demais tipos -->
            <!-- caixa amarela -->
            <xsl:choose>
                <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//related-article">
                    <!-- sub-article -->
                    <div class="panel article-correction-title">
                        <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//related-article[@related-article-type!='preprint']" mode="article-meta-related-article-box-item"/>
                    </div>
                </xsl:when>
                <xsl:when test=".//front//related-article">
                    <!-- article -->
                    <div class="panel article-correction-title">
                        <xsl:apply-templates select="front | body | back" mode="article-meta-related-article-box-item"/>
                    </div>
                </xsl:when>
            </xsl:choose>   
        </xsl:if>
    </xsl:template>
</xsl:stylesheet>