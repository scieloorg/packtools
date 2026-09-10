<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/article-meta-contrib.xsl"/>

    <xsl:template match="article-meta/contrib-group | front/contrib-group | front-stub/contrib-group" mode="contrib-group-title">
        <xsl:variable name="type">
            <xsl:choose>
                <xsl:when test="../../@article-type='reviewer-report'">reviewer</xsl:when>
                <xsl:when test="not(contrib[1]/@contrib-type)">author</xsl:when>
                <xsl:otherwise><xsl:value-of select="contrib[1]/@contrib-type"/></xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <xsl:variable name="plural"><xsl:if test="number(count(contrib[@contrib-type=$type]))&gt;1">s</xsl:if></xsl:variable>
        <xsl:choose>
            <!--
                Chaves fechadas para os tipos de contrib mais comuns, para que o catálogo
                consiga traduzi-las. Para um contrib-type fora dessa lista, mantém-se o
                texto dinâmico (sempre em inglês, pois não há como catalogar um vocabulário
                aberto).
            -->
            <xsl:when test="$type='author' or $type='reviewer'">
                <xsl:apply-templates select="." mode="interface">
                    <xsl:with-param name="text">about-the-<xsl:value-of select="$type"/><xsl:value-of select="$plural"/></xsl:with-param>
                </xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>About the <xsl:value-of select="$type"/><xsl:value-of select="$plural"/></xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="article | sub-article" mode="contrib-group">
        <div>
            <xsl:attribute name="class">scielo__contribGroup</xsl:attribute>
            <xsl:variable name="id"><xsl:value-of select="@id"/></xsl:variable>
            <ul class="author-list" id="authorList-{$id}">
                <xsl:attribute name="aria-label">
                    <xsl:apply-templates select="." mode="interface">
                        <xsl:with-param name="text">Lista de autores</xsl:with-param>
                    </xsl:apply-templates>
                </xsl:attribute>
                <xsl:apply-templates select="front | front-stub" mode="contrib-group"/>
            </ul>
        </div>
    </xsl:template>

    <xsl:template match="contrib-group" mode="about-the-contrib-group-button">
        <xsl:param name="id"/>
        <!--
            Adiciona o botão 'About the contributor', trocando 'author',
            pelo tipo de contribuição
        -->
        <xsl:if test="contrib/*[name()!='name' and name()!='collab']">
            <a href="" class="btn btn-secondary btn-sm outlineFadeLink"
                data-bs-toggle="modal"
                data-bs-target="#ModalTutors{$id}">
                <xsl:apply-templates select="." mode="contrib-group-title"/>
            </a>
        </xsl:if>
    </xsl:template>

    <xsl:template match="front | front-stub" mode="scimago-button">
        <xsl:param name="id"/>
        <!--
            Adiciona o botão 'SCIMAGO INSTITUTIONS RANKINGS'
        -->
        <xsl:if test=".//aff">
            <a href="" class="btn btn-secondary btn-sm outlineFadeLink"
                data-bs-toggle="modal"
                data-bs-target="#ModalScimago{$id}">SCIMAGO INSTITUTIONS RANKINGS</a>
        </xsl:if>
    </xsl:template>

    <xsl:template match="contrib" mode="article-meta-contrib">
        <xsl:variable name="id">
            <xsl:value-of select="position()"/>
        </xsl:variable>
        <div class="dropdown">
            <button id="contribGroupTutor{$id}">
                <xsl:attribute name="class">btn btn-secondary dropdown-toggle</xsl:attribute>
                <xsl:attribute name="type">button</xsl:attribute>
                <xsl:attribute name="data-bs-toggle">dropdown</xsl:attribute>
                <xsl:attribute name="aria-expanded">false</xsl:attribute>
                <xsl:choose>
                    <xsl:when test="$ABBR_CONTRIB='true'">
                        <xsl:apply-templates select="name|collab|on-behalf-of" mode="abbrev"/>
                    </xsl:when>
                    <xsl:otherwise><xsl:apply-templates select="name|collab|on-behalf-of"/></xsl:otherwise>
                </xsl:choose>
            </button>
             <xsl:apply-templates select="." mode="contrib-dropdown-menu">
                 <xsl:with-param name="id">
                     <xsl:value-of select="$id"/>
                 </xsl:with-param>
             </xsl:apply-templates>
        </div>
    </xsl:template>


    <xsl:template match="contrib" mode="contrib-dropdown-menu">
        <xsl:param name="id"/>
        <xsl:if test="role or xref or contrib-id or bio">
            <ul class="dropdown-menu" role="menu" aria-labelledby="contribGrupoTutor{$id}">
                <xsl:apply-templates select="." mode="contrib-dropdown-menu-general"/>
                <xsl:apply-templates select="xref[@ref-type='corresp']" mode="contrib-dropdown-menu-corresp"/>
            </ul>
        </xsl:if>
    </xsl:template>

    <xsl:template match="contrib" mode="contrib-dropdown-menu-general">
        <xsl:if test="role or xref[@ref-type!='corresp'] or contrib-id or bio">
            <li>
                <xsl:apply-templates select="role | bio"/>
                <xsl:apply-templates select="xref[@ref-type!='corresp']" mode="contrib-dropdown-menu"/>
                <xsl:apply-templates select="contrib-id"/>
            </li>
        </xsl:if>
    </xsl:template>

    <xsl:template match="*" mode="contrib-dropdown-menu-corresp">
        <xsl:apply-templates select="*|text()"/>
    </xsl:template>

    <xsl:template match="xref[@ref-type='corresp']" mode="contrib-dropdown-menu-corresp">
        <xsl:variable name="rid"><xsl:value-of select="@rid"/></xsl:variable>
        <!--
            <li><div class="corresp"> <h3><sup>4</sup></h3> Autor para correspondência: <a href="mailto:author@gmail.com">author@gmail.com</a> </div></li>
        -->

        <li>
            <xsl:apply-templates select="$article//*[@id=$rid]" mode="contrib-dropdown-menu-corresp"/>
        </li>
    </xsl:template>    

    <xsl:template match="author-notes/corresp" mode="contrib-dropdown-menu-corresp">
        <div class="corresp">
            <xsl:apply-templates select="*|text()"/>
        </div>
    </xsl:template>

    <xsl:template match="front | front-stub" mode="contrib-group">
        <xsl:variable name="id"><xsl:value-of select="../@id"/></xsl:variable>

        <xsl:apply-templates select=".//contrib-group" mode="contrib-group">
            <xsl:with-param name="id"><xsl:value-of select="$id"/></xsl:with-param>
        </xsl:apply-templates>

        <xsl:apply-templates select="." mode="scimago-button">
            <xsl:with-param name="id"><xsl:value-of select="$id"/></xsl:with-param>
        </xsl:apply-templates>

        <!-- -->
        <xsl:if test="not(.//contrib-group) and ../@article-type='translation'">
            <xsl:apply-templates select="../..//front" mode="contrib-group"/>
        </xsl:if>
        
    </xsl:template>

    <xsl:template match="contrib-group" mode="contrib-group">
        <xsl:param name="id"/>

        <xsl:variable name="contrib_names" select="contrib[not(@id)]"/>
        <xsl:variable name="total_contribs"><xsl:value-of select="count(contrib)"/></xsl:variable>
        <xsl:variable name="total_contrib_names"><xsl:value-of select="count($contrib_names)"/></xsl:variable>

        <xsl:choose>
            <xsl:when test="$total_contribs &lt; $MAX_DISPLAYED_AUTHORS + 1">
                <xsl:apply-templates select="$contrib_names" mode="contrib-list-item">
                    <xsl:with-param name="id"><xsl:value-of select="$id"/></xsl:with-param>
                    <xsl:with-param name="sep">,</xsl:with-param>
                    <xsl:with-param name="skip_last_sep">true</xsl:with-param>
                </xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="$contrib_names[position()&lt;3]" mode="contrib-list-item">
                    <xsl:with-param name="id"><xsl:value-of select="$id"/></xsl:with-param>
                    <xsl:with-param name="index">1</xsl:with-param>
                    <xsl:with-param name="sep">,</xsl:with-param>
                </xsl:apply-templates>

                <li>    
                    <details class="authors-collapse">
                        <summary>
                            <span class="authors-collapse__open">
                                + <xsl:value-of select="$total_contrib_names - 3"/>
                                <xsl:text>&#160;</xsl:text>
                                <xsl:apply-templates select="." mode="interface">
                                    <xsl:with-param name="text">autores</xsl:with-param>
                                </xsl:apply-templates>
                            </span>
                            <span class="authors-collapse__close">
                                <xsl:apply-templates select="." mode="interface">
                                    <xsl:with-param name="text">ocultar autores</xsl:with-param>
                                </xsl:apply-templates>
                            </span>
                        </summary>
                        <ul class="author-list__hidden">
                            <xsl:attribute name="aria-label">
                                <xsl:apply-templates select="." mode="interface">
                                    <xsl:with-param name="text">Autores intermediários</xsl:with-param>
                                </xsl:apply-templates>
                            </xsl:attribute>
                            <xsl:for-each select="$contrib_names[position()&gt;2 and position()&lt;$total_contrib_names]">
                                <xsl:apply-templates select="." mode="contrib-list-item">
                                    <xsl:with-param name="id"><xsl:value-of select="$id"/></xsl:with-param>
                                    <xsl:with-param name="index"><xsl:value-of select="position()+2"/></xsl:with-param>
                                    <xsl:with-param name="sep">,</xsl:with-param>
                                </xsl:apply-templates>
                            </xsl:for-each>
                        </ul>
                    </details>
                </li>

                <xsl:apply-templates select="$contrib_names[position()=$total_contrib_names]" mode="contrib-list-item">
                    <xsl:with-param name="id"><xsl:value-of select="$id"/></xsl:with-param>
                    <xsl:with-param name="index"><xsl:value-of select="$total_contrib_names"/></xsl:with-param>
                    <xsl:with-param name="sep"><xsl:if test="$total_contrib_names!=$total_contribs">,</xsl:if></xsl:with-param>
                </xsl:apply-templates>

            </xsl:otherwise>
        </xsl:choose>
        <xsl:if test="$total_contrib_names!=$total_contribs">
            <xsl:apply-templates select="contrib[@id]" mode="contrib-list-item">
                <xsl:with-param name="id"><xsl:value-of select="$id"/></xsl:with-param>
                <xsl:with-param name="index"><xsl:value-of select="$total_contribs"/></xsl:with-param>
                <xsl:with-param name="sep"></xsl:with-param>
            </xsl:apply-templates>
        </xsl:if>
    </xsl:template>

    <xsl:template match="contrib-group[@content-type='collab-list']" mode="contrib-group">
        <xsl:param name="id"/>
        <!--
            Remove a apresentação dos autores, deixando apenas o botão "sobre os autores
        <xsl:apply-templates select="contrib[@contrib-type='author']" mode="article-meta-contrib"/>
        -->
        <xsl:variable name="total">
            <xsl:value-of select="count(contrib)"/>
        </xsl:variable>

        <li>    
            <details class="authors-collapse">
                <summary>
                    <span class="authors-collapse__open">
                        <xsl:value-of select="count(contrib)"/>
                        <xsl:text>&#160;</xsl:text>
                        <xsl:apply-templates select="." mode="interface">
                            <xsl:with-param name="text">group members</xsl:with-param>
                        </xsl:apply-templates>
                    </span>
                    <span class="authors-collapse__close">
                        <xsl:apply-templates select="." mode="interface">
                            <xsl:with-param name="text">ocultar collab list</xsl:with-param>
                        </xsl:apply-templates>
                    </span>
                </summary>
                <ul class="author-list__hidden">
                    <xsl:attribute name="aria-label">
                        <xsl:apply-templates select="." mode="interface">
                            <xsl:with-param name="text">Autores intermediários</xsl:with-param>
                        </xsl:apply-templates>
                    </xsl:attribute>
                    <xsl:apply-templates select="contrib" mode="contrib-list-item">
                        <xsl:with-param name="id"><xsl:value-of select="@content-type"/><xsl:value-of select="$id"/></xsl:with-param>
                        <xsl:with-param name="sep">,</xsl:with-param>
                        <xsl:with-param name="skip_last_sep">true</xsl:with-param>
                    </xsl:apply-templates>
                </ul>
            </details>
        </li>
    </xsl:template>

    <xsl:template match="contrib" mode="contrib-list-item">
        <xsl:param name="id"/>
        <xsl:param name="index"/>
        <xsl:param name="sep"/>
        <xsl:param name="skip_last_sep"/>

        <xsl:variable name="author-name">
            <xsl:apply-templates select="name|collab|on-behalf-of"/>
        </xsl:variable>

        <xsl:variable name="position">
            <xsl:choose>
                <xsl:when test="$index"><xsl:value-of select="$index"/></xsl:when>
                <xsl:otherwise><xsl:value-of select="position()"/></xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <li class="author-item">
            <xsl:apply-templates select="xref[@ref-type='corresp']|xref[@ref-type='aff']" mode="email-icon"/>
            <button
                type="button"
                class="btn-link px-0 author-name-trigger"
                data-bs-toggle="modal"
                data-author-index="{$position - 1}"
                data-bs-target="#authorModal-{$id}-{$position}"
            >
                <xsl:attribute name="aria-label">
                    <xsl:apply-templates select="." mode="interface">
                        <xsl:with-param name="text">Abrir detalhes de </xsl:with-param>
                    </xsl:apply-templates>
                    <xsl:value-of select="$author-name"/>
                </xsl:attribute>
                <span><xsl:value-of select="$author-name"/></span>
            </button>
            <xsl:if test="not($skip_last_sep='true' and position()=last())">
                <span class="author-separator" aria-hidden="true"><xsl:value-of select="$sep"/></span>
            </xsl:if>
        </li>
    </xsl:template>
    
    <xsl:template match="corresp | aff" mode="email-icon">
        <xsl:if test="not(email)">
            <xsl:comment>email ausente para <xsl:value-of select="name()"/> (<xsl:value-of select="@id"/>)</xsl:comment>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="corresp[email] | aff[email]" mode="email-icon">
        <a href="mailto:{email}">
           <span class="material-icons-outlined me-1 fs-6" aria-hidden="true">mail</span>
        </a>
    </xsl:template>
    
    <xsl:template match="xref" mode="email-icon">
        <xsl:variable name="rid"><xsl:value-of select="@rid"/></xsl:variable>
        
        <xsl:apply-templates select="$article//corresp[@id=$rid] | $article//aff[@id=$rid]" mode="email-icon"/>
   </xsl:template>

</xsl:stylesheet>