<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:variable name="ref" select="//ref"></xsl:variable>
    
    
    <xsl:variable name="q_abstracts"><xsl:apply-templates select="article" mode="count_abstracts"></xsl:apply-templates></xsl:variable>
    <xsl:variable name="q_back"><xsl:apply-templates select="article" mode="count_back_elements"></xsl:apply-templates></xsl:variable>
    <xsl:variable name="body_index"><xsl:value-of select="$q_abstracts"/></xsl:variable>
    
    <xsl:template match="article" mode="count_abstracts">
        <xsl:choose>
            <xsl:when test=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]">
                <xsl:apply-templates select=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]" mode="count_abstracts"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select=".//article-meta" mode="count_abstracts"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="*" mode="count_abstracts">
        <xsl:value-of select="count(.//abstract)+count(.//trans-abstract)"></xsl:value-of>
    </xsl:template>
    
    <xsl:template match="article" mode="count_back_elements">
        <xsl:choose>
            <xsl:when test=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]">
                <xsl:apply-templates select=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]" mode="count_back_elements"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="count(back/*)"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="sub-article[@article-type='translation']" mode="count_back_elements">
        <xsl:choose>
            <xsl:when test="back/ref-list">
                <xsl:value-of select="count(back/*)"/>
            </xsl:when>
            <xsl:when test="../back/ref-list">
                <xsl:value-of select="count(back/*)+1"/>
            </xsl:when>
            <xsl:otherwise><xsl:value-of select="count(back/*)"/></xsl:otherwise>
        </xsl:choose>       
    </xsl:template>
    
    <xsl:template match="article" mode="text">
        <article id="articleText" class="col-md-10 col-md-offset-2 col-sm-12 col-sm-offset-0">
            <xsl:apply-templates select="." mode="article-meta-abstract"></xsl:apply-templates>
            <xsl:apply-templates select="." mode="text-body"></xsl:apply-templates>
            <xsl:apply-templates select="." mode="text-back"></xsl:apply-templates>
            <xsl:apply-templates select="." mode="sub-articles"></xsl:apply-templates>
            
            <xsl:apply-templates select="." mode="dates-notes">
                <xsl:with-param name="position">
                    <xsl:value-of select="$q_abstracts + count(./body) + $q_back"/>
                </xsl:with-param>
            </xsl:apply-templates>
        </article>
    </xsl:template>
    <xsl:template match="*" mode="title">
        <xsl:apply-templates select="title"></xsl:apply-templates>
        <xsl:if test="not(title)">
            <xsl:apply-templates select="." mode="label"></xsl:apply-templates>
        </xsl:if>
    </xsl:template>
    <xsl:template match="*" mode="text-body">
        <div class="articleSection">
            <xsl:attribute name="data-anchor">
            <xsl:apply-templates select="body" mode="label"/>
            </xsl:attribute>
            <!-- FIXME: body ou sub-article/body -->
            <a name="articleSection{$body_index}"/>
            <xsl:choose>
                <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG]">
                    <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG]//body/*"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:apply-templates select="./body/*"/>                    
                </xsl:otherwise>
            </xsl:choose>            
        </div>
    </xsl:template>
    
    <xsl:template match="body/sec">
        <xsl:param name="position"></xsl:param>
        <a name="as{$body_index}-heading{position()-1}"/>
        
        <xsl:apply-templates>
            <xsl:with-param name="position" select="position()"></xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>
    <xsl:template match="body/*/sec">
        <xsl:param name="position"></xsl:param>
        
        <xsl:apply-templates>
            <xsl:with-param name="position" select="position()"></xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>
    <xsl:template match="body//p">
        <xsl:param name="position"></xsl:param>
        <p>
        <xsl:apply-templates select="*|text()">
            <xsl:with-param name="position" select="position()"></xsl:with-param>
        </xsl:apply-templates>
        </p>
    </xsl:template>
    
    <xsl:template match="body/sec/title">
        <xsl:param name="position"></xsl:param>
        <h1 id="text-{../@sec-type}">
            <xsl:apply-templates select="*|text()"/>
        </h1>
    </xsl:template>
    
    <xsl:template match="body/sec/sec/title">
        <xsl:param name="position"></xsl:param>
        
        <h2>
            <xsl:apply-templates select="*|text()"/>
        </h2>
    </xsl:template>
    
    <xsl:template match="xref">
        <xsl:variable name="type"><xsl:choose>
            <xsl:when test="@ref-type='equation'">formula</xsl:when>
            <xsl:when test="@ref-type='disp-formula'">formula</xsl:when>
            <xsl:when test="@ref-type='fig'">figure</xsl:when>
            <xsl:when test="@ref-type='table'">table</xsl:when>
            </xsl:choose></xsl:variable>
        <a href="#{@rid}" class="goto">
            <xsl:choose>
                <xsl:when test="$type!=''">
                    <span class="glyphBtn {$type}Icon"></span><xsl:value-of select="."/>
                </xsl:when>
                <xsl:otherwise>
                    <sup><xsl:value-of select="."/></sup>
                </xsl:otherwise>
            </xsl:choose>
        </a>
    </xsl:template>
    <xsl:template match="xref[@ref-type='bibr' or @ref-type='fn']">
        <xsl:param name="position"></xsl:param>
        <xsl:variable name="id">p<xsl:value-of select="$position"/>-<xsl:value-of select="@rid"/></xsl:variable>
        <span class="ref">
            <xsl:choose>
                <xsl:when test="sup">
                    <sup class="xref {$id}"><xsl:value-of select="."/></sup>
                </xsl:when>
                <xsl:otherwise>
                    <sup class="xref {$id}"><xsl:value-of select="."/></sup>
                </xsl:otherwise>
            </xsl:choose>
            <span class="{$id} closed">
                <xsl:apply-templates select="." mode="text"></xsl:apply-templates>
            </span>
        </span>
    </xsl:template>
    
    <xsl:template match="list">
        <xsl:param name="position"></xsl:param>
        
        <xsl:choose>
            <xsl:when test="@list-type='order'">
                <ol>
                    <xsl:apply-templates select="*">
                        <xsl:with-param name="position" select="position()"></xsl:with-param>
                    </xsl:apply-templates>
                </ol>
            </xsl:when>
            <xsl:otherwise>
                <ul>
                    <xsl:apply-templates select="*">
                        <xsl:with-param name="position" select="position()"></xsl:with-param>
                    </xsl:apply-templates>
                </ul>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="list-item">
        <xsl:param name="position"></xsl:param>
        
        <li>
            <xsl:apply-templates select="*|text()">
                <xsl:with-param name="position" select="position()"></xsl:with-param>
            </xsl:apply-templates>
        </li>
    </xsl:template>
    
    <xsl:template match="xref[@ref-type='bibr']" mode="text">
        <xsl:variable name="id"><xsl:value-of select="@rid"/></xsl:variable>
        <xsl:apply-templates select="$document//ref[@id=$id]" mode="text"></xsl:apply-templates>
    </xsl:template>
    <xsl:template match="xref[@ref-type='fn']" mode="text">
        <xsl:variable name="id"><xsl:value-of select="@rid"/></xsl:variable>
        <xsl:apply-templates select="$document//fn[@id=$id]" mode="text"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="ref" mode="text">
        <xsl:variable name="url"><xsl:apply-templates select="." mode="url"></xsl:apply-templates></xsl:variable>
        <xsl:choose>
            <xsl:when test="$url!=''">
                <a href="{$url}" target="_blank">
                    <xsl:apply-templates select="mixed-citation"></xsl:apply-templates>
                </a>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="mixed-citation"></xsl:apply-templates></xsl:otherwise>
        </xsl:choose>
    </xsl:template>
   
    <xsl:template match="article" mode="sub-articles">
       <xsl:apply-templates select="sub-articles[@article-type!='translation' and (@xml:lang=$TEXT_LANG or not(@xml:lang))]"></xsl:apply-templates>
       
   </xsl:template>
</xsl:stylesheet>