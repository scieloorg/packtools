<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:variable name="ref" select="//ref"></xsl:variable>
    
    <xsl:template match="article" mode="text">
        <article id="articleText" class="col-md-10 col-md-offset-2 col-sm-12 col-sm-offset-0">
            <xsl:apply-templates select="." mode="article-meta-abstract"></xsl:apply-templates>
            <xsl:apply-templates select="." mode="text-body"></xsl:apply-templates>
            <xsl:apply-templates select="." mode="text-back"></xsl:apply-templates>
            <xsl:apply-templates select=". " mode="dates-notes"></xsl:apply-templates>
        </article>
    </xsl:template>
    
    <xsl:template match="*" mode="text-body">
        <div class="articleSection" data-anchor="Texto">
            <!-- FIXME: body ou sub-article/body -->
            <xsl:apply-templates select="./body"></xsl:apply-templates>
        </div>
    </xsl:template>
    
    <xsl:template match="body/sec">
        <xsl:param name="position"></xsl:param>
        <a name="articleSection{position()}"/>
        
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
    
    <xsl:template match="*" mode="title">
        <xsl:if test="not(title)">
            <xsl:apply-templates select="." mode="generated-title"></xsl:apply-templates>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="body/sec/title">
        <xsl:param name="position"></xsl:param>
        <a name="as1-heading{$position - 1}"></a>
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
    
    <xsl:template match="xref[@ref-type='bibr']">
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
    
    <xsl:template match="fn">
        <xsl:param name="position"></xsl:param>
        
        <a name="{@id}"/>
        <div id="{@id}" class="footnote">
            <xsl:apply-templates select="*|text()">
                <xsl:with-param name="position" select="position()"></xsl:with-param>
            </xsl:apply-templates>
        </div>
    </xsl:template>
    
    <xsl:template match="xref">
        <xsl:variable name="type"><xsl:choose>
            <xsl:when test="@ref-type='equation'">formula</xsl:when>
            <xsl:when test="@ref-type='disp-formula'">formula</xsl:when>
            <xsl:when test="@ref-type='fig'">figure</xsl:when>
            <xsl:when test="@ref-type='table'">table</xsl:when>
            
        </xsl:choose></xsl:variable>
        <a href="#{@rid}" class="goto">
            <span class="glyphBtn {$type}Icon"></span><xsl:value-of select="."/>
        </a>
    </xsl:template>
    <xsl:template match="xref[@ref-type='bibr']" mode="text">
        <xsl:variable name="id"><xsl:value-of select="@rid"/></xsl:variable>
        <xsl:apply-templates select="$document//ref[@id=$id]" mode="text"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="ref" mode="text">
        <xsl:variable name="url"><xsl:choose>
            <xsl:when test=".//ext-link"><xsl:value-of select=".//ext-link[1]"/></xsl:when>
            <xsl:when test=".//pub-id[@pub-id-type='doi']">https://doi.org/<xsl:value-of select=".//pub-id[@pub-id-type='doi']"/></xsl:when>
        </xsl:choose></xsl:variable>
        
        <a href="{$url}" target="_blank">
            <xsl:apply-templates select="mixed-citation" mode="text"></xsl:apply-templates>
        </a>
    </xsl:template>
    <xsl:template match="mixed-citation/*" mode="text">
        <xsl:apply-templates select="*|text()"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="p | sub | sup">
        <xsl:param name="position"></xsl:param>
        <xsl:element name="{name()}">
            <xsl:apply-templates select="*|text()">
                <xsl:with-param name="position" select="position()"></xsl:with-param>
            </xsl:apply-templates>
        </xsl:element>
    </xsl:template>
    
    <xsl:template match="*" mode="dates-notes">
        <div class="articleSection" data-anchor="Data de publicação">
            <a name="articleSection8"></a>
            
            <div class="row">
                <div class="col-md-12 col-sm-12">
                    <h1><xsl:apply-templates select="." mode="interface"><xsl:with-param name="text">Data de publicação</xsl:with-param></xsl:apply-templates></h1>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12 col-sm-12">
                    <ul class="articleTimeline">
                        <xsl:apply-templates select="." mode="submission-date"></xsl:apply-templates>
                        <xsl:apply-templates select="." mode="approvement-date"></xsl:apply-templates>
                        <xsl:apply-templates select="." mode="aop-date"></xsl:apply-templates>
                        <xsl:apply-templates select="." mode="publication-date"></xsl:apply-templates>
                        <xsl:apply-templates select="." mode="errata-date"></xsl:apply-templates>
                        <xsl:apply-templates select="." mode="retraction-date"></xsl:apply-templates>
                        <xsl:apply-templates select="." mode="manisfestation-date"></xsl:apply-templates>
                    </ul>
                </div>
            </div>
        </div>
    </xsl:template>
    <xsl:template match="*" mode="submission-date">
        <li><strong>Submissão:</strong><br/> <xsl:apply-templates select=".//history/date[@date-type='received']"></xsl:apply-templates></li>
    </xsl:template>
    <xsl:template match="*" mode="approvement-date">
        <li><strong>Aprovação:</strong><br/> <xsl:apply-templates select=".//history/date[@date-type='accepted']"></xsl:apply-templates></li>
    </xsl:template>
    <xsl:template match="*" mode="aop-date">
        <xsl:choose>
            <xsl:when test=".//article-meta/pub-date[@pub-type='epub'] and .//article-meta/pub-date[@pub-type='ppub']">
                <li><strong>Publicação Avançada:</strong><br/> <xsl:apply-templates select=".//article-meta/pub-date[@pub-type='epub']"></xsl:apply-templates></li>                
            </xsl:when>
            <xsl:when test=".//article-meta/pub-date[@pub-type='epub'] and count(.//article-meta/pub-date)=1">
                <li><strong>Publicação Avançada:</strong><br/> <xsl:apply-templates select=".//pub-date[@pub-type='epub']"></xsl:apply-templates></li>                
            </xsl:when>
        </xsl:choose>
    </xsl:template>
    <xsl:template match="*" mode="publication-date">
        <xsl:if test=".//article-meta/pub-date[@pub-type='epub-ppub'] or .//article-meta/pub-date[@pub-type='ppub'] or .//article-meta/pub-date[@pub-type='collection']">
            <li><strong>Publicação em número:</strong><br/> 
            <xsl:choose>
                <xsl:when test=".//article-meta/pub-date[@pub-type='epub-ppub']">
                    <xsl:apply-templates select=".//article-meta/pub-date[@pub-type='epub-ppub']"></xsl:apply-templates>             
                </xsl:when>
                <xsl:when test=".//article-meta/pub-date[@pub-type='collection']">
                    <xsl:apply-templates select=".//article-meta/pub-date[@pub-type='collection']"></xsl:apply-templates>             
                </xsl:when>
                <xsl:when test=".//article-meta/pub-date[@pub-type='ppub']">
                    <xsl:apply-templates select=".//article-meta/pub-date[@pub-type='ppub']"></xsl:apply-templates>             
                </xsl:when>
            </xsl:choose>
            </li>
        </xsl:if>
    </xsl:template>
    <xsl:template match="*" mode="errata-date">
        <!-- FIXME -->
        <li><strong>Errata:</strong><br/> 01/11/2013</li>
    </xsl:template>
    <xsl:template match="*" mode="retraction-date">
        <!-- FIXME -->
        <li><strong>Retratação:</strong><br/> 01/11/2013</li>
    </xsl:template>
    <xsl:template match="*" mode="manisfestation-date">
        <!-- FIXME -->
        <li><strong>Manifestação de preocupação:</strong><br/> 01/11/2013</li>
    </xsl:template>
    
    <xsl:template match="*[month or year or day or season]">
        <xsl:apply-templates select="day"></xsl:apply-templates>
        <xsl:if test="day">/</xsl:if>
        <xsl:apply-templates select="month|season"></xsl:apply-templates>
        <xsl:if test="month or season">/</xsl:if>
        <xsl:apply-templates select="year"></xsl:apply-templates>
    </xsl:template>
</xsl:stylesheet>