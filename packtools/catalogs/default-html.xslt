<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:mml="http://www.w3.org/1998/Math/MathML"
  exclude-result-prefixes="xlink mml">

  <xsl:param name="article_lang" />
  <xsl:param name="is_translation" />
  <xsl:param name="issue_label" />
  <xsl:output method="html" indent="yes" encoding="UTF-8" omit-xml-declaration="yes" standalone="yes" />

  <!-- MAIN TEMPLTE -->
  <xsl:template match="/">
    <html lang="{ $article_lang }">
      <head>
        <meta charset="utf-8" />
        <title>
          <xsl:value-of select="article/front/journal-meta/journal-id"/> -
          <xsl:choose>
            <xsl:when test="$is_translation = 'True' ">
              <xsl:value-of select="article/front/article-meta/title-group/trans-title-group[@xml:lang=$article_lang]/trans-title" />
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="article/front/article-meta/title-group/article-title"/>
            </xsl:otherwise>
          </xsl:choose>
        </title>
      </head>
      <body>

        <a id="article-title"></a>
        <div class="title-top">
          <span class="bibliographic_legend">
            <xsl:value-of select="$bibliographic_legend" />
          </span>
          <span class="issn">
            ppub: <span class="ppub"><xsl:value-of select="article/front/journal-meta/issn[@pub-type='ppub']"/></span> -
            epub: <span class="epub"><xsl:value-of select="article/front/journal-meta/issn[@pub-type='epub']"/></span>
          </span>
          <!-- FPAGE and LPAGE -->
          <xsl:if test="article/front/article-meta/fpage != '00' and article/front/article-meta/lpage != '00' ">
            <span class="pages">
              <span class="fpage"><xsl:value-of select="article/front/article-meta/fpage"/></span> -
              <span class="lpage"><xsl:value-of select="article/front/article-meta/lpage"/></span>
            </span>
          </xsl:if>
          <!-- ELOCATION-ID -->
          <xsl:if test="article/front/article-meta/elocation-id">
            <span class="elocation_id"><xsl:value-of select="article/front/article-meta/elocation-id"/></span>
          </xsl:if>
          <!-- VOLUME and ISSUE or "ahead of print" -->
          <xsl:choose>
            <xsl:when test="article/front/article-meta/issue = '00' and article/front/article-meta/volume = '00' ">
              <span class="issue_label">ahead of print</span>
            </xsl:when>
            <xsl:otherwise>
              <span class="issue_label"><xsl:value-of select="$issue_label"/></span>
            </xsl:otherwise>
          </xsl:choose>
        </div>

        <h1 class="article-title">
          <xsl:choose>
            <xsl:when test="$is_translation = 'True' ">
              <xsl:apply-templates select="article/front/article-meta/title-group/trans-title-group[@xml:lang=$article_lang]/trans-title"/>
            </xsl:when>
            <xsl:otherwise>
              <xsl:apply-templates select="article/front/article-meta/title-group/article-title"/>
            </xsl:otherwise>
          </xsl:choose>
        </h1>

        <div class="title-bottom">
          <span class="doi">
            DOI:
            <xsl:apply-templates select="article/front/article-meta/article-id[@pub-id-type='doi']"/>
          </span>
        </div>

        <a id="article-categories"></a>
        <h2>Article categories:</h2>
        <div class="article-categories">
          <xsl:choose>
            <xsl:when test="$is_translation = 'True' ">
              <xsl:apply-templates select="article/sub-article[@article-type='translation' and @xml:lang=$article_lang]/front-stub/article-categories"/>
            </xsl:when>
            <xsl:otherwise>
              <xsl:apply-templates select="article/front/article-meta/article-categories"/>
            </xsl:otherwise>
          </xsl:choose>
        </div>

        <a id="contrib-group"></a>
        <h2>Contrib-group:</h2>
        <ul class="contrib-group">
          <xsl:apply-templates select="article/front/article-meta/contrib-group"/>
        </ul>

        <xsl:if test="article/front/article-meta/counts | article/sub-article[@article-type='translation' and @xml:lang=$article_lang]/front-stub/counts">
          <h2>Counts:</h2>
          <ul class="counts">
            <xsl:choose>
              <xsl:when test="$is_translation = 'True' and article/sub-article[@article-type='translation' and @xml:lang=$article_lang]/front-stub/counts">
                <xsl:apply-templates select="article/sub-article[@article-type='translation' and @xml:lang=$article_lang]/front-stub/counts"/>
              </xsl:when>
              <xsl:otherwise>
                <xsl:apply-templates select="article/front/article-meta/counts"/>
              </xsl:otherwise>
            </xsl:choose>
          </ul>
        </xsl:if>

        <a id="affiliations"></a>
        <h2>Affiliations:</h2>
        <ul class="affiliations">
          <xsl:apply-templates select="article/front/article-meta/aff"/>
        </ul>

        <a id="author-notes"></a>
        <h2>Author notes:</h2>
        <div class="author-notes">
          <xsl:choose>
            <xsl:when test="$is_translation = 'True' ">
              <xsl:apply-templates select="article/sub-article[@article-type='translation' and @xml:lang=$article_lang]/front-stub/author-notes"/>
            </xsl:when>
            <xsl:otherwise>
              <xsl:apply-templates select="article/front/article-meta/author-notes"/>
            </xsl:otherwise>
          </xsl:choose>
        </div>

        <a id="license"></a>
        <h2>License:</h2>
        <div class="permissions">
          <xsl:choose>
            <xsl:when test="$is_translation = 'True' ">
              <xsl:apply-templates select="article/sub-article[@article-type='translation' and @xml:lang=$article_lang]/front-stub/permissions"/>
            </xsl:when>
            <xsl:otherwise>
              <xsl:apply-templates select="article/front/article-meta/permissions"/>
            </xsl:otherwise>
          </xsl:choose>
        </div>

        <a id="products"></a>
        <h2>Products:</h2>
        <div class="products">
          <!-- <xsl:apply-templates select="article/front/article-meta//product"/> -->
          <xsl:choose>
            <xsl:when test="$is_translation = 'True' ">
              <xsl:apply-templates select="article/sub-article[@article-type='translation' and @xml:lang=$article_lang]/front-stub/article-meta/product"/>
            </xsl:when>
            <xsl:otherwise>
              <xsl:apply-templates select="article/front/article-meta/product"/>
            </xsl:otherwise>
          </xsl:choose>
        </div>

        <a id="abstract"></a>
        <h2>Abstract:</h2>
        <div class="abstract">
          <xsl:choose>
            <!-- if: is_translation AND sub-article/front-stub/abstract/ -->
            <xsl:when test="$is_translation = 'True' and article/sub-article[@article-type='translation' and @xml:lang=$article_lang]/front-stub/abstract[@xml:lang=$article_lang]">
              <xsl:apply-templates select="article/sub-article[@article-type='translation' and @xml:lang=$article_lang]/front-stub/abstract[@xml:lang=$article_lang]"/>
            </xsl:when>
            <!-- if: is_translation AND sub-article/front-stub/trans-abstract/ -->
            <xsl:when test="$is_translation = 'True' and article/sub-article[@article-type='translation' and @xml:lang=$article_lang]/front-stub/trans-abstract[@xml:lang=$article_lang]">
              <xsl:apply-templates select="article/sub-article[@article-type='translation' and @xml:lang=$article_lang]/front-stub/trans-abstract[@xml:lang=$article_lang]"/>
            </xsl:when>
            <!-- if: is_translation AND article/front/article-meta/trans-abstract/ -->
            <xsl:when test="$is_translation = 'True' and article/front/article-meta/trans-abstract[@xml:lang=$article_lang]">
              <xsl:apply-templates select="article/front/article-meta/trans-abstract[@xml:lang=$article_lang]"/>
            </xsl:when>
            <!-- if: article/front/article-meta/abstract/ -->
            <xsl:otherwise>
              <xsl:apply-templates select="article/front/article-meta/abstract[@xml:lang=$article_lang]"/>
            </xsl:otherwise>
          </xsl:choose>
        </div>

        <a id="keywords"></a>
        <h3>Keywords:</h3>
        <ul class="kwd-group">
          <xsl:choose>
            <xsl:when test="$is_translation = 'True' and article/sub-article[@article-type='translation' and @xml:lang=$article_lang]/front-stub/kwd-group[@xml:lang=$article_lang]">
              <xsl:apply-templates select="article/sub-article[@article-type='translation' and @xml:lang=$article_lang]/front-stub/kwd-group[@xml:lang=$article_lang]"/>
            </xsl:when>
            <xsl:otherwise>
              <xsl:apply-templates select="article/front/article-meta/kwd-group[@xml:lang=$article_lang]"/>
            </xsl:otherwise>
          </xsl:choose>
        </ul>

        <a id="dates"></a>
        <section class="pub_dates">
          <header>
            <h3>Pub Dates:</h3>
          </header>
          <xsl:choose>
            <xsl:when test="$is_translation = 'True' ">
              <xsl:apply-templates select="article/sub-article[@article-type='translation' and @xml:lang=$article_lang]/front-stub/pub-date"/>
            </xsl:when>
            <xsl:otherwise>
              <xsl:apply-templates select="article/front/article-meta/pub-date"/>
            </xsl:otherwise>
          </xsl:choose>
        </section>

        <xsl:if test="//article-meta/history | sub-article/front-stub/history">
          <a id="history"></a>
          <section class="history">
            <header>
              <h3>History:</h3>
            </header>
            <ul class="history">
              <xsl:choose>
                <xsl:when test="$is_translation = 'True' ">
                  <xsl:apply-templates select="article/sub-article[@article-type='translation' and @xml:lang=$article_lang]/front-stub/history"/>
                </xsl:when>
                <xsl:otherwise>
                  <xsl:apply-templates select="article/front/article-meta/history"/>
                </xsl:otherwise>
              </xsl:choose>
            </ul>
          </section>
        </xsl:if>

        <xsl:if test="article//funding-group">
          <a id="funding-group"></a>
          <section class="funding-group">
            <h3>Funding group:</h3>
            <ul class="funding-group-list">
              <xsl:choose>
                <xsl:when test="$is_translation = 'True' and article/sub-article[@article-type='translation' and @xml:lang=$article_lang]/front-stub/funding-group">
                  <xsl:apply-templates select="article/sub-article[@article-type='translation' and @xml:lang=$article_lang]/front-stub/funding-group"/>
                </xsl:when>
                <xsl:otherwise>
                  <xsl:apply-templates select="article/front/article-meta/funding-group"/>
                </xsl:otherwise>
              </xsl:choose>
            </ul>
          </section>
        </xsl:if>

        <a id="text"></a>
        <article class="body">
          <xsl:choose>
            <xsl:when test="$is_translation = 'True' ">
              <xsl:apply-templates
                select="article/sub-article[@article-type='translation' and @xml:lang=$article_lang]/body" mode="scift-standard-body" />
            </xsl:when>
            <xsl:otherwise>
              <xsl:apply-templates select="article/body"  mode="scift-standard-body" />
            </xsl:otherwise>
          </xsl:choose>
        </article>

        <xsl:if test="article/back/ack">
          <a id="acknowledgement"></a>
          <section class="article ack">
            <header>
              <h2>Acknowledgement:</h2>
            </header>
            <xsl:choose>
              <xsl:when test="$is_translation = 'True' ">
                <xsl:apply-templates select="article/sub-article[@article-type='translation' and @xml:lang=$article_lang]/back/ack"/>
              </xsl:when>
              <xsl:otherwise>
                <xsl:apply-templates select="article/back/ack"/>
              </xsl:otherwise>
            </xsl:choose>
          </section>
        </xsl:if>

        <xsl:if test="article//back/ref-list">
          <a id="references"></a>
          <section class="article references">
            <header>
              <h2>Referencias:</h2>
            </header>
            <xsl:choose>
              <xsl:when test="$is_translation = 'True' ">
                <xsl:apply-templates select="article/sub-article[@article-type='translation' and @xml:lang=$article_lang]/back/ref-list"/>
              </xsl:when>
              <xsl:otherwise>
                <xsl:apply-templates select="article/back/ref-list"/>
              </xsl:otherwise>
            </xsl:choose>
          </section>
        </xsl:if>

        <xsl:if test="article/body//fig">
          <a id="figures"></a>
          <section class="article figures">
            <header>
              <h2>Figures:</h2>
            </header>
            <xsl:choose>
              <xsl:when test="$is_translation = 'True' ">
                <xsl:apply-templates select="article/sub-article[@article-type='translation' and @xml:lang=$article_lang]//fig"/>
              </xsl:when>
              <xsl:otherwise>
                <xsl:apply-templates select="article/body//fig"/>
              </xsl:otherwise>
            </xsl:choose>
          </section>
        </xsl:if>

        <xsl:if test="article/body//table-wrap">
          <a id="tables"></a>
          <section class="tables-section">
            <header>
              <h2>Tables:</h2>
            </header>
            <xsl:choose>
              <xsl:when test="$is_translation = 'True' ">
                <xsl:apply-templates select="article/sub-article[@article-type='translation' and @xml:lang=$article_lang]//table-wrap"/>
              </xsl:when>
              <xsl:otherwise>
                <xsl:apply-templates select="article/body//table-wrap"/>
              </xsl:otherwise>
            </xsl:choose>
          </section>
        </xsl:if>

        <section class="article def-lists">
          <a id="def-lists"></a>
          <header>
            <h2>DEF LIST</h2>
          </header>
          <xsl:choose>
            <xsl:when test="$is_translation = 'True' ">
              <xsl:apply-templates select="article/sub-article[@article-type='translation' and @xml:lang=$article_lang]/back/def-list"/>
            </xsl:when>
            <xsl:otherwise>
              <xsl:apply-templates select="article/back/def-list"/>
            </xsl:otherwise>
          </xsl:choose>
        </section>

        <section class="article app-group">
          <a id="app-group"></a>
          <header>
            <h2>APP-GROUP:</h2>
          </header>
          <xsl:choose>
            <xsl:when test="$is_translation = 'True' ">
              <xsl:apply-templates select="article/sub-article[@article-type='translation' and @xml:lang=$article_lang]/back/app-group"/>
            </xsl:when>
            <xsl:otherwise>
              <xsl:apply-templates select="article/back/app-group"/>
            </xsl:otherwise>
          </xsl:choose>
        </section>

        <section class="article fn-group">
          <a id="fn-group"></a>
          <header>
            <h2>FN-GROUP:</h2>
          </header>
          <xsl:choose>
            <xsl:when test="$is_translation = 'True' ">
              <xsl:apply-templates select="article/sub-article[@article-type='translation' and @xml:lang=$article_lang]/back/fn-group"/>
            </xsl:when>
            <xsl:otherwise>
              <xsl:apply-templates select="article/back/fn-group"/>
            </xsl:otherwise>
          </xsl:choose>
        </section>

        <xsl:if test="//back/glossary">
          <section class="article glossary">
            <a id="glossary"></a>
            <header>
              <h3>GLOSSARY:</h3>
            </header>
            <xsl:choose>
              <xsl:when test="$is_translation = 'True' ">
                <xsl:apply-templates select="article/sub-article[@article-type='translation' and @xml:lang=$article_lang]/back/glossary"/>
              </xsl:when>
              <xsl:otherwise>
                <xsl:apply-templates select="article/back/glossary"/>
              </xsl:otherwise>
            </xsl:choose>

          </section>
        </xsl:if>

      </body>
    </html>
  </xsl:template>

  <!-- Tags Flutuantes -->
    <!-- As chamadas tags flutuantes podem aparecer em todo o documento, <front>, <body> e <back>. -->

    <!-- XREF -->
    <xsl:template match="xref | td/xref | th/xref">
      <xsl:if test="@ref-type='fn'">
        <a id="back_{@rid}" class="xref_id" />
      </xsl:if>
      <a href="#{@rid}" class="xref_href">
        <xsl:apply-templates/>
      </a>
    </xsl:template>
    <!-- /XREF -->

    <!-- LABEL -->
    <xsl:template match="label|caption" mode="scift-label-caption-graphic">
      <xsl:choose>
        <xsl:when test="name() = 'label' ">
          <label for="{../@id}">
            <xsl:apply-templates select="text() | *" mode="scift-label-caption-graphic"/>
          </label>
        </xsl:when>
        <xsl:otherwise>
          <xsl:element name="{name()}">
            <xsl:apply-templates select="text() | *" mode="scift-label-caption-graphic"/>
          </xsl:element>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:template>
    <!-- /LABEL -->
    <!-- TITLE -->
    <xsl:template match="title" mode="scift-label-caption-graphic">
      <xsl:apply-templates select="text() | *"/>
    </xsl:template>
    <!-- /TITLE -->

    <!-- P -->
    <xsl:template match="p">
      <p><xsl:apply-templates/></p>
    </xsl:template>
    <!-- /P -->
    <!-- SUP or SUB -->
    <xsl:template match="sup|sub">
      <xsl:element name="{name()}">
        <xsl:apply-templates/>
      </xsl:element>
    </xsl:template>
    <!-- /SUP or SUB -->
    <!-- ITALIC or BOLD -->
    <xsl:template match="italic">
      <em>
        <xsl:apply-templates/>
      </em>
    </xsl:template>
    <xsl:template match="bold">
      <strong>
        <xsl:apply-templates/>
      </strong>
    </xsl:template>
    <!-- /ITALIC or BOLD -->

  <!-- FRONT related tags -->
  <!-- Em <front> devem ser identificados os metadados do periódico, título, autoria, afiliação, resumo, ... -->

    <!-- <ABSTRACT>, <TRANS-ABSTRACT> -->
    <xsl:template match="abstract/title|trans-abstract/title">
      <header>
        <h4 class="abstract-title"><xsl:apply-templates/></h4>
      </header>
    </xsl:template>
    <xsl:template match="abstract/sec/title|trans-abstract/sec/title">
      <header>
        <h5 class="abstract-sec-title"><xsl:apply-templates/></h5>
      </header>
    </xsl:template>
    <xsl:template match="abstract//p|trans-abstract//p">
      <p class="abstract-p"><xsl:apply-templates/></p>
    </xsl:template>
    <xsl:template match="abstract/sec|trans-abstract/sec">
      <section class="abstract">
        <xsl:apply-templates/>
      </section>
    </xsl:template>

    <xsl:template match="front-stub/abstract | article-meta/abstract | front-stub/trans-abstract | article-meta/trans-abstract">
      <xsl:apply-templates/>
    </xsl:template>

    <!-- <ARTICLE-TITLE> and <TRANS-TITLE> -->
    <xsl:template match="article-title | trans-title">
      <span class="article-title">
        <xsl:apply-templates />
      </span>
    </xsl:template>

    <!-- <ARTICLE-META>/<ARTICLE-ID>/DOI -->
    <xsl:template match="article/front/article-meta/article-id[@pub-id-type='doi']">
      <xsl:variable name="doi" select="." />
      <a href='{$doi}'>
        <xsl:value-of select="."/>
      </a>
    </xsl:template>

    <!-- CONTRIB GROUP -->
    <xsl:template match="contrib-group">
      <xsl:for-each select="contrib | collab | on-behalf-of | role">
        <li class="contrib-type {@contrib-type}">
          <xsl:apply-templates select="."/>
        </li>
      </xsl:for-each>
    </xsl:template>

    <!-- CONTRIB -->
    <xsl:template match="contrib">
      <xsl:apply-templates/>
    </xsl:template>
    <!-- NAME -->
    <xsl:template match="name">
      <div class="name">
        <xsl:if test="prefix">
          <span class="prefix"><xsl:value-of select="prefix"/></span>
          &#160;
        </xsl:if>
        <xsl:if test="surname">
          <span class="surname"><xsl:value-of select="surname"/></span>
          ,&#160;
        </xsl:if>
        <xsl:if test="given-names">
          <span class="given_names"><xsl:value-of select="given-names"/></span>
          ,&#160;
        </xsl:if>
        <xsl:if test="suffix">
          <span class="suffix"><xsl:value-of select="suffix"/></span>
          ,&#160;
        </xsl:if>
      </div>
    </xsl:template>

    <!-- COLLAB -->
    <xsl:template match="collab">
      <div class="collab">
        <xsl:apply-templates/>
      </div>
    </xsl:template>

    <!-- ON-BEHALF-OF -->
    <xsl:template match="on-behalf-of">
      <div class="on_behalf_of">
        <xsl:apply-templates/>
      </div>
    </xsl:template>

    <!-- ROLE -->
    <xsl:template match="role">
      <span class="role">
        <xsl:apply-templates/>
      </span>
    </xsl:template>

    <!-- ARTICLE CATEGORIES -->
    <xsl:template match="article//article-categories">
      <ul class="article-categories">
        <xsl:for-each select="subj-group">
          <li class="article-categories {@subj-group-type}">
            <xsl:value-of select="subject"/>
          </li>
        </xsl:for-each>
      </ul>
    </xsl:template>

    <!-- AFF -->
    <xsl:template match="article/front/article-meta/aff">
      <li id="{@id}" class="aff">
          <div>
            <label for="{@id}"><xsl:value-of select="label"/></label>
            <xsl:if test="institution[@content-type='orgname']">
              &#8226; <span class="institution orgname"><xsl:value-of select="institution[@content-type='orgname']"/></span>
            </xsl:if>
            <xsl:if test="institution[@content-type='orgdiv1']">
              &#8226; <span class="institution orgdiv1"><xsl:value-of select="institution[@content-type='orgdiv1']"/></span>
            </xsl:if>
            <xsl:if test="institution[@content-type='orgdiv2']">
              &#8226; <span class="institution orgdiv2"><xsl:value-of select="institution[@content-type='orgdiv2']"/></span>
            </xsl:if>
            <xsl:if test="institution[@content-type='normalized']">
              &#8226; <span class="institution normalized"><xsl:value-of select="institution[@content-type='normalized']"/></span>
            </xsl:if>
            <xsl:if test="institution[@content-type='original']">
              &#8226; <span class="institution original"><xsl:value-of select="institution[@content-type='original']"/></span>
            </xsl:if>
            <xsl:if test="addr-line">
              <div class="addr-line">
                <xsl:if test="addr-line/named-content[@content-type='city']">
                  &#8226;
                  <span class="addr_line city">
                    <xsl:value-of select="addr-line/named-content[@content-type='city']"/>
                  </span>
                </xsl:if>
                <xsl:if test="addr-line/named-content[@content-type='state']">
                  &#8226;
                  <span class="addr_line state">
                    <xsl:value-of select="addr-line/named-content[@content-type='state']"/>
                  </span>
                </xsl:if>
              </div>
            </xsl:if>
            <xsl:if test="country">
              &#8226; <span class="country"><xsl:value-of select="country"/></span>
            </xsl:if>
          </div>
      </li>
    </xsl:template>

    <!-- AUTHOR NOTES -->
    <xsl:template match="email">
      <xsl:variable name="email_href" select="." />
      <a href='mailto:{$email_href}'>
        <xsl:value-of select="$email_href"/>
      </a>
    </xsl:template>

    <xsl:template match="corresp/label | fn/label">
      <label for="{../@id}">
        <xsl:value-of select="."/>
      </label>
    </xsl:template>

    <xsl:template match="author-notes/fn">
      <div class="author-notes-fn {@fn-type}">
        <xsl:apply-templates/>
      </div>
    </xsl:template>

    <xsl:template match="author-notes/corresp">
      <div class="corresp">
        <xsl:apply-templates/>
      </div>
    </xsl:template>

    <xsl:template match="author-notes">
      <xsl:for-each select="*">
        <xsl:apply-templates select="."/>
      </xsl:for-each>
    </xsl:template>

    <!-- PUB-DATE -->
    <xsl:template match="pub-date">
      <span class="pub_date">
        <span class="pub_date_type"><xsl:value-of select="@pub-type"/></span>:
        <xsl:if test="day">
          <span class="day"><xsl:apply-templates select="day"/></span>
        </xsl:if>
        <xsl:if test="month">
          <span class="month"><xsl:apply-templates select="month"/></span>
        </xsl:if>
        <xsl:if test="year">
          <span class="year"><xsl:apply-templates select="year"/></span>
        </xsl:if>
        <xsl:if test="season">
          <span class="season"><xsl:apply-templates select="season"/></span>
        </xsl:if>
      </span>
    </xsl:template>

    <!-- PERMISSIONS/LICENSE -->
    <xsl:template match="//permissions/license">
      <div class="license">
        <xsl:variable name="licence_href" select="@xlink:href" />
        <a href='{$licence_href}'>
          <xsl:value-of select="license-p"/>
        </a>
      </div>
    </xsl:template>
    <!-- PERMISSIONS/COPYRIGHT-STATEMENT -->
    <xsl:template match="//permissions/copyright-statement">
      <span class="copyright-statement">
        <xsl:apply-templates/>
      </span>
    </xsl:template>
    <!-- PERMISSIONS/COPYRIGHT-YEAR -->
    <xsl:template match="//permissions/copyright-year">
      <span class="copyright-year"><xsl:apply-templates/></span>
    </xsl:template>
    <!-- PERMISSIONS -->
    <xsl:template match="//permissions">
      <xsl:if test="license">
        <xsl:apply-templates select="license"/>
      </xsl:if>
      <xsl:if test="copyright-year | copyright-statement">
        <div class="copyright">
          <xsl:if test="copyright-year">
            <xsl:apply-templates select="copyright-year"/>
          </xsl:if>
          <xsl:if test="copyright-statement">
            <xsl:apply-templates select="copyright-statement"/>
          </xsl:if>
        </div>
      </xsl:if>
    </xsl:template>

    <!-- KWD GROUP -->
    <xsl:template match="kwd-group">
      <li class="kwd-group-item">
          <h4 class="kwd-group-title"><xsl:apply-templates select="title"/></h4>
          <ul class="kwds">
             <xsl:for-each select="kwd">
                <li class="kwd">
                  <xsl:apply-templates select="."/>
                </li>
              </xsl:for-each>
          </ul>
      </li>
    </xsl:template>

    <!-- PRODUCT -->
    <xsl:template match="product/etal">
      <span class="et-al">et al.</span>
    </xsl:template>

    <xsl:template match="product/inline-graphic | p/inline-graphic | th/inline-graphic | td/inline-graphic">
      <xsl:apply-templates select="." mode="scift-standard-body"/>
    </xsl:template>

    <xsl:template match="product/page-range">
      <span class="product_page_range"><xsl:value-of select="."/></span>
    </xsl:template>

    <xsl:template match="product/role|product/source|product/season|product/year|product/publisher-name|product/publisher-loc|product/size|product/isbn|product/edition">
      <div class="{name()}">
        <xsl:apply-templates/>
      </div>
    </xsl:template>

    <xsl:template match="product">
      <div class="product {@product-type}">
        <xsl:apply-templates/>
      </div>
    </xsl:template>

    <!-- HISTORY -->
    <xsl:template match="//article-meta/history | //front-stub/history">
      <xsl:for-each select="date">
        <li class="date {@date-type}">
          <div>
            <span class="type"><xsl:value-of select="@date-type"/></span>:
            <span class="day"><xsl:value-of select="day"/></span>/
            <span class="month"><xsl:value-of select="month"/></span>/
            <span class="year"><xsl:value-of select="year"/></span>
          </div>
        </li>
      </xsl:for-each>
    </xsl:template>

    <!-- FUNDING GROUP -->
    <xsl:template match="article//funding-group">
      <xsl:for-each select="award-group | funding-statement">
        <xsl:choose>
          <xsl:when test="name() ='funding-statement'">
            <li class="funding-statement">
              <xsl:apply-templates select="."/>
            </li>
          </xsl:when>
          <xsl:otherwise>
            <li class="award-group">
              <div class="award">
                <span class="funding-source">
                  <xsl:apply-templates select="funding-source"/>
                </span>
                <span class="award-id">
                  <xsl:apply-templates select="award-id"/>
                </span>
              </div>
            </li>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:for-each>
    </xsl:template>

    <xsl:template match="fig-count | table-count | equation-count | ref-count | page-count">
      <xsl:value-of select="@count"/>
    </xsl:template>
    <xsl:template match="article-meta/counts | front-stub/counts">
      <xsl:if test="fig-count">
        <li>Fig count: <span class="fig-count"><xsl:apply-templates select="fig-count"/></span></li>
      </xsl:if>
      <xsl:if test="table-count">
        <li>Table count: <span class="table-count"><xsl:apply-templates select="table-count"/></span></li>
      </xsl:if>
      <xsl:if test="equation-count">
        <li>Equation count: <span class="equation-count"><xsl:apply-templates select="equation-count"/></span></li>
      </xsl:if>
      <xsl:if test="ref-count">
        <li>Ref count: <span class="ref-count"><xsl:apply-templates select="ref-count"/></span></li>
      </xsl:if>
      <xsl:if test="page-count">
        <li>Page count: <span class="page-count"><xsl:apply-templates select="page-count"/></span></li>
      </xsl:if>
    </xsl:template>

  <!-- /FRONT related tags -->
  <!-- BODY related tags -->
  <!-- O body compreende o conteúdo e desenvolvimento do artigo. -->

    <!-- TEXT -->
    <xsl:template match="article//body//p" mode="scift-standard-body">
      <xsl:apply-templates select="."/>
    </xsl:template>

    <xsl:template match="disp-formula" mode="scift-standard-body">
      <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="article//body//sec" mode="scift-standard-body">
      <a id="{@sec-type}"></a>
      <section class="{translate(@sec-type, '|', ' ')}">
        <header>
          <h4><xsl:value-of select="title"/></h4>
        </header>
        <xsl:for-each select="sec | p | disp-formula | inline-graphic | supplementary-material | table-wrap">
          <xsl:choose>
            <xsl:when test="./fig">
            </xsl:when>
            <xsl:when test="name() = 'table-wrap'">
              <xsl:apply-templates select="."/>
            </xsl:when>

            <xsl:when test="./supplementary-material">
              <div class="supplementary-material">
                <xsl:apply-templates />
              </div>
            </xsl:when>
            <xsl:when test="name() = 'supplementary-material'">
              <div class="supplementary-material">
                <xsl:apply-templates />
              </div>
            </xsl:when>
            <xsl:otherwise>
              <xsl:apply-templates select="." mode="scift-standard-body"/>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:for-each>
      </section>
    </xsl:template>

    <!-- SEC/TITLE -->
    <xsl:template match="sec[@sec-type]/title">
      <p class="sec {@sec-type}">
        <xsl:apply-templates/>
      </p>
    </xsl:template>

    <!-- INLINE-FORMULA -->
    <xsl:template match="inline-formula">
      <span class="inline-formula">
        <xsl:apply-templates />
      </span>
    </xsl:template>

    <!-- DISP-FORMULA -->
    <xsl:template match="disp-formula/label">
      <label for="{../@id}">
        <xsl:apply-templates/>
      </label>
    </xsl:template>

    <xsl:template match="inline-graphic" mode="scift-standard-body">
      <span class="inline-graphic">
        <a target="_blank">
          <xsl:apply-templates select="." mode="scift-attribute-href"/>
          <img class="inline-graphic">
            <xsl:apply-templates select="." mode="scift-attribute-src"/>
          </img>
        </a>
      </span>
    </xsl:template>

    <xsl:template match="disp-formula/graphic">
      <a id="disp-formula_{../@id}"></a>
      <div class="disp-formula {../@id}">
        <a target="_blank">
          <xsl:apply-templates select="." mode="scift-attribute-href"/>
          <img class="inline-formula">
            <xsl:apply-templates select="." mode="scift-attribute-src"/>
          </img>
        </a>
      </div>
    </xsl:template>

    <!-- TABLE-WRAP -->
    <xsl:template match="table-wrap">
      <a id="{@id}"></a>
      <span class="label_caption">
        <xsl:apply-templates select="label | caption" mode="scift-label-caption-graphic"/>
      </span>
      <xsl:apply-templates select="graphic | table"/>
      <xsl:apply-templates select="table-wrap-foot"/>
      <xsl:apply-templates mode="footnote" select=".//fn"/>
    </xsl:template>

    <xsl:template match="table-wrap" mode="scift-standard">
      <span class="label_caption">
        <xsl:apply-templates select="label | caption" mode="scift-label-caption-graphic"/>
      </span>
      <xsl:apply-templates select="graphic | table"/>
      <xsl:apply-templates mode="footnote" select=".//fn"/>
    </xsl:template>

    <xsl:template match="table-wrap[not(.//graphic)]" mode="scift-thumbnail">
      <xsl:apply-templates select="." mode="scift-standard"/>
    </xsl:template>

    <!-- TABLE -->
    <xsl:template match="table/@rules">
      <xsl:attribute name="style">
        <xsl:text>border-color:black; border-style: solid;</xsl:text>
      </xsl:attribute>
    </xsl:template>

    <xsl:template match="table/@frame"></xsl:template>

    <xsl:template match="colgroup/@width">
      <xsl:attribute name="style">
          <xsl:text>width:</xsl:text><xsl:value-of select="." />
      </xsl:attribute>
    </xsl:template>

    <xsl:template match="th/@align|td/@align">
      <xsl:attribute name="style">
          <xsl:text>text-align:</xsl:text><xsl:value-of select="." />
      </xsl:attribute>
    </xsl:template>

    <xsl:template match="table">
      <table class="table">
        <xsl:apply-templates/>
      </table>
    </xsl:template>

    <xsl:template match="table//disp-formula">
      <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="table//*">
      <xsl:element name="{name()}">
        <xsl:apply-templates/>
      </xsl:element>
    </xsl:template>

    <xsl:template match="table//@*">
      <xsl:attribute name="{name()}">
        <xsl:value-of select="."/>
      </xsl:attribute>
    </xsl:template>

    <xsl:template match="table-wrap//fn" mode="footnote">
      <a id="{@id}"/>
      <xsl:apply-templates select="* | text()"/>
    </xsl:template>

    <xsl:template match="table-wrap//fn//label">
      <sup>
        <xsl:value-of select="."/>
      </sup>
    </xsl:template>

    <xsl:template match="table-wrap//fn/p">
      <p class="fn">
        <xsl:apply-templates select="*|text()"/>
      </p>
    </xsl:template>

    <!-- FIG -->
    <xsl:template match="fig">
      <xsl:apply-templates select="." mode="scift-standard"/>
    </xsl:template>

    <xsl:template match="fig" mode="scift-standard">
      <figure id="{@id}" class="figure">
        <xsl:apply-templates select="graphic|media"/>
        <figcaption class="label_caption">
          <xsl:apply-templates select="label | caption" mode="scift-label-caption-graphic"/>
        </figcaption>
      </figure>
    </xsl:template>

    <!-- FIG/CAPTION or TABLE-WRAP/CAPTION -->
    <xsl:template match="fig/caption | table-wrap/caption">
      <span class="{name()}">
        <xsl:apply-templates select="* | text()"/>
      </span>
    </xsl:template>

    <!-- FIG/LABEL or TABLE-WRAP/LABEL -->
    <xsl:template match="fig/label | table-wrap/label">
      <label for="{../@id}">
        <xsl:apply-templates select=". | text()"/>
      </label>
    </xsl:template>

    <xsl:template match="table-wrap//table-wrap-foot">
      <div class="{name()}">
        <xsl:apply-templates select="* | text()"/>
      </div>
    </xsl:template>

    <xsl:template match="fig | table-wrap[.//graphic]" mode="scift-thumbnail">
      <div class="{local-name()} panel">
        <table class="table_thumbnail">
          <tr>
            <td class="td_thumbnail">
              <xsl:apply-templates select=".//graphic" mode="scift-thumbnail"/>
            </td>
            <td class="td_label_caption">
              <span class="label_caption">
                <xsl:apply-templates select="label | caption" mode="scift-label-caption-graphic"/>
              </span>
              <xsl:apply-templates mode="footnote" select=".//fn"/>
            </td>
          </tr>
        </table>
      </div>
    </xsl:template>

    <!-- SUPPLEMENTARY-MATERIAL -->
    <xsl:template match="supplementary-material/caption">
      <caption class="supplementary-material-caption-for-{../@id}">
        <xsl:apply-templates />
      </caption>
    </xsl:template>

    <xsl:template match="supplementary-material/label">
      <label for="{../@id}">
        <xsl:apply-templates />
      </label>
    </xsl:template>

    <xsl:template match="supplementary-material">
      <xsl:choose>
        <xsl:when test="not(*) and normalize-space(text())=''">
          <xsl:variable name="src">/????/<xsl:value-of select="@xlink:href"/></xsl:variable>
          <a target="_blank">
            <xsl:attribute name="href"><xsl:value-of select="$src"/></xsl:attribute>
            <xsl:value-of select="@xlink:href"/>
          </a>
        </xsl:when>
        <xsl:when test="table-wrap">
          <xsl:apply-templates select="table-wrap"/>
        </xsl:when>
        <xsl:otherwise>
          <div class="panel">
            <xsl:apply-templates select="." mode="label"/>
          </div>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:template>

    <!-- INLINE-SUPPLEMENTARY-MATERIAL -->
    <xsl:template match="inline-supplementary-material">
      <xsl:variable name="src">/pdf<xsl:value-of
            select="substring-after($var_IMAGE_PATH,'/img/revistas')"/><xsl:value-of
              select="@xlink:href"/></xsl:variable>
      <a target="_blank">
        <xsl:attribute name="href">
          <xsl:value-of select="$src"/>
        </xsl:attribute>
        <xsl:choose>
          <xsl:when test="normalize-space(text())=''">
            <xsl:value-of
              select="@xlink:href"/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="."/>
          </xsl:otherwise>
        </xsl:choose>
      </a>
    </xsl:template>

    <!-- DISP-QUOTE -->
    <xsl:template match="disp-quote">
      <blockquote class="disp-quote">
        <xsl:apply-templates select="*|text()"/>
      </blockquote>
    </xsl:template>

    <!-- EXT-LINK|URI -->
    <xsl:template match="ext-link|uri">
      <a href="{@xlink:href}" target="_blank">
        <xsl:value-of select="."/>
      </a>
    </xsl:template>

    <!-- LIST -->
    <xsl:template match="list-item" mode="scift-standard-list-item">
      <div class="list-item-content">
        <xsl:if test="label">
          <label for="{@id}">
            <xsl:apply-templates select="./label"/>
          </label>
        </xsl:if>
        <xsl:apply-templates select="*[not(name()='label')]"/>
        <xsl:apply-templates select="list"/>
      </div>
    </xsl:template>

    <xsl:template match="list">
      <xsl:if test="title">
        <span class="list-title"><xsl:value-of select="title"/></span>
      </xsl:if>
      <xsl:if test="label">
        <label for="{@id}">
          <xsl:apply-templates select="label"/>
        </label>
      </xsl:if>
      <xsl:variable name="type" select="@list-type" />
      <ul class="{$type}">
        <xsl:for-each select="list-item">
          <xsl:choose>
            <xsl:when test="$type = 'order'">
              <li class="list-item">
                <xsl:number level="multiple"/>.
                <xsl:apply-templates select="." mode="scift-standard-list-item"/>
              </li>
            </xsl:when>
            <xsl:when test="$type = 'bullet'">
              <li>
                &#8226; <xsl:apply-templates select="." mode="scift-standard-list-item"/>
              </li>
            </xsl:when>
            <xsl:when test="$type = 'alpha-lower'">
              <li>
                <xsl:number level="multiple" format="a. "/> <xsl:apply-templates select="." mode="scift-standard-list-item"/>
              </li>
            </xsl:when>
            <xsl:when test="$type = 'roman-lower'">
              <li>
                <xsl:number level="multiple" format="i. "/> <xsl:apply-templates select="." mode="scift-standard-list-item"/>
              </li>
            </xsl:when>
            <xsl:when test="$type = 'roman-upper'">
              <li>
                <xsl:number level="multiple" format="I. "/> <xsl:apply-templates select="." mode="scift-standard-list-item"/>
              </li>
            </xsl:when>
            <xsl:when test="$type = 'simple'">
              <li>
                <xsl:apply-templates select="." mode="scift-standard-list-item"/>
              </li>
            </xsl:when>
          </xsl:choose>
        </xsl:for-each>
      </ul>
    </xsl:template>

    <!-- MEDIA -->
    <xsl:template match="media">
      <xsl:variable name="src">//cdn.scielo.org/media_path/<xsl:value-of select="@xlink:href"/></xsl:variable>

      <a target="_blank">
        <xsl:attribute name="href">
          <xsl:value-of select="$src"/>
        </xsl:attribute>
        <xsl:if test="label">
          <span class="media-label"><xsl:value-of select="label"/></span>
        </xsl:if>
      </a>

      <embed width="100%" height="400">
        <xsl:attribute name="src">
          <xsl:value-of select="$src"/>
        </xsl:attribute>
      </embed>
    </xsl:template>

    <xsl:template match="media[@mime-subtype='pdf']">
      <!-- <xsl:variable name="src">/pdf<xsl:value-of select="substring-after($var_IMAGE_PATH,'/img/revistas')"/><xsl:value-of select="@xlink:href"/></xsl:variable> -->
      <xsl:variable name="src">//cdn.scielo.org/pdf_path/<xsl:value-of select="@xlink:href"/></xsl:variable>
      <a target="_blank">
        <xsl:attribute name="href">
          <xsl:value-of select="$src"/>
        </xsl:attribute>
        <xsl:if test="normalize-space(text())=''">
          <xsl:value-of select="@xlink:href"/>
        </xsl:if>
      </a>
    </xsl:template>

    <!-- SIG-BLOCK -->
    <xsl:template match="sig-block/sig" mode="scift-standard-body">
      <div class="sig-block">
        <xsl:apply-templates select="*"/>
      </div>
    </xsl:template>

  <!-- /BODY related tags -->
  <!-- BACK related tags -->
  <!-- O <back> é a parte final do documento que compreende lista de referências e demais dados referentes a pesquisa. -->

    <!-- ACK -->
    <xsl:template match="//back/ack">
      <h3><xsl:value-of select="title"/></h3>
      <ul>
        <xsl:for-each select="p">
          <li><xsl:apply-templates select="."/></li>
        </xsl:for-each>
      </ul>
    </xsl:template>

    <!-- REF-LIST & REF -->
    <xsl:template match="//back/ref-list">
      <div class="ref-list">
        <a id="ref-list"/>
        <section class="ref">
          <h4><xsl:apply-templates select="title"/></h4>
          <xsl:if test="not(title)">
            <xsl:choose>
              <xsl:when test="$article_lang='pt'"><h4>REFERÊNCIAS</h4></xsl:when>
              <xsl:when test="$article_lang='es'"><h4>REFERENCIAS</h4></xsl:when>
              <xsl:otherwise><h4>REFERENCES</h4></xsl:otherwise>
            </xsl:choose>
          </xsl:if>
          <xsl:apply-templates select="ref"/>
        </section>
      </div>
    </xsl:template>

    <xsl:template match="ref">
      <p class="ref">
        <a id="{@id}"/>
        <xsl:choose>
          <xsl:when test="label and mixed-citation">
            <xsl:if test="substring(mixed-citation,1,string-length(label))!=label">
              <label for="{@id}"><xsl:value-of select="label"/></label>
            </xsl:if>
          </xsl:when>
          <xsl:when test="label">
            <label for="{@id}">
              <label for="{@id}"><xsl:value-of select="label"/></label>
            </label>
          </xsl:when>
        </xsl:choose>
        <xsl:choose>
          <xsl:when test="element-citation[.//ext-link] and mixed-citation[not(.//ext-link)] or element-citation[.//uri] and mixed-citation[not(.//uri)] ">
            <xsl:apply-templates select="mixed-citation" mode="with-link">
              <xsl:with-param name="ext_link" select=".//ext-link"/>
              <xsl:with-param name="uri" select=".//uri"/>
            </xsl:apply-templates>
          </xsl:when>
          <xsl:when test="element-citation">
            <xsl:apply-templates select="element-citation"/>
          </xsl:when>
          <xsl:when test="mixed-citation">
            <xsl:apply-templates select="mixed-citation"/>
          </xsl:when>
          <xsl:when test="citation">
            <xsl:apply-templates select="citation"/>
          </xsl:when>
          <xsl:otherwise><xsl:comment>_missing mixed-citation _</xsl:comment>
          </xsl:otherwise>
        </xsl:choose>
        <xsl:variable name="aref">
          000000<xsl:apply-templates select="." mode="scift-get_position"/>
        </xsl:variable>
        <xsl:variable name="ref">
          <xsl:value-of select="substring($aref, string-length($aref) - 5)"/>
        </xsl:variable>
        <xsl:variable name="pid">
          <!-- <xsl:value-of select="$pid"/>&#160;<xsl:value-of select="substring($ref,2)"/> -->
          <xsl:value-of select="pid"/>
          <xsl:value-of select="substring($ref,2)"/>
        </xsl:variable>
        [&#160;<a href="#pid:{$pid}" >Links</a>&#160;]
      </p>
    </xsl:template>

    <!-- FN-GROUP -->
    <xsl:template match="article/back/fn-group/fn/p">
      <p class="fn">
        <xsl:apply-templates select="*|text()"/>
      </p>
    </xsl:template>

    <xsl:template match="back//fn-group">
      <div class="foot-notes">
        <xsl:for-each select="fn">
          <div class="fn-block fn-id-{@id} fn-type-{@fn-type}">
            <div class="fn-block-label">
              <xsl:if test="label">
                <a id="{@id}"></a>
                <a href="#back_{@id}" class="fn-label">
                  <xsl:apply-templates select="label"/>
                </a>
              </xsl:if>
            </div>
            <div class="fn-content">
              <xsl:apply-templates select="*[not(name()='label')]"/>
            </div>
          </div>
        </xsl:for-each>
      </div>
    </xsl:template>

    <!-- APP-GROUP/APP -->
    <xsl:template match="app">
      <div class="app">
        <div class="app-label">
          <label for="{@id}"><xsl:apply-templates select="label"/></label>
        </div>
        <div class="app-content">
          <xsl:apply-templates select="*[not(name()='label')]"/>
        </div>
      </div>
    </xsl:template>

    <xsl:template match="back/app-group">
      <div class="app-group">
        <xsl:for-each select="*">
          <xsl:choose>
              <xsl:when test="./app">
                <xsl:apply-templates select="./app"/>
              </xsl:when>
              <xsl:otherwise>
                <xsl:apply-templates select="."/>
              </xsl:otherwise>
          </xsl:choose>
        </xsl:for-each>
      </div>
    </xsl:template>

    <!-- DEF-LIST -->
    <xsl:template match="back/def-list" name="def-list">
      <div class="def-list">
        <xsl:if test="label">
          <label for="{@id}"><xsl:apply-templates select="label"/></label>
        </xsl:if>
        <dl>
          <xsl:for-each select="def-item | def-list">
            <dt class="def-list-term">
              <xsl:apply-templates select="term"/>
            </dt>
            <dd class="def-list-item">
              <xsl:choose>
                <xsl:when test="name() ='def-item'">
                  <xsl:apply-templates select="def/*"/>
                </xsl:when>
                <xsl:otherwise>
                  <xsl:apply-templates select="."/>
                </xsl:otherwise>
              </xsl:choose>
            </dd>
          </xsl:for-each>
        </dl>
      </div>
    </xsl:template>

    <!-- GLOSSARY -->
    <xsl:template match="back/glossary">
      <div id="glossary-{@id}" class="glossary">
        <xsl:if test="label">
          <label for="{@id}"><xsl:apply-templates select="label"/></label>
        </xsl:if>
        <xsl:if test="title">
          <span class="glossary-title-for-{@id}"><xsl:apply-templates select="title"/></span>
        </xsl:if>
        <xsl:for-each select="def-list">
          <xsl:call-template name="def-list"/>
        </xsl:for-each>
        <xsl:for-each select="table-wrap">
          <xsl:apply-templates select="."/>
        </xsl:for-each>
      </div>
    </xsl:template>

  <!-- /BACK related tags -->
  <!-- OTHERS tags -->

  <xsl:template match="elocation-id">
    <span class="elocation-id">
      <xsl:value-of select="text()" />
    </span>
  </xsl:template>

  <!-- PERSON-GROUP -->
  <xsl:template match="person-group">
    <span class="person-group {@person-group-type}">
      <xsl:for-each select="name">
        <div class="person">
          <xsl:apply-templates select="."/>
          <xsl:if test="../collab">
           - <xsl:value-of select="../collab"/>
          </xsl:if>
        </div>
      </xsl:for-each>
      <xsl:if test="role">
        <xsl:apply-templates select="role"/>
      </xsl:if>
      <xsl:if test="etal">
        <span class="et-al">et al.</span>
      </xsl:if>
    </span>
    &#160;
  </xsl:template>

  <!-- GRAPHIC -->
  <xsl:template match="graphic">
    <a target="_blank">
      <xsl:apply-templates select="." mode="scift-attribute-href"/>
      <img class="graphic"><xsl:apply-templates select="." mode="scift-attribute-src"/></img>
    </a>
  </xsl:template>
  <!-- HREF -->
  <xsl:template match="*" mode="scift-fix-href">//cdn.scielo.org/image_path/<xsl:value-of select="@xlink:href"/></xsl:template>
  <xsl:template match="*" mode="scift-attribute-href">
    <xsl:attribute name="href">
      <xsl:apply-templates select="." mode="scift-fix-href"/>
    </xsl:attribute>
  </xsl:template>
  <!-- SRC -->
  <xsl:template match="*" mode="scift-attribute-src">
    <xsl:attribute name="src"><xsl:apply-templates select="." mode="scift-fix-href"/></xsl:attribute>
    <xsl:attribute name="alt"></xsl:attribute>
  </xsl:template>

  <xsl:template match="element-citation/season">
    <span class="season"><xsl:apply-templates/></span>
  </xsl:template>
  <xsl:template match="element-citation/size">
    <span class="size"><xsl:apply-templates/></span>
  </xsl:template>
  <xsl:template match="element-citation">
    <span class="{name()} {@publication-type}">
      <xsl:apply-templates select="*[not(issue|volume|fpage|lpage|elocation-id)]"/>
      <!-- ISSUE and VOLUME -->
      <xsl:if test="issue and volume">
        <xsl:choose>
          <xsl:when test="issue = '00' and volume = '00' ">
            <span class="element_issue_volume">ahead of print</span>
          </xsl:when>
          <xsl:otherwise>
            <span class="element_issue_volume">
              vol.<xsl:value-of select="volume"/> n.<xsl:value-of select="issue"/>
            </span>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:if>
      <!-- FPAGE and LPAGE -->
      <xsl:if test="fpage and fpage != '00' and lpage and lpage != '00' ">
        <span class="element_pages">
          <span class="element_fpage"><xsl:value-of select="fpage"/></span> -
          <span class="element_lpage"><xsl:value-of select="lpage"/></span>
        </span>
      </xsl:if>
      <!-- PAGE-RANGE -->
      <xsl:if test="page-range">
        <span class="element_page_range"><xsl:value-of select="page-range"/></span>
      </xsl:if>
      <!-- ISBN -->
      <xsl:if test="isbn">
        <span class="element_isbn"><xsl:value-of select="isbn"/></span>
      </xsl:if>
      <!-- SOURCE -->
      <xsl:if test="source">
        <span class="element_source"><xsl:value-of select="source"/></span>
      </xsl:if>
      <!-- EDITION -->
      <xsl:if test="edition">
        <span class="element_edition"><xsl:value-of select="edition"/></span>
      </xsl:if>
      <!-- PUBLISHER-NAME -->
      <xsl:if test="publisher-name">
        <span class="element_publisher_name"><xsl:value-of select="publisher-name"/></span>
      </xsl:if>
      <!-- PUBLISHER-LOC -->
      <xsl:if test="publisher-loc">
        <span class="element_publisher_loc"><xsl:value-of select="publisher-loc"/></span>
      </xsl:if>
    </span>
  </xsl:template>
  <xsl:template match="mixed-citation | nlm-citation | citation ">
    <span class="{name()} {@publication-type}"><xsl:apply-templates/></span>
  </xsl:template>

  <xsl:template match="mixed-citation" mode="with-link">
    <xsl:param name="uri"/>
    <xsl:param name="ext_link"/>
    <xsl:choose>
      <xsl:when test="$uri">
        <xsl:choose>
          <xsl:when test="contains(.,$uri/text())">
            <xsl:value-of select="substring-before(.,$uri/text())"/>
            <xsl:apply-templates select="$uri"/>
            <xsl:value-of select="substring-after(.,$uri/text())"/>
          </xsl:when>
          <xsl:when test="contains(.,$uri/@xlink:href)">
            <xsl:value-of select="substring-before(.,$uri/@xlink:href)"/>
            <xsl:apply-templates select="$uri"/>
            <xsl:value-of select="substring-after(.,$uri/@xlink:href)"/>
          </xsl:when>
        </xsl:choose>
      </xsl:when>
      <xsl:when test="$ext_link">
        <xsl:choose>
          <xsl:when test="contains(.,$ext_link/text())">
            <xsl:value-of select="substring-before(.,$ext_link/text())"/>
            <xsl:apply-templates select="$ext_link"/>
            <xsl:value-of select="substring-after(.,$ext_link/text())"/>
          </xsl:when>
          <xsl:when test="contains(.,$ext_link/@xlink:href)">
            <xsl:value-of select="substring-before(.,$ext_link/@xlink:href)"/>
            <xsl:apply-templates select="$ext_link"/>
            <xsl:value-of select="substring-after(.,$ext_link/@xlink:href)"/>
          </xsl:when>
        </xsl:choose>
      </xsl:when>
    </xsl:choose>
  </xsl:template>

  <!-- /OTHERS tags -->
</xsl:stylesheet>
