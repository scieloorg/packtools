<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

    <xsl:variable name="howtocite_location"><xsl:choose>
        <xsl:when test=".//article-id[@pub-id-type='doi']">
            <xsl:apply-templates select=".//article-id[@pub-id-type='doi']" mode="how2cite-doi"/>
        </xsl:when>
        <xsl:when test="$URL_PERMLINK!=''">
            <xsl:value-of select="$URL_PERMLINK"/>
        </xsl:when>
        <xsl:when test="$URL_ARTICLE_PAGE!=''">
            <xsl:value-of select="$URL_ARTICLE_PAGE"/>
        </xsl:when>
    </xsl:choose></xsl:variable>

    <xsl:template match="*" mode="modal-how2cite">
        <div class="modal fade ModalDefault" id="ModalArticles" tabindex="-1" role="dialog"
            aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal">
                            <span aria-hidden="true">&#xd7;</span>
                            <span class="sr-only">
                                <xsl:apply-templates select="." mode="interface">
                                    <xsl:with-param name="text">Close</xsl:with-param>
                                </xsl:apply-templates>
                            </span>
                        </button>
                        <h4 class="modal-title">
                            <xsl:apply-templates select="." mode="text-labels">
                                <xsl:with-param name="text">How to cite</xsl:with-param>
                            </xsl:apply-templates>
                        </h4>
                    </div>
                    <div class="modal-body">
                        <p id="citation">
                        </p>
                        <input id="citationCut" type="text" value=""></input>
                        <a class="copyLink">
                            <xsl:attribute name="data-clipboard-target">#citationCut</xsl:attribute>
                            <span class="glyphBtn copyIcon"/> <xsl:apply-templates select="." mode="interface">
                                <xsl:with-param name="text">copy</xsl:with-param>
                            </xsl:apply-templates> </a>

                        <xsl:if test="$URL_DOWNLOAD_RIS!=''">
                            <div class="row" id="how2cite-export">
                                <div class="col-md-2 col-sm-2">
                                    <a
                                        href="{$URL_DOWNLOAD_RIS}"
                                        class="midGlyph download"> <xsl:apply-templates select="." mode="interface">
                                            <xsl:with-param name="text">ris format</xsl:with-param>
                                        </xsl:apply-templates> </a>
                                </div>
                            </div>
                        </xsl:if>
                    </div>
                </div>
            </div>
        </div>
        <xsl:variable name="citation"><xsl:apply-templates select="." mode="citation"/></xsl:variable>
        <script type="text/javascript">
            function currentDate() {
            var today = new Date();
            var months = [<xsl:apply-templates select="." mode="interface">
                <xsl:with-param name="text">'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'</xsl:with-param>
            </xsl:apply-templates>]
            today.setTime(today.getTime());
            return today.getDate() + " " + months[today.getMonth()] + " " + today.getFullYear();
            }
            var citation = '<xsl:value-of select="normalize-space($citation)"/>'.replace('CURRENTDATE', currentDate());
            document.getElementById('citation').innerHTML = citation;
            document.getElementById('citationCut').value = citation.replace('&amp;lt;', '<xsl:text>&lt;</xsl:text>').replace('&amp;gt;', "<xsl:text>&gt;</xsl:text>");
        </script>
    </xsl:template>

    <xsl:template match="article" mode="citation">
        <xsl:apply-templates select="front" mode="citation"></xsl:apply-templates>
    </xsl:template>

    <xsl:template match="front" mode="citation">
        <xsl:apply-templates select="." mode="how2cite-contrib"></xsl:apply-templates>
        <xsl:apply-templates select="." mode="how2cite-article-title"></xsl:apply-templates>
        <xsl:apply-templates select="." mode="how2cite-journal-title"></xsl:apply-templates>
        <xsl:if test="$howtocite_location!=''"> [online]</xsl:if>.
        <xsl:apply-templates select="." mode="how2cite-issue-info"></xsl:apply-templates>
        <xsl:apply-templates select="." mode="how2cite-current-date"></xsl:apply-templates>,
        <xsl:apply-templates select="." mode="how2cite-pages"></xsl:apply-templates>
        <xsl:apply-templates select="." mode="how2cite-available-from"></xsl:apply-templates>
        <xsl:apply-templates select="." mode="how2cite-epub-date"></xsl:apply-templates>
        <xsl:apply-templates select="." mode="how2cite-issn"></xsl:apply-templates>
        <xsl:apply-templates select="." mode="how2cite-doi"></xsl:apply-templates>
    </xsl:template>

    <xsl:template match="*" mode="how2cite-contrib">
        <xsl:apply-templates select=".//contrib-group" mode="how2cite-contrib"/>
    </xsl:template>

    <xsl:template match="contrib-group" mode="how2cite-contrib">
        <xsl:choose>
            <xsl:when test="count(contrib)=1">
                <xsl:apply-templates select="contrib" mode="how2cite-contrib">
                    <xsl:with-param name="sep"></xsl:with-param>
                </xsl:apply-templates>
            </xsl:when>
            <xsl:when test="count(contrib)&lt;=3">
                <xsl:apply-templates select="contrib" mode="how2cite-contrib">
                    <xsl:with-param name="sep"><xsl:apply-templates select="." mode="text-labels">
                        <xsl:with-param name="text">and</xsl:with-param>
                    </xsl:apply-templates></xsl:with-param>
                </xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="contrib[1]" mode="how2cite-contrib">

                </xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:if test="count(contrib)&gt;3">et al</xsl:if>.
    </xsl:template>

    <xsl:template match="contrib" mode="how2cite-contrib">
        <xsl:param name="sep"></xsl:param>
        <xsl:if test="position()!=1">
            <xsl:choose>
                <xsl:when test="position()!=last()">, </xsl:when>
                <xsl:otherwise>&#160;<xsl:value-of select="$sep"/>&#160;</xsl:otherwise>
            </xsl:choose>
        </xsl:if>
        <xsl:apply-templates select="name | collab" mode="how2cite-contrib"/>
    </xsl:template>

    <xsl:template match="name" mode="how2cite-contrib">
        <xsl:apply-templates select="surname"/>, <xsl:apply-templates select="given-names"/>
    </xsl:template>

    <xsl:template match="*" mode="how2cite-article-title">
        <xsl:choose>
            <xsl:when test=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]//article-title">
                <xsl:apply-templates select=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]//article-title"></xsl:apply-templates>.
            </xsl:when>
            <xsl:when test=".//trans-title-group[@xml:lang=$TEXT_LANG]//trans-title">
                <xsl:apply-templates select=".//trans-title-group[@xml:lang=$TEXT_LANG]//trans-title"></xsl:apply-templates>.
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select=".//article-title"></xsl:apply-templates>.
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="*" mode="how2cite-journal-title">
        <xsl:apply-templates select=".//journal-title"></xsl:apply-templates>
    </xsl:template>

    <xsl:template match="*" mode="how2cite-issue-info">
        <xsl:choose>
            <xsl:when test=".//pub-date[@pub-type='epub-ppub']">
                <xsl:apply-templates select=".//pub-date[@pub-type='epub-ppub']/year"/><xsl:if test=".//volume or .//issue">, </xsl:if>
            </xsl:when>
            <xsl:when test=".//pub-date[@pub-type='collection']">
                <xsl:apply-templates select=".//pub-date[@pub-type='collection']/year"/><xsl:if test=".//volume or .//issue">, </xsl:if>
            </xsl:when>
            <xsl:when test=".//pub-date[@pub-type='ppub']">
                <xsl:apply-templates select=".//pub-date[@pub-type='ppub']/year"/><xsl:if test=".//volume or .//issue">, </xsl:if>
            </xsl:when>
            <xsl:when test=".//pub-date[@pub-type='epub']">
                <xsl:apply-templates select=".//pub-date[@pub-type='epub']/year"/><xsl:if test=".//volume or .//issue">, </xsl:if>
            </xsl:when>
        </xsl:choose>
        <xsl:if test=".//volume">v. <xsl:value-of select=".//volume"/></xsl:if>
        <xsl:if test=".//issue"><xsl:if  test=".//volume">, </xsl:if>
            <xsl:choose>
                <xsl:when test="contains(.//issue,' ')">
                    <xsl:choose>
                        <xsl:when test="substring(.//issue,1,1)!='s'">
                            n. <xsl:value-of select=".//issue"/>
                        </xsl:when>
                        <xsl:otherwise><xsl:value-of select=".//issue"/></xsl:otherwise>
                    </xsl:choose>
                </xsl:when>
                <xsl:otherwise>
                    n. <xsl:value-of select=".//issue"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:if>
    </xsl:template>

    <xsl:template match="*" mode="how2cite-current-date">
        <xsl:if test="$howtocite_location!=''">
        [<xsl:apply-templates select="." mode="interface">
            <xsl:with-param name="text">cited</xsl:with-param>
        </xsl:apply-templates>&#160;CURRENTDATE]
        </xsl:if>
    </xsl:template>

    <xsl:template match="*" mode="how2cite-pages">
        <xsl:choose>
            <xsl:when test=".//elocation-id"><xsl:value-of select=".//elocation-id"/>. </xsl:when>
            <xsl:when test=".//fpage or .//lpage">pp. <xsl:value-of select=".//fpage"/><xsl:if test=".//lpage and .//fpage!=.//lpage">-<xsl:value-of select=".//lpage"/></xsl:if>. </xsl:when>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="*" mode="how2cite-available-from">
        <xsl:apply-templates select="." mode="interface">
            <xsl:with-param name="text">Available from</xsl:with-param>
        </xsl:apply-templates>:
        &amp;lt;<span id="how2cite_shorturl"><xsl:value-of select="normalize-space($howtocite_location)"/></span>&amp;gt;.
    </xsl:template>

    <xsl:template match="*" mode="how2cite-epub-date">
        <xsl:if test=".//pub-date[@pub-type='epub']">
            Epub <xsl:apply-templates select=".//pub-date[@pub-type='epub']"/>.
        </xsl:if>
    </xsl:template>

    <xsl:template match="*" mode="how2cite-issn">
        ISSN <xsl:value-of select=".//issn[@pub-type='epub']"/><xsl:if test="not(.//issn[@pub-type='epub'])"><xsl:value-of select=".//issn[1]"/></xsl:if>.
    </xsl:template>

    <xsl:template match="*" mode="how2cite-doi">
        <xsl:if test=".//article-id[@pub-id-type='doi']">
            <xsl:apply-templates select=".//article-id[@pub-id-type='doi']" mode="how2cite-doi"></xsl:apply-templates>.
        </xsl:if>
    </xsl:template>

    <xsl:template match="article-id[@pub-id-type='doi']" mode="how2cite-doi">
        https://doi.org/<xsl:value-of select="."/>
    </xsl:template>

</xsl:stylesheet>
