<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/generic-history.xsl"/>

    <xsl:template match="history" mode="history-section">
        <!-- manter pareado class="articleSection" e data-anchor="nome da seção no menu esquerdo" -->
        <div class="articleSection">
            <xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="text-labels">
                <xsl:with-param name="text">History</xsl:with-param>
            </xsl:apply-templates></xsl:attribute>
            <h2 class="h5"><xsl:apply-templates select="." mode="text-labels">
                <xsl:with-param name="text">History</xsl:with-param>
            </xsl:apply-templates></h2>
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

</xsl:stylesheet>