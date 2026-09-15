<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/html-modals-contribs.xsl"/>

    <xsl:template match="article-meta | front-stub" mode="modal-contrib-group">
        <xsl:variable name="id"><xsl:apply-templates select="." mode="modal-id"></xsl:apply-templates></xsl:variable>
        <div class="modal fade ModalDefault ModalTutors" id="ModalTutors{$id}" tabindex="-1" role="dialog" aria-hidden="true">

            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <xsl:apply-templates select="." mode="contrib-group-title"/>
                        </h5>
                        <button class="btn-close" data-bs-dismiss="modal">
                            <xsl:attribute name="aria-label">
                                <xsl:apply-templates select="." mode="interface">
                                    <xsl:with-param name="text">Close</xsl:with-param>
                                </xsl:apply-templates>
                            </xsl:attribute>
                        </button>
                    </div>
                    <xsl:call-template name="modal-author-css"/>
                    <div class="modal-body">
                        <xsl:apply-templates select="." mode="contrib-group-body"/>
                        <xsl:apply-templates select=".//author-notes" mode="modal-contrib"></xsl:apply-templates>
                    </div>
                </div>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="article-meta | front-stub" mode="contrib-group-title">
        <xsl:choose>
            <xsl:when test="contrib-group">
                <xsl:apply-templates select="contrib-group" mode="contrib-group-title"/>
            </xsl:when>
            <xsl:when test="../@article-type='translation'">
                <xsl:apply-templates select="../../front/article-meta | ../../front-stub" mode="contrib-group-title"/>
            </xsl:when>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="article-meta | front-stub" mode="contrib-group-body">
        <xsl:choose>
            <xsl:when test="contrib-group">
                <xsl:apply-templates select="contrib-group/contrib" mode="modal-contrib"/>
            </xsl:when>
            <xsl:when test="../@article-type='translation'">
                <!-- sem contrib-group própria: usa a do front/front-stub do artigo pai, mesmo comportamento do article/front -->
                <xsl:apply-templates select="../../front/article-meta/contrib-group/contrib | ../../front-stub/contrib-group/contrib" mode="modal-contrib"/>
            </xsl:when>
        </xsl:choose>
    </xsl:template>

    <xsl:template name="modal-author-css">
        <style>
            .author-card {
                border-bottom: 1px solid #ccc;
                padding: 1rem 0;
            }
            .author-card:last-child {
                border-bottom: 0px;
            }
            .author-name {
                font-weight: 600;
            }
            
            .orcid-button {
                padding-left: 2.5rem;
            }
            .modal-body {
                padding-bottom: 3rem;
            }
            .orcid-button::before {
                content: "";
                position: absolute;
                background-image: url(https://ds.scielo.org/img/logo-orcid.svg);
                background-repeat: no-repeat;
                background-size: 1.5em auto;
                background-position: .5em center;
                display: block;
                width: 60px;
                height: 60px;
                top: -10px;
                left: 0;
            }
        </style>
    </xsl:template>

    <xsl:template match="article-meta | front-stub" mode="modal-contrib-group">
        <xsl:variable name="id"><xsl:apply-templates select="." mode="modal-id"></xsl:apply-templates></xsl:variable>
        <xsl:choose>
            <xsl:when test="contrib-group">
                <xsl:apply-templates select="contrib-group" mode="modal-contrib-group">
                    <xsl:with-param name="id"><xsl:value-of select="$id"/></xsl:with-param>
                </xsl:apply-templates>
            </xsl:when>
            <xsl:when test="../@article-type='translation'">
                <xsl:apply-templates select="../../front/article-meta | ../../front-stub" mode="modal-contrib-group"/>
            </xsl:when>
        </xsl:choose>
    </xsl:template>
 
    <xsl:template match="contrib-group" mode="modal-contrib-group">
        <xsl:param name="id"/>
        <xsl:apply-templates select="contrib" mode="modal-contrib">
            <xsl:with-param name="id"><xsl:value-of select="@content-type"/><xsl:value-of select="$id"/></xsl:with-param>
            <xsl:with-param name="title"><xsl:apply-templates select="." mode="contrib-group-title"/></xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>
 
    <xsl:template match="article-meta | front-stub" mode="modal-scimago">
        <xsl:variable name="id"><xsl:apply-templates select="." mode="modal-id"></xsl:apply-templates></xsl:variable>
        <div class="modal fade ModalDefault ModalTutors" id="ModalScimago{$id}" tabindex="-1" role="dialog" aria-hidden="true">
                
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            SCImago Institutions Rankings
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
                            <xsl:apply-templates select=".//aff" mode="modal-scimago"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="contrib" mode="modal-contrib">
        <!--
            ((contrib-id)*, (anonymous | collab | collab-alternatives | name | name-alternatives | string-name)*, (degrees)*, (address | aff | aff-alternatives | author-comment | bio | email | ext-link | on-behalf-of | role | uri | xref)*)
        -->
        
        <div class="author-card">
            <div class="author-name">
                <span class="material-icons-outlined">person</span>
                <xsl:apply-templates select="anonymous|name|collab|on-behalf-of"/>
                <xsl:apply-templates select="xref[@ref-type='corresp']"/>
            </div>
            <div class="author-roles ms-4 mb-2 scielo__text-color__subtle--light">
                <xsl:apply-templates select="role | bio" mode="modal-contrib"/>
            </div>
            <div class="author-institution ms-4 mb-2 scielo__text-color__subtle--light">
                <xsl:apply-templates select="xref" mode="modal-contrib"/>
            </div>
            <div class="ms-4">
                <xsl:apply-templates select="contrib-id" mode="modal-contrib"/>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="contrib/xref" mode="modal-contrib">
        <xsl:variable name="rid" select="@rid"/>
        <xsl:apply-templates select="$article//aff[@id=$rid]" mode="modal-contrib"/>
        <xsl:apply-templates select="$article//*[@id=$rid]" mode="modal-contrib"/>
    </xsl:template>
    
    <xsl:template match="role" mode="modal-contrib">
        <xsl:choose>
            <xsl:when test="position()=1"></xsl:when>
            <xsl:otherwise> · </xsl:otherwise>
        </xsl:choose><xsl:value-of select="."/>
    </xsl:template>

    <xsl:template match="aff" mode="modal-contrib">
        <span class="material-icons-outlined">school</span>
        <span data-aff-display="{@id}">
            <xsl:apply-templates select="." mode="display"/>
        </span>
        <xsl:apply-templates select="." mode="hidden-for-scimago"/>
    </xsl:template>
    
    <xsl:template match="contrib-id" mode="modal-contrib">
        <xsl:variable name="access_text">
            <xsl:apply-templates select="." mode="interface">
                <xsl:with-param name="text">access_contributor</xsl:with-param>
            </xsl:apply-templates>
        </xsl:variable>
        <xsl:variable name="new_tab_text">
            <xsl:apply-templates select="." mode="interface">
                <xsl:with-param name="text">opens_new_tab</xsl:with-param>
            </xsl:apply-templates>
        </xsl:variable>
        <xsl:variable name="external_resource_text">
            <xsl:apply-templates select="." mode="interface">
                <xsl:with-param name="text">external_resource</xsl:with-param>
            </xsl:apply-templates>
        </xsl:variable>
        <xsl:variable name="contributor_url">
            <xsl:apply-templates select="." mode="url"/><xsl:value-of select="."/>
        </xsl:variable>
        <xsl:variable name="aria_label">
            <xsl:value-of select="$access_text"/>
            <xsl:text> </xsl:text>
            <xsl:value-of select="."/>
            <xsl:text>. </xsl:text>
            <xsl:value-of select="$new_tab_text"/>
            <xsl:text>. </xsl:text>
            <xsl:value-of select="$external_resource_text"/>
            <xsl:text>.</xsl:text>
        </xsl:variable>
        <a target="_blank" class="btn btn-secondary  {@contrib-id-type}-button" href="{$contributor_url}" aria-label="{normalize-space($aria_label)}">
            <xsl:value-of select="."/>
        </a>
    </xsl:template>

    <xsl:template match="author-notes/*" mode="modal-contrib">
        <xsl:apply-templates select="*|text()"/>
    </xsl:template>

    <xsl:template match="author-notes/fn/label" mode="modal-contrib">
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

    <xsl:template match="author-notes/fn/label[sup]" mode="modal-contrib">
        <strong><xsl:apply-templates select="*|text()"/></strong>
    </xsl:template>

    <xsl:template match="author-notes/fn" mode="modal-contrib">
        <div>
            <xsl:apply-templates select="." mode="author-notes-fn-class"/>
            <xsl:apply-templates select="*|text()" mode="modal-contrib"/>
        </div>
    </xsl:template>

    <xsl:template match="author-notes/fn" mode="author-notes-fn-class">
        <xsl:attribute name="class">mb-3</xsl:attribute>
    </xsl:template>

    <xsl:template match="author-notes/fn[@fn-type='con']" mode="author-notes-fn-class">
        <xsl:attribute name="class">author-contributions mb-3</xsl:attribute>
    </xsl:template>

    <xsl:template match="author-notes/fn[@fn-type='con']/label" mode="modal-contrib">
        <strong><span class="material-icons-outlined">groups</span> <xsl:apply-templates select="."/></strong>
    </xsl:template>

    <xsl:template match="author-notes/fn/p | author-notes/fn/text()" mode="modal-contrib">
        <p class="scielo__text-color__subtle--light mb-0">
            <xsl:apply-templates select="."/>
        </p>
    </xsl:template>

    <xsl:template match="author-notes/corresp" mode="modal-contrib">
        <xsl:variable name="id"><xsl:value-of select="@id"/></xsl:variable>
        <a class="" name="{@id}_ref"/>
        <div class="correspondence mt-3 mb-4">
            <xsl:apply-templates select="*|text()" mode="modal-contrib"/>
        </div>
    </xsl:template>

    <xsl:template match="author-notes/corresp/label" mode="modal-contrib">
        <strong>
            <span class="material-icons-outlined">
                <xsl:choose>
                    <xsl:when test="contains(., 'mail')">email</xsl:when>
                    <xsl:otherwise>person</xsl:otherwise>
                </xsl:choose>
            </span><xsl:value-of select="."/>
        </strong>
    </xsl:template>

    <xsl:template match="author-notes/corresp/text()" mode="modal-contrib">
        <xsl:choose>
            <xsl:when test="normalize-space(.)!=''">
                <span class="scielo__text-color__subtle--light">
                    <xsl:value-of select="."/>
                </span><br/>
            </xsl:when>
            <xsl:when test="contains(., 'mail')">1
                <strong><span class="material-icons-outlined">email</span> </strong>
            </xsl:when>
            <xsl:otherwise><xsl:value-of select="."/></xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="text()" mode="corresp-texts">
        <xsl:value-of select="."/>
    </xsl:template>

    <xsl:template match="author-notes/corresp/email" mode="modal-contrib">
        <xsl:variable name="text"><xsl:apply-templates select="..//text()" mode="corresp-texts"/></xsl:variable>
        <xsl:choose>
            <xsl:when test="contains($text, 'mail')">
                <xsl:apply-templates select="."/>
            </xsl:when>
            <xsl:otherwise>
                <strong><span class="material-icons-outlined">email</span> </strong><xsl:apply-templates select="."/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="contrib" mode="modal-contrib">
        <xsl:param name="id"/>
        <xsl:param name="notes"/>
        <xsl:param name="title"/>
        <xsl:variable name="position" select="position()"/>        
        <xsl:variable name="id_position"><xsl:value-of select="$id"/>-<xsl:value-of select="$position"/></xsl:variable>

        <div class="modal fade ModalDefault ModalTutors" id="authorModal-{$id_position}" tabindex="-1" role="dialog"
       aria-labelledby="authorModalLabel-{$id_position}" aria-hidden="true">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="h4 modal-title" id="authorModalLabel-{$id_position}">
                            <xsl:value-of select="$title"/>
                        </h5>
                        <button
                            type="button"
                            class="btn-close"
                            data-bs-dismiss="modal">
                            <xsl:attribute name="aria-label">
                                <xsl:apply-templates select="." mode="interface">
                                    <xsl:with-param name="text">Close</xsl:with-param>
                                </xsl:apply-templates>
                            </xsl:attribute>
                        </button>
                    </div>
                    <div class="modal-body">
                        <xsl:apply-templates select="." mode="modal-contrib-body"/>
                    </div>
                </div>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="contrib" mode="modal-contrib-body">
        <!--
            ((contrib-id)*, (anonymous | collab | collab-alternatives | name | name-alternatives | string-name)*, (degrees)*, (address | aff | aff-alternatives | author-comment | bio | email | ext-link | on-behalf-of | role | uri | xref)*)
        -->
        <div class="author-card">
            <div class="author-grid-row">
                <span class="material-icons-outlined" aria-hidden="true">person</span>
                <div class="author-name">
                    <span class="author-name-text">
                        <xsl:apply-templates select="anonymous|name|collab|on-behalf-of"/>
                    </span>
                </div>
            </div>
            <xsl:apply-templates select="." mode="modal-contrib-body-role"/>
            <xsl:apply-templates select="." mode="modal-contrib-body-aff"/>
            <xsl:apply-templates select="." mode="modal-contrib-body-contrib-id"/>
        </div>
    </xsl:template>

    <xsl:template match="contrib" mode="modal-contrib-body-contrib-id">
        <xsl:apply-templates select="contrib-id" mode="modal-contrib-body-contrib-id"/>
    </xsl:template>

    <xsl:template match="contrib-id" mode="modal-contrib-body-contrib-id">
        <xsl:variable name="id_type" select="@contrib-id-type"/>
        <div class="{$id_type}-button-wrap ms-4">
            <xsl:value-of select="."/>
        </div>
    </xsl:template>

    <xsl:template match="contrib-id[@contrib-id-type='orcid']" mode="modal-contrib-body-contrib-id">
        <div class="orcid-button-wrap ms-4">
            <a 
            target="_blank" 
            rel="noopener noreferrer" 
            class="btn btn-secondary orcid-button" 
            href="https://orcid.org/{.}"
            >
            <xsl:attribute name="aria-label">
                <xsl:apply-templates select="." mode="interface">
                    <xsl:with-param name="text">Access contributor profile</xsl:with-param>
                </xsl:apply-templates><xsl:text>&#160;</xsl:text><xsl:value-of select="."/>.
                <xsl:text>&#160;</xsl:text>
                <xsl:apply-templates select="." mode="interface">
                    <xsl:with-param name="text">Opens in new tab. External resource.</xsl:with-param>
                </xsl:apply-templates>
            </xsl:attribute>
            <xsl:value-of select="."/>
            </a>
        </div>
    </xsl:template>

    <xsl:template match="contrib" mode="modal-contrib-body-role">
        <xsl:if test="role">
            <div class="author-roles author-subrow mb-2">
                <xsl:apply-templates select="role" mode="modal-contrib-body-role"/>
            </div>
        </xsl:if>
    </xsl:template>

    <xsl:template match="role" mode="modal-contrib-body-role">
        <xsl:choose>
            <xsl:when test="position()=1"></xsl:when>
            <xsl:otherwise> · </xsl:otherwise>
        </xsl:choose><xsl:value-of select="."/>
    </xsl:template>

    <xsl:template match="contrib" mode="modal-contrib-body-aff">
        <xsl:if test="xref[@ref-type='aff']">
            <div class="author-grid-row author-subrow mb-2">
                <span class="material-icons-outlined" aria-hidden="true">school</span>
                <div class="author-institution">
                    <xsl:apply-templates select="xref[@ref-type='aff']" mode="modal-contrib-body-aff"/>
                </div>
            </div>
        </xsl:if>
    </xsl:template>

    <xsl:template match="xref[@ref-type='aff']" mode="modal-contrib-body-aff">
        <xsl:variable name="rid" select="@rid"/>
        <xsl:apply-templates select="$article//aff[@id=$rid]" mode="modal-contrib-body-aff"/>
    </xsl:template>

    <xsl:template match="aff" mode="modal-contrib-body-aff">
        <xsl:value-of select="institution[@content-type='original']"/>
        <xsl:if test="not(institution[@content-type='original'])">
            <xsl:apply-templates select="." mode="modal-contrib-body-aff-built"/>
        </xsl:if>
    </xsl:template>

    <xsl:template match="aff" mode="modal-contrib-body-aff-built">
        <xsl:apply-templates select="institution | addr-line | city | state | country" mode="display"/>
    </xsl:template>
</xsl:stylesheet>