<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">

    <xsl:template match="front | front-stub" mode="modal-id"><xsl:value-of select="../@id"/></xsl:template>
    <xsl:template match="article-meta | sub-article[@article-type='translation']/front | sub-article[@article-type='translation']/front-stub" mode="modal-id">    
    </xsl:template>
    
    <xsl:variable name="xref_items" select="$article//xref[@rid]"/>
    
    <xsl:template match="article" mode="modal-contribs">
        <xsl:choose>
            <xsl:when
                test="sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]">
                <xsl:apply-templates
                    select="sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]" mode="modal-contrib"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="front/article-meta" mode="modal-contrib"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:apply-templates select=".//sub-article[@article-type!='translation'] | .//response[@xml:lang=$TEXT_LANG]" mode="modal-contrib"></xsl:apply-templates>            
    </xsl:template>
    
    <xsl:template match="sub-article | response" mode="modal-contrib">
        <xsl:apply-templates select="front | front-stub" mode="modal-contrib"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="article-meta | front | front-stub" mode="modal-contrib">
        <xsl:if test="contrib-group/contrib or contrib-group/author-notes">
            <xsl:variable name="id"><xsl:apply-templates select="." mode="modal-id"></xsl:apply-templates></xsl:variable>
            <div class="modal fade ModalDefault ModalTutors" id="ModalTutors{$id}" tabindex="-1" role="dialog" aria-hidden="true">
                
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&#xd7;</span><span class="sr-only"><xsl:apply-templates select="." mode="interface">
                            <xsl:with-param name="text">Close</xsl:with-param>
                        </xsl:apply-templates></span></button>
                        <h4 class="modal-title">
                            <xsl:apply-templates select="contrib-group" mode="about-the-contrib-group-button-text"/>
                        </h4>
                    </div>
                    <div class="modal-body">
                        <div class="info">
                            <xsl:apply-templates select="contrib-group/contrib" mode="modal-contrib"></xsl:apply-templates>
                            <xsl:if test="not(contrib-group/contrib) and ../@article-type='translation'">
                                <xsl:apply-templates select="$article//article-meta/front/contrib-group/contrib" mode="modal-contrib"></xsl:apply-templates>
                            </xsl:if>
                        </div>
                        <xsl:apply-templates select=".//author-notes" mode="modal-contrib"></xsl:apply-templates>
                    </div>
                </div>
            </div>
            </div>
            <xsl:apply-templates select="." mode="modal-scimago">
                <xsl:with-param name="id" select="$id"/>
            </xsl:apply-templates>
        </xsl:if>
    </xsl:template>

    <xsl:template match="article-meta | front | front-stub" mode="modal-scimago">
        <xsl:param name="id"/>
        <!-- modal com as instituições scimago -->
        <div class="modal fade ModalDefault ModalTutors" id="ModalScimago{$id}" tabindex="-1" role="dialog" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&#xd7;</span><span class="sr-only"><xsl:apply-templates select="." mode="interface">
                            <xsl:with-param name="text">Close</xsl:with-param>
                        </xsl:apply-templates></span></button>
                        <h4 class="modal-title">
                            SCIMAGO INSTITUTIONS RANKINGS
                        </h4>
                    </div>
                    <div class="modal-body">
                        <div class="info">
                            <xsl:apply-templates select="aff" mode="modal-scimago"/>
                            <xsl:if test="not(aff) and ../@article-type='translation'">
                                <xsl:apply-templates select="$article//article-meta/front/aff" mode="modal-scimago"/>
                            </xsl:if>
                        </div>
                    </div>
                </div>
            </div>
        </div>
     </xsl:template>
    
    <xsl:template match="contrib" mode="modal-contrib-type">
        <xsl:if test="@contrib-type!='author'">
        <xsl:apply-templates select="." mode="text-labels">
            <xsl:with-param name="text"><xsl:value-of select="@contrib-type"/></xsl:with-param>
        </xsl:apply-templates><br/>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="contrib" mode="modal-contrib">
        <div class="tutors">
            <xsl:apply-templates select="." mode="modal-contrib-type"/>
            <strong><xsl:apply-templates select="anonymous|name|collab|on-behalf-of"/></strong>
            <xsl:if test="xref[@ref-type='corresp']">
                <xsl:apply-templates select="xref[@ref-type='corresp']" />
            </xsl:if>
            <br/>
            <xsl:apply-templates select="role"/>
            <xsl:apply-templates select="xref" mode="modal-contrib"/>
            <xsl:apply-templates select="author-notes"/>
            <xsl:if test="contrib-id">
                <ul class="md-list inline">
                    <xsl:apply-templates select="contrib-id" mode="list-item"></xsl:apply-templates>
                </ul>
            </xsl:if>
            <div class="clearfix"></div>
        </div>
    </xsl:template>
    
    <xsl:template match="anonymous">
        <xsl:apply-templates select="." mode="interface">
            <xsl:with-param name="text">Anonymous</xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="contrib/xref" mode="modal-contrib">
        <xsl:variable name="rid" select="@rid"/>
            <xsl:apply-templates select="$article//aff[@id=$rid]" mode="modal-contrib"/>
        <xsl:apply-templates select="$article//fn[@id=$rid]" mode="xref"/>
    </xsl:template>
    
    <xsl:template match="aff" mode="modal-contrib">
        <div>
            <span data-aff-display="{@id}">
                <xsl:apply-templates select="." mode="display"/>
            </span>
            <xsl:apply-templates select="." mode="hidden-for-scimago"/>
        </div>
    </xsl:template>

    <xsl:template match="aff" mode="modal-scimago">
        <div>
            <span data-aff-display="{@id}">
                <xsl:apply-templates select="." mode="display"/>
            </span>
            <xsl:apply-templates select="." mode="hidden-for-scimago"/>
        <br/>
        </div>
    </xsl:template>

    <xsl:template match="aff" mode="hidden-for-scimago">
        <span data-aff-orgname="{@id}" hidden="">
            <xsl:apply-templates select="." mode="hidden-for-scimago-orgname"/>
        </span>
        <span data-aff-country="{@id}" hidden="">
            <xsl:apply-templates select=".//country"/>
        </span>
        <span data-aff-country-code="{@id}" hidden="">
            <xsl:apply-templates select=".//country/@country"/>
        </span>
        <span data-aff-location="{@id}" hidden="">
            <xsl:apply-templates select="." mode="hidden-for-scimago-location"/>
        </span>
        <span data-aff-full="{@id}" hidden="">
            <xsl:apply-templates select="." mode="display"/>
        </span>
        <a href="" class="scimago-link" data-scimago-link="{@id}"/>
    </xsl:template>

    <xsl:template match="aff" mode="hidden-for-scimago-orgname">
        <xsl:choose>
            <xsl:when
                test="institution[@content-type='orgname']">
                <xsl:value-of select="institution[@content-type='orgname']"/>
            </xsl:when>
            <xsl:when test="institution[@content-type='original']">
                <xsl:apply-templates select="institution[@content-type='original']"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="institution" mode="insert-separator"/>
            </xsl:otherwise>
        </xsl:choose>        
    </xsl:template>

    <xsl:template match="aff" mode="hidden-for-scimago-location">
        <xsl:choose>
            <xsl:when test=".//*[@content-type='city'] and .//*[@content-type='state']">
                <xsl:apply-templates select=".//*[@content-type='city']"/>, <xsl:apply-templates select=".//*[@content-type='state']"/><xsl:if test="country">, </xsl:if><xsl:apply-templates select=".//country"/>
            </xsl:when>
            <xsl:when test=".//city and .//state">
                <xsl:apply-templates select=".//city"/>, <xsl:apply-templates select=".//state"/><xsl:if test="country">, </xsl:if><xsl:apply-templates select=".//country"/>
            </xsl:when>
            <xsl:when test=".//*[@content-type='city'] or .//city">
                <xsl:apply-templates select=".//*[@content-type='city']|.//city"/><xsl:if test="country">, </xsl:if><xsl:apply-templates select=".//country"/>
            </xsl:when>
            <xsl:when test=".//*[@content-type='state'] or .//state">
                <xsl:apply-templates select=".//*[@content-type='state']|.//state"/><xsl:if test="country">, </xsl:if><xsl:apply-templates select=".//country"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select=".//country"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="contrib-id" mode="list-item">
        <li>
            <xsl:apply-templates select="."></xsl:apply-templates>
        </li>
    </xsl:template>
    
    <xsl:template match="author-notes" mode="modal-contrib">
        <xsl:apply-templates select="*" mode="modal-contrib"/>
    </xsl:template>

    <xsl:template match="fn | corresp" mode="modal-contrib">
        <div class="ref-list">
            <ul class="refList footnote">
                <li>
                    <xsl:apply-templates select="*|text()" mode="modal-contrib-li-content"/>
                </li>
            </ul>
        </div>
    </xsl:template>

    <xsl:template match="*" mode="modal-contrib-li-content">
        <xsl:apply-templates select="."/>
    </xsl:template>

    <xsl:template match="fn/p | corresp/p" mode="modal-contrib-li-content">
        <div>
            <xsl:apply-templates select="*|text()"/>
        </div>
    </xsl:template>

    <xsl:template match="fn/label | corresp/label" mode="modal-contrib-li-content">
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

    <xsl:template match="fn/title | corresp/title" mode="modal-contrib-li-content">
        <h2><xsl:apply-templates select="*|text()"/></h2>
    </xsl:template>

    <xsl:template match="author-notes/corresp" mode="contrib-dropdown-menu">
      <div class="corresp">
        <xsl:apply-templates/>
      </div>
    </xsl:template>

</xsl:stylesheet>