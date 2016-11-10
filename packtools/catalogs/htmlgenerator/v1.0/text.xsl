<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:variable name="ref" select="//ref"></xsl:variable>
    
    <xsl:template match="article" mode="text">
        <div class="row articleTxt">
            <!-- ul class="col-md-2 hidden-sm articleMenu">
            </ul-->
            <article id="articleText" class="col-md-10 col-md-offset-2 col-sm-12">
                <xsl:apply-templates select="." mode="article-meta-abstract"></xsl:apply-templates>
                <xsl:apply-templates select="." mode="text-body"></xsl:apply-templates>
                <xsl:apply-templates select="." mode="text-back"></xsl:apply-templates>
            </article>
        </div>
    </xsl:template>
    
    <xsl:template match="*" mode="text-body">
        <div class="articleSection" data-anchor="Texto">
            <!-- FIXME: body ou sub-article/body -->
            <xsl:apply-templates select="./body"></xsl:apply-templates>
        </div>
    </xsl:template>
    
    <xsl:template match="body/sec[@sec-type]">
        <xsl:apply-templates select="*">
            <xsl:with-param name="position" select="position()"></xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="body/sec/title">
        <xsl:param name="position"></xsl:param>
        <!--div class="row">
            <a name="as1-heading{$position - 1}"></a>
            <div class="col-md-8 col-sm-9 text">
                <h1>
                    <xsl:if test="../@sec-type">
                        <xsl:attribute name="id">text-<xsl:value-of select="../@sec-type"/></xsl:attribute>
                    </xsl:if>
                    <xsl:apply-templates select="*|text()"/>
                </h1>
            </div>
        </div-->
    </xsl:template>
    
    <xsl:template match="p">
        <xsl:element name="{name()}">
            <xsl:apply-templates select="@*|*|text()"/>
        </xsl:element>
    </xsl:template>
    
    <xsl:template match="body/p | sec/p">
        <div class="row paragraph">
            <div class="col-md-8 col-sm-8 text">
                <p>
                    <xsl:apply-templates select="*|text()"></xsl:apply-templates>
                </p>    
            </div>
            <!-- referencia na lateral -->
        </div>
    </xsl:template>
    <xsl:template match="p" mode="text-xref-list">
        <xsl:variable name="pindex" select="position()"></xsl:variable>
        <ul class="refList">
            <xsl:apply-templates select=".//xref" mode="text-xref-list-item">
                <xsl:with-param name="pindex" select="$pindex"></xsl:with-param>
            </xsl:apply-templates>
        </ul>
    </xsl:template>
    <xsl:template match="xref" mode="text-xref-list-item">
        <xsl:variable name="rid" select="@rid"></xsl:variable>
        <xsl:apply-templates select="$ref[@id=$rid]" mode="text-xref-list-item"></xsl:apply-templates>
    </xsl:template>
    <xsl:template match="ref/label">
        <sup class="xref big"><xsl:apply-templates select="*|text()"></xsl:apply-templates></sup>
    </xsl:template>
    <xsl:template match="ref" mode="text-xref-list-item">
        <xsl:param name="pindex"></xsl:param>
        <li class="p{$pindex}-{@id}">
            <xsl:apply-templates select="label"/>
            <div class="closed">
                <xsl:apply-templates select="." mode="part"/>
                <div class="source"><xsl:apply-templates select="." mode="source-year"/></div>
            </div>
            <div class="opened">
                <strong><xsl:apply-templates select="." mode="part"/></strong>
                <xsl:apply-templates select="element-citation/person-group[1]"></xsl:apply-templates>
                <div class="source">
                    <xsl:apply-templates select="." mode="source-year-pages-doi"/>
                </div>
            </div>
        </li>
    </xsl:template>
    <xsl:template match="ref" mode="part">
        <xsl:apply-templates select="element-citation/article-title|element-citation/chapter-title"/>.
    </xsl:template>
    <xsl:template match="ref" mode="source-year">
        <xsl:apply-templates select="element-citation/source"/>, <xsl:apply-templates select="element-citation/year"/>.
    </xsl:template>
    <xsl:template match="ref" mode="source-year-pages-doi">
        <xsl:apply-templates select="element-citation/source"/><xsl:text> </xsl:text><xsl:apply-templates select="element-citation/year"/>: <xsl:apply-templates select="." mode="pages"></xsl:apply-templates><xsl:apply-templates select="." mode="doi"></xsl:apply-templates>.
    </xsl:template>
    <xsl:template match="ref" mode="doi">
        <xsl:choose>
            <xsl:when test="element-citation/pub-id[@pub-id-type='doi']">, doi: <xsl:apply-templates select="element-citation/pub-id[@pub-id-type='doi']"></xsl:apply-templates>
            </xsl:when>
        </xsl:choose>
    </xsl:template>
    <xsl:template match="ref" mode="pages">
        <xsl:if test="element-citation/fpage">
            <xsl:apply-templates select="element-citation/fpage"/><xsl:if test="lpage">-<xsl:apply-templates select="element-citation/lpage"/></xsl:if>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="list">
        <xsl:choose>
            <xsl:when test="@list-type='order'">
                <ol>
                    <xsl:apply-templates select="*"></xsl:apply-templates>
                </ol>
            </xsl:when>
            <xsl:otherwise>
                <ul>
                    <xsl:apply-templates select="*"></xsl:apply-templates>
                </ul>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="list-item">
        <li>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </li>
    </xsl:template>
    
    <xsl:template match="fn">
        <a name="{@id}"/>
        <div id="{@id}" class="footnote">
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </div>
    </xsl:template>
</xsl:stylesheet>