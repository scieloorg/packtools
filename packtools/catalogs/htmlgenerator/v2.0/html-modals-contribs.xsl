<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">

    <xsl:template match="front | front-stub" mode="modal-id"><xsl:value-of select="../@id"/></xsl:template>
    <xsl:template match="article-meta | sub-article[@article-type='translation']/front | sub-article[@article-type='translation']/front-stub" mode="modal-id">    
    </xsl:template>
    
    <xsl:variable name="xref_fn" select="$article//xref[@ref-type='fn']"></xsl:variable>
    
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
        <xsl:apply-templates select=".//sub-article[@article-type!='translation' and  @xml:lang=$TEXT_LANG]| .//response[@xml:lang=$TEXT_LANG]" mode="modal-contrib"></xsl:apply-templates>            
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
                            <xsl:apply-templates select="." mode="interface">
                                <xsl:with-param name="text">About the author<xsl:if test="count(contrib-group/contrib[@contrib-type='author'])&gt;1">s</xsl:if></xsl:with-param>
                            </xsl:apply-templates>
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
        </xsl:if>    
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
        <xsl:apply-templates select="." mode="display"/>
        <xsl:apply-templates select="." mode="hidden-for-scimago"/>
        </div>
    </xsl:template>

    <xsl:template match="aff" mode="hidden-for-scimago">
        <span class="hidden-aff-orgname" data-scimago="hidden_aff_orgname_{@id}" hidden="">
            <xsl:apply-templates select="." mode="hidden-for-scimago-orgname"/>
        </span>

        <span class="hidden-aff-location" data-scimago="hidden_aff_location_{@id}" hidden="">
            <xsl:apply-templates select="." mode="hidden-for-scimago-location"/>
        </span>
        
        <span class="hidden-aff-orgname" data-scimago="hidden_aff_full_{@id}" hidden="">
            <xsl:apply-templates select="." mode="hidden-for-scimago-orgname"/>, <xsl:apply-templates select="." mode="hidden-for-scimago-location"/>
        </span>
        <a href="" class="scimago-link" data-scimago="scimago_link_{@id}"/>
    </xsl:template>

    <xsl:template match="aff" mode="hidden-for-scimago-orgname">
        <xsl:variable name="text"><xsl:apply-templates select="text()"/></xsl:variable>
        <!--
        <xsl:comment> $text: <xsl:value-of select="$text"/> </xsl:comment>
        <xsl:comment> text(): <xsl:apply-templates select="text()"></xsl:apply-templates></xsl:comment>
        -->

        <xsl:choose>
            <xsl:when
                test="institution[@content-type='orgname']">
                <!--
                <xsl:comment> $text </xsl:comment>
                -->
                <xsl:value-of select="institution[@content-type='orgname']"/>
            </xsl:when>
            <xsl:when test="institution[@content-type='original']">
                <!--
                <xsl:comment> aff original </xsl:comment>
                -->
                <xsl:apply-templates select="institution[@content-type='original']"/>
            </xsl:when>
            <xsl:when
                test="*[name()!='label']">
                <!--
                <xsl:comment> aff insert separator </xsl:comment>
                -->
                <xsl:apply-templates select="*[name()!='label']" mode="insert-separator"/>
            </xsl:when>
            <xsl:otherwise>
                <!--
                <xsl:comment> $text </xsl:comment>
                -->
                <xsl:value-of select="$text"/>
            </xsl:otherwise>
        </xsl:choose>
        
    </xsl:template>

    <xsl:template match="aff" mode="hidden-for-scimago-location">
        <xsl:apply-templates select=".//city | .//*[@content-type='city']"/>, <xsl:apply-templates select=".//state | .//*[@content-type='state']"/>, <xsl:apply-templates select=".//country"/>
    </xsl:template>

    <xsl:template match="contrib-id" mode="list-item">
        <li>
            <xsl:apply-templates select="."></xsl:apply-templates>
        </li>
    </xsl:template>
    
    <xsl:template match="author-notes" mode="modal-contrib">
        <xsl:apply-templates select="*|text()" mode="modal-contrib"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="author-notes/*" mode="modal-contrib">
        <div class="info">
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </div>
    </xsl:template>
    
    <xsl:template match="author-notes//label">
        <xsl:choose>
            <xsl:when test="string-length(normalize-space(text())) = 1">
                <xsl:apply-templates select="*|text()"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <h3><xsl:apply-templates select="*|text()"></xsl:apply-templates></h3>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <!--xsl:template match="author-notes//fn" mode="modal-contrib">
        <xsl:variable name="id" select="@id"></xsl:variable>
        <xsl:if test="not($xref_fn[@rid=$id])">
            <div class="info">
                <xsl:apply-templates select="*|text()" mode="modal-contrib"></xsl:apply-templates>
            </div>
        </xsl:if>
    </xsl:template-->

    <xsl:template match="author-notes/corresp" mode="contrib-dropdown-menu">
      <div class="corresp">
        <xsl:apply-templates/>
      </div>
    </xsl:template>

</xsl:stylesheet>