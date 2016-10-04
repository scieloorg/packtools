<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    
    <xsl:template match="article-meta/title-group/article-title|article-meta/title-group//trans-title">
        <h1 class="article-title">
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>    
        </h1>
    </xsl:template>
    <xsl:template match="article-id[@pub-id-type='doi']">
        <xsl:variable name="link">https://doi.org/<xsl:value-of select="."/></xsl:variable>
        <div class="row articleMeta">
            <div class="col-md-5 col-sm-12">
                <span>DOI: <xsl:value-of select="."/></span>
            </div>
            <div class="col-md-7 col-sm-12">
                <label class="showTooltip" data-placement="left" title="Clique para copiar a URL">
                    <span class="glyphBtn articleLink "></span> <input type="text" name="link-share" class="fakeLink" value="{$link}" data-clipboard-text="{$link}" data-toggle="tooltip" id="linkShare" />
                </label>
            </div>
        </div>    
    </xsl:template>
    
</xsl:stylesheet>