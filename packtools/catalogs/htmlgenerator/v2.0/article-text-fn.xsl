<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    
    <xsl:template match="article" mode="text-fn">
        <!--
        Apresenta uma lista de fn encontrados em body, exceto os de table-wrap
        -->
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//body//fn">
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']/body" mode="text-fn"/>
            </xsl:when>
            <xsl:when test="body//fn">
                <xsl:apply-templates select="body" mode="text-fn"/>
            </xsl:when>
        </xsl:choose>            
    </xsl:template>
    
    <xsl:template match="body" mode="text-fn">
        <!--
        Apresenta uma lista de fn encontrados em body, exceto os de table-wrap
        -->
        <xsl:if test="count(.//fn) &gt; count(.//table-wrap-foot//fn)">
            <!-- fn em body -->
            <xsl:apply-templates select=".//fn" mode="text-fn"/>
        </xsl:if>
    </xsl:template>

    <xsl:template match="fn" mode="text-fn">
        <!--
        Apresenta uma lista de fn encontrados em body, exceto os de table-wrap
        -->
        <xsl:apply-templates select="." mode="choose-format"/>
    </xsl:template>

    <xsl:template match="table-wrap-foot//fn" mode="text-fn">
        <!-- do nothing for table-wrap-foot/fn -->
    </xsl:template>

    <xsl:template match="fn" mode="choose-format">
        <!--
        Dependendo do tipo de fn, apresenta em formato de
        back-section ou item de lista
        -->
        <xsl:choose>
            <xsl:when test="@fn-type='edited-by' or @fn-type='data-availability'">
                <xsl:apply-templates select="." mode="back-section"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="." mode="div-fn-list-item"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="fn/p">
        <div>
            <xsl:apply-templates select="*|text()"/>
        </div>
    </xsl:template>

    <xsl:template match="body//fn">
        <!-- do nothing for fn in body -->
    </xsl:template>

    <xsl:template match="table-wrap-foot//fn">
        <!-- display table-wrap-foot/fn -->
        <xsl:apply-templates select="." mode="div-fn-list-item"/>
    </xsl:template>

    <xsl:template match="fn" mode="div-fn-list-item">
        <li>
            <xsl:apply-templates select="*|text()" mode="div-fn-list-item"/>
        </li>
    </xsl:template>

    <xsl:template match="fn/p | fn/*" mode="div-fn-list-item">
        <div>
            <xsl:apply-templates select="*|text()"/>
        </div>
    </xsl:template>

    <xsl:template match="fn/label" mode="div-fn-list-item">
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

    <xsl:template match="fn/title" mode="div-fn-list-item">
        <h2><xsl:apply-templates select="*|text()"/></h2>
    </xsl:template>

    <xsl:template match="fn[@fn-type='edited-by']/label | fn[@fn-type='data-availability']/label | fn[@fn-type='edited-by']/title | fn[@fn-type='data-availability']/title" mode="div-fn-list-item">
        <!-- do nothing for fn edited-by or data-availability -->
    </xsl:template>
        
    <xsl:template match="body//fn | back/fn | author-notes/fn | back/fn-group" mode="back-section-content">
        <div class="ref-list">
            <ul class="refList footnote">
                <xsl:apply-templates select="fn" mode="div-fn-list-item"/>
                <xsl:if test="not(fn)">
                    <xsl:apply-templates select="." mode="div-fn-list-item"/>
                </xsl:if>
            </ul>
        </div>
    </xsl:template>

    <xsl:template match="article" mode="author-notes-as-sections">
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//author-notes">
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//front-stub//author-notes/fn" mode="author-notes-as-sections"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select=".//front//author-notes/fn" mode="author-notes-as-sections"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="author-notes/fn" mode="author-notes-as-sections">
        <!-- do nothing for fn <xsl:value-of select="@fn-type"/> -->
    </xsl:template>

    <xsl:template match="author-notes/fn[@id]" mode="author-notes-as-sections">
        <xsl:variable name="id" select="@id"/>
        <xsl:if test="$article//xref[@rid=$id]">
            <xsl:apply-templates select="." mode="back-section"/>
        </xsl:if>
    </xsl:template>

    <xsl:template match="fn[@fn-type='edited-by'] | fn[ @fn-type='data-availability']" mode="author-notes-as-sections">
        <xsl:apply-templates select="." mode="back-section"/>
    </xsl:template>

    <xsl:template match="fn[@fn-type='edited-by'] | fn[ @fn-type='data-availability']" mode="back-section-menu">
        <xsl:variable name="name" select="@fn-type"/>
        <!-- cria menu somente para o primeiro ref-list (há casos de série de ref-list) -->
         <xsl:if test="not(preceding-sibling::node()) or preceding-sibling::*[1][not(@fn-type)] or preceding-sibling::*[1][@fn-type!=$name]">
            <xsl:attribute name="data-anchor">
                <xsl:apply-templates select="." mode="text-labels">
                    <xsl:with-param name="text"><xsl:value-of select="@fn-type"/></xsl:with-param>
                </xsl:apply-templates>
            </xsl:attribute>
            <xsl:if test="not(title) and not(label)">
                <h3>
                    <xsl:apply-templates select="." mode="text-labels">
                        <xsl:with-param name="text"><xsl:value-of select="@fn-type"/></xsl:with-param>
                    </xsl:apply-templates>
                </h3>
            </xsl:if>
        </xsl:if>
    </xsl:template>

</xsl:stylesheet>
