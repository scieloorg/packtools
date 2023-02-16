<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/html-modals-how2cite.xsl"/>

    <xsl:template match="*" mode="modal-how2cite">
        <div class="modal fade ModalDefault" id="ModalArticles" tabindex="-1" role="dialog"
            aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <xsl:apply-templates select="." mode="text-labels">
                                <xsl:with-param name="text">How to cite</xsl:with-param>
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
                        <p id="citation">
                        </p>
                        <input id="citationCut" type="text" value=""></input>
                        <a class="btn btn-secondary btn-sm scielo__btn-with-icon--left copyLink">
                            <xsl:attribute name="data-clipboard-target">#citationCut</xsl:attribute>
                            <span class="material-icons-outlined">link</span>
                            <xsl:apply-templates select="." mode="interface">
                                 <xsl:with-param name="text">copy</xsl:with-param>
                            </xsl:apply-templates>
                        </a>

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

</xsl:stylesheet>