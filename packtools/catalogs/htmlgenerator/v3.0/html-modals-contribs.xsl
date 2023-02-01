<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/html-modals-contribs.xsl"/>

    <xsl:template match="article-meta | front | front-stub" mode="modal-contrib">
        <xsl:if test="contrib-group/contrib or contrib-group/author-notes">
            <xsl:variable name="id"><xsl:apply-templates select="." mode="modal-id"></xsl:apply-templates></xsl:variable>
            <div class="modal fade ModalDefault ModalTutors" id="ModalTutors{$id}" tabindex="-1" role="dialog" aria-hidden="true">            
                
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                             <xsl:apply-templates select="." mode="interface">
                                 <xsl:with-param name="text">About the author<xsl:if test="count(contrib-group/contrib[@contrib-type='author'])&gt;1">s</xsl:if></xsl:with-param>
                             </xsl:apply-templates>
                        </h5>
                        <button class="btn-close" data-bs-dismiss="modal">
                            <xsl:attribute name="aria-label">
                                <xsl:apply-templates select="." mode="interface">
                                    <xsl:with-param name="text">Close</xsl:with-param>
                                </xsl:apply-templates>
                            </xsl:attribute>
                        </button>
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

    <xsl:template match="aff" mode="modal-contrib">
        <div>
        <xsl:apply-templates select="." mode="display"/>
        <xsl:apply-templates select="." mode="hidden-for-scimago"/>
        </div>
    </xsl:template>

    <xsl:template match="aff" mode="hidden-for-scimago">
        <xsl:variable name="text"><xsl:apply-templates select="text()"/></xsl:variable>
        <!--
        <xsl:comment> $text: <xsl:value-of select="$text"/> </xsl:comment>
        <xsl:comment> text(): <xsl:apply-templates select="text()"></xsl:apply-templates></xsl:comment>
        -->
        <span class="hidden-aff-orgname" id="hidden_aff_orgname_{@id}" hidden="">
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
        </span>
        <a href="" class="scimago-link" id="scimago_link_{@id}"/>
    </xsl:template>

    <xsl:template match="aff" mode="hidden-for-scimago">
        <xsl:apply-templates select="." mode="hidden-for-scimago-orgname"/>
        <xsl:apply-templates select="." mode="hidden-for-scimago-location"/>
        <a href="" class="scimago-link" id="scimago_link_{@id}"/>
    </xsl:template>

    <xsl:template match="aff" mode="hidden-for-scimago-orgname">
        <xsl:variable name="text"><xsl:apply-templates select="text()"/></xsl:variable>
        <!--
        <xsl:comment> $text: <xsl:value-of select="$text"/> </xsl:comment>
        <xsl:comment> text(): <xsl:apply-templates select="text()"></xsl:apply-templates></xsl:comment>
        -->
        <span class="hidden-aff-orgname" id="hidden_aff_orgname_{@id}" hidden="">
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
        </span>
    </xsl:template>

    <xsl:template match="aff" mode="hidden-for-scimago-location">
        <span class="hidden-aff-location" id="hidden_aff_location_{@id}" hidden="">
        <xsl:apply-templates select=".//city | .//*[@content-type='city']"/>, 
        <xsl:apply-templates select=".//state | .//*[@content-type='state']"/>, 
        <xsl:apply-templates select=".//country"/>
        </span>
    </xsl:template>

    <xsl:template match="author-notes/*" mode="modal-contrib">
        <div class="info">
            <xsl:apply-templates select="*|text()"/>
        </div>
    </xsl:template>

    <xsl:template match="author-notes/corresp" mode="modal-contrib">
        <xsl:variable name="id"><xsl:value-of select="@id"/></xsl:variable>
        <div class="corresp">
            <a class="" name="{@id}_ref"/>
            <xsl:apply-templates select="*|text()"/>
        </div>
    </xsl:template>

    <xsl:template match="author-notes//label">
        <xsl:variable name="text"><xsl:apply-templates select=".//text()"/></xsl:variable>
        <xsl:choose>
            <xsl:when test="contains('123456789',substring(normalize-space($text),1,1))">
                <sup><strong><xsl:apply-templates select="*|text()"/></strong></sup>
            </xsl:when>
            <xsl:otherwise>
                <strong><xsl:apply-templates select="*|text()"/></strong>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="author-notes//label[sup]">
        <strong><xsl:apply-templates select="*|text()"/></strong>
    </xsl:template>
</xsl:stylesheet>