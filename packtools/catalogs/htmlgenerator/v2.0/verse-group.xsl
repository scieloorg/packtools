<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">

    <xsl:template match="verse-group">
        <div class="versegroup">
            <xsl:apply-templates select="*"/>
        </div>
        
    </xsl:template>
      
    <xsl:template match="verse-line">
        <xsl:apply-templates select="*|text()"/><br/>
    </xsl:template>

</xsl:stylesheet>