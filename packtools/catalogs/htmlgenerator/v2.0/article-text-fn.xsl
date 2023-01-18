<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    
    <xsl:template match="article" mode="text-fn">  
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//body">
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//body" mode="text-fn"/>
            </xsl:when>
            <xsl:when test="body">
                <xsl:apply-templates select="body" mode="text-fn"/>
            </xsl:when>
        </xsl:choose>            
    </xsl:template>
    
    <xsl:template match="body" mode="text-fn">
        <xsl:variable name="footnotes"><xsl:apply-templates select=".//fn" mode="text-fn"/></xsl:variable>
        <xsl:if test="normalize-space($footnotes) != ''">
            <div class="articleSection">
                <h2></h2>
                <div class="ref-list">
                    <xsl:value-of select="$footnotes"/>
                </div>
            </div>
        </xsl:if>
    </xsl:template>
  
    <xsl:template match="fn" mode="text-fn">
        <xsl:apply-templates select="."/>
    </xsl:template>
    
    <xsl:template match="table-wrap-foot//fn" mode="text-fn">
    </xsl:template>

    <xsl:template match="fn">
        <li>
            <xsl:apply-templates select="*|text()"/>
        </li>
    </xsl:template>

    <xsl:template match="fn[@fn-type='edited-by'] | fn[@fn-type='data-availability']">
        <li>
            <xsl:apply-templates select="." mode="open-science-notes"/>
        </li>
    </xsl:template>

    <xsl:template match="fn/label">
        <xsl:variable name="title"><xsl:apply-templates select="*|text()"/></xsl:variable>
        <xsl:choose>
            <xsl:when test="string-length(normalize-space($title)) &gt; 3">
                <h3><xsl:apply-templates select="*|text()"/></h3>
            </xsl:when>
            <xsl:otherwise>
                <span class="xref big"><xsl:apply-templates select="*|text()"/></span>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="fn/p">
        <div>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </div>
    </xsl:template>
        
    <xsl:template match="fn/title">
        <h2><xsl:apply-templates select="*|text()"></xsl:apply-templates></h2>        
    </xsl:template>

    <xsl:template match="back/fn | back/fn-group" mode="back-section-content">
            <div class="ref-list">
                <ul class="refList footnote">
                    <xsl:apply-templates select="*[name()!='title']|text()"></xsl:apply-templates>
                </ul>
            </div>
    </xsl:template>

    <xsl:template match="article" mode="author-notes-as-sections">
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']">
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//front-stub//author-notes" mode="author-notes-as-sections"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select=".//front//author-notes" mode="author-notes-as-sections"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="author-notes" mode="author-notes-as-sections">
        <!--
            destaca algumas notas de autores, colocando-as no menu esquerdo
        -->  
        <xsl:apply-templates select="fn[@fn-type='edited-by'] | fn[@fn-type='data-availability']" mode="open-science-notes"/>
    </xsl:template>

    <xsl:template match="fn[@fn-type='edited-by'] | fn[@fn-type='data-availability']" mode="open-science-notes">
        <xsl:variable name="title"><xsl:apply-templates select="label"/><xsl:if test="not(label)"><xsl:apply-templates select="." mode="text-labels">
                 <xsl:with-param name="text"><xsl:value-of select="@fn-type"/></xsl:with-param>
             </xsl:apply-templates></xsl:if></xsl:variable>
        <div>
            <xsl:attribute name="class">articleSection</xsl:attribute>
            <xsl:attribute name="data-anchor"><xsl:value-of select="translate($title, ':', '')"/></xsl:attribute>
            <h3><xsl:value-of select="translate($title, ':', '')"/></h3>
            <xsl:apply-templates select="*[name()!='label']|text()"/>
        </div>
    </xsl:template>

</xsl:stylesheet>
