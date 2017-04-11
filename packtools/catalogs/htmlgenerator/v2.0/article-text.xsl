<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink" >
    
    <xsl:variable name="q_abstracts"><xsl:apply-templates select="article" mode="count_abstracts"></xsl:apply-templates></xsl:variable>
    <xsl:variable name="q_back"><xsl:apply-templates select="article" mode="count_back_elements"></xsl:apply-templates></xsl:variable>
    <xsl:variable name="body_index"><xsl:value-of select="$q_abstracts"/></xsl:variable>
    
    
    <xsl:template match="*" mode="list-item">
        <li>
            <xsl:apply-templates select="."></xsl:apply-templates>
        </li>
    </xsl:template>
    
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
    
    <xsl:template match="article" mode="sub-articles">
       <xsl:apply-templates select="sub-articles[@article-type!='translation' and (@xml:lang=$TEXT_LANG or not(@xml:lang))]|*[name()!='front' and name()!='body' and name()!='back' and name()!='sub-article']"></xsl:apply-templates>
   </xsl:template>
    
    <xsl:template match="ext-link">
        <xsl:choose>
            <xsl:when test="@xlink:href">
                <a href="{@xlink:href}" target="_blank"><xsl:apply-templates select="*|text()"></xsl:apply-templates></a>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="*|text()"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="email">
        <a href="mailto:{.}"><xsl:value-of select="."/></a>
    </xsl:template>
    
</xsl:stylesheet>