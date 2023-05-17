<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:template match="custom-meta-group">
        <!--
            <custom-meta>
                <meta-name>peer-review-recommendation</meta-name>
                <meta-value>accept</meta-value>
            </custom-meta>
        -->
        <div class="row">
            <div class="col-md-12 col-sm-12">
                <ul class="articleTimeline">
                    <xsl:apply-templates select="custom-meta"/>
                </ul>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="custom-meta">
        <li>
            <strong><xsl:apply-templates select="meta-name"/>: </strong>
            <xsl:apply-templates select="meta-value"/>
        </li>
    </xsl:template>

    <xsl:template match="meta-name | meta-value">
        <xsl:apply-templates match="." mode="text-labels">
            <xsl:with-param name="text" select="."/>
            <xsl:with-param name="default_value" select="."/>
        </xsl:apply-templates>
    </xsl:template>
</xsl:stylesheet>