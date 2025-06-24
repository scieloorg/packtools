<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/article-text-sub-article.xsl"/>

    <xsl:template match="sub-article[@article-type!='translation']//subject | response//subject">
        <h2 class="h5"><xsl:apply-templates select="*|text()"></xsl:apply-templates></h2>
     </xsl:template>

</xsl:stylesheet>