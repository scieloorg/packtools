<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    >
    <xsl:template match="article | sub-article" mode="article-meta-related-article">
        <xsl:choose>
            <xsl:when test="front//related-article">
                <xsl:apply-templates select="front" mode="article-meta-related-articles"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test="body//related-article">
                <xsl:apply-templates select="body" mode="article-meta-related-articles"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//related-article">
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']" mode="article-meta-related-article"></xsl:apply-templates>
            </xsl:when>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="*" mode="article-meta-related-articles">
        <!-- 
        <related-article ext-link-type="doi" id="ra1" related-article-type="corrected-article" xlink:href="10.1590/0102-311X00064615"></related-article>
        <related-article id="RA1" page="142" related-article-type="corrected-article" vol="39">
            <bold>2016;39(3):142–8</bold>
        </related-article>
        -->
        <xsl:apply-templates select="." mode="article-meta-related-articles-corrected-articles"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="*" mode="article-meta-related-articles-corrected-articles">
        <xsl:if test=".//related-article[@related-article-type='corrected-article']">
            <div class="panel article-correction-title">
                <div class="panel-heading">
                    <xsl:apply-templates select="." mode="text-labels">
                        <xsl:with-param name="text">This erratum corrects</xsl:with-param></xsl:apply-templates>:
                </div>
                <div class="panel-body">
                    <ul>
                        <xsl:apply-templates select=".//related-article[@related-article-type='corrected-article']" mode="article-meta-related-article"></xsl:apply-templates>
                    </ul>
                </div>
            </div>
        </xsl:if>
    </xsl:template>
    
    
    <xsl:template match="related-article" mode="article-meta-related-article">
        <!-- 
        	<li>
				Edição Março de 2016, vol. 106 (3), pág. 168-170.
				<a href="https://doi.org/10.5935/abc.20160032" target="_blank">10.5935/abc.20160032</a>
			</li>
        -->
        <li>
            <xsl:choose>
                <xsl:when test="@xlink:href">
                    <xsl:apply-templates select="@xlink:href"></xsl:apply-templates>
                </xsl:when>
                <xsl:when test="normalize-space(.//text())=''">
                    <xsl:if test="@vol">
                        <xsl:apply-templates select="@vol"></xsl:apply-templates>
                    </xsl:if>
                    <xsl:if test="@issue">
                        (<xsl:apply-templates select="@issue"></xsl:apply-templates>)
                    </xsl:if>
                    <xsl:if test="(@vol or @issue) and (@page or @elocation-id)">: </xsl:if>
                    
                    <xsl:if test="@page">
                        <xsl:apply-templates select="@page"></xsl:apply-templates>
                    </xsl:if>
                    <xsl:if test="@page and @elocation-id">, </xsl:if>
                    <xsl:if test="@elocation-id">
                        <xsl:apply-templates select="@elocation-id"></xsl:apply-templates>
                    </xsl:if>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:apply-templates select="*|text()"></xsl:apply-templates>
                </xsl:otherwise>
            </xsl:choose>
        </li>
    </xsl:template>
    
    <xsl:template match="related-article/@xlink:href">
        <a href="https://doi.org/{.}" target="_blank">
            <xsl:value-of select="."/>
        </a>
    </xsl:template>
</xsl:stylesheet>