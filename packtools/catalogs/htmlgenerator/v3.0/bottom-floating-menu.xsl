<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:template match="/" mode="bottom-floating-menu">
        <div class="container">
            <div class="row">
              <div class="col">
                  <div class="scielo__floatingMenuCttJs3">
                    <xsl:apply-templates select="." mode="bottom-floating-menu-gototop"/>
                    <xsl:apply-templates select="." mode="bottom-floating-menu-metrics"/>
                    <ul class="scielo__floatingMenuJs3 fm-slidein" data-fm-toogle="hover">
                      <xsl:apply-templates select="." mode="bottom-floating-menu-open-and-close"/>
                    </ul>
                 </div>
              </div>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="/" mode="bottom-floating-menu-gototop">
      <a class="scielo__floatingMenuItem fm-button-child item-goto d-none d-lg-inline-block" data-bs-toggle="tooltip" href="#top">
        <xsl:attribute name="title"><xsl:apply-templates select="." mode="text-labels">
            <xsl:with-param name="text">Go to top</xsl:with-param>
        </xsl:apply-templates></xsl:attribute>
        <span class="material-icons-outlined">
          vertical_align_top
        </span>
      </a>
    </xsl:template>

    <xsl:template match="/" mode="bottom-floating-menu-metrics">
      <a href="javascript:;" class="scielo__floatingMenuItem fm-button-child item-metrics d-none d-lg-inline-block" data-bs-toggle="tooltip" target="_blank" data-bs-target="#metric_modal_id" tabindex="0">
        <xsl:attribute name="title"><xsl:apply-templates select="." mode="text-labels">
            <xsl:with-param name="text">Metrics</xsl:with-param>
        </xsl:apply-templates></xsl:attribute>
        <span class="material-icons-outlined">
          show_chart
        </span>
      </a>
    </xsl:template>

    <xsl:template match="/" mode="bottom-floating-menu-open-and-close">
      <li class="fm-wrap">
        <a href="javascript:;" class="fm-button-main" data-bs-toggle="tooltip" tabindex="0">
          <xsl:attribute name="title"><xsl:apply-templates select="." mode="text-labels">
              <xsl:with-param name="text">Open menu</xsl:with-param>
          </xsl:apply-templates></xsl:attribute>
          <span class="material-icons-outlined material-icons-outlined-menu-default">more_horiz</span></a>
        <a href="javascript:;" class="fm-button-close" data-bs-toggle="tooltip" tabindex="0">
          <xsl:attribute name="title"><xsl:apply-templates select="." mode="text-labels">
              <xsl:with-param name="text">Close menu</xsl:with-param>
          </xsl:apply-templates></xsl:attribute>
          <span class="material-icons-outlined material-icons-outlined-menu-close">close</span></a>

          <xsl:apply-templates select="." mode="bottom-floating-menu-for-not-mobile"/>
          <xsl:apply-templates select="." mode="bottom-floating-menu-for-mobile"/>
      </li>
    </xsl:template>

    <xsl:template match="/" mode="bottom-floating-menu-for-not-mobile">
      <!-- exibe em tudo menos mobile-->
      <ul class="fm-list-desktop d-none d-lg-block">
        <li>
          <a class="fm-button-child" id="lnkFigsTables" data-bs-toggle="tooltip" data-bs-target="#ModalTablesFigures" tabindex="0">
            <xsl:attribute name="title"><xsl:apply-templates select="." mode="text-labels">
              <xsl:with-param name="text"><xsl:value-of select="$graphic_elements_title"/></xsl:with-param>
          </xsl:apply-templates></xsl:attribute>
            <span class="material-icons-outlined">
              image
            </span>
          </a>
        </li>
        <!-- n/a -->
        <!--li>
          <a class="fm-button-child" id="lnkVersTranslations" data-bs-toggle="tooltip" data-bs-target="#ModalVersionsTranslations" tabindex="0">
            <xsl:attribute name="title"><xsl:apply-templates select="." mode="text-labels">
              <xsl:with-param name="text">Versões e traduções</xsl:with-param>
          </xsl:apply-templates></xsl:attribute>
            <span class="material-icons-outlined">
              translate
            </span>
          </a>
        </li-->
        <!--li>
          <a class="fm-button-child" id="lnkHowToCite" data-bs-toggle="tooltip"  data-bs-target="#ModalHowcite" tabindex="0">
            <xsl:attribute name="title"><xsl:apply-templates select="." mode="text-labels">
              <xsl:with-param name="text">Como citar este artigo</xsl:with-param>
          </xsl:apply-templates></xsl:attribute>
            <span class="material-icons-outlined">
              link
            </span>
          </a>
        </li-->
        <!--li>
          <a class="fm-button-child" id="lnkArticles" data-bs-toggle="tooltip" data-bs-target="#ModalRelatedArticles" tabindex="0">
            <xsl:attribute name="title"><xsl:apply-templates select="." mode="text-labels">
              <xsl:with-param name="text">Artigos relacionados</xsl:with-param>
          </xsl:apply-templates></xsl:attribute>
            <span class="material-icons-outlined">
              article
            </span>
          </a>
        </li-->
      </ul>
    </xsl:template>
    <xsl:template match="/" mode="bottom-floating-menu-for-mobile">
      <ul class="fm-list-desktop d-none d-lg-block">
        <li>
          <a class="fm-button-child" id="lnkFigsTables" data-bs-toggle="tooltip" title="{$graphic_elements_title}" data-bs-target="#ModalTablesFigures" tabindex="0">
            <span class="material-icons-outlined">
              image
            </span>
          </a>
        </li>
        <!-- n/a for standalone -->
        <!--li>
          <a class="fm-button-child" id="lnkVersTranslations" data-bs-toggle="tooltip" title="{% trans %}Versões e traduções{% endtrans %}" data-bs-target="#ModalVersionsTranslations" tabindex="0">
            <span class="material-icons-outlined">
              translate
            </span>
          </a>
        </li>
        <li>
          <a class="fm-button-child" id="lnkHowToCite" data-bs-toggle="tooltip" title="{% trans %}Como citar este artigo{% endtrans %}" data-bs-target="#ModalHowcite" tabindex="0">
            <span class="material-icons-outlined">
              link
            </span>
          </a>
        </li>
        <li>
          <a class="fm-button-child" id="lnkArticles" data-bs-toggle="tooltip" title="{% trans %}Artigos relacionados{% endtrans %}" data-bs-target="#ModalRelatedArticles" tabindex="0">
            <span class="material-icons-outlined">
              article
            </span>
          </a>
        </li-->
      </ul>
    </xsl:template>
</xsl:stylesheet>