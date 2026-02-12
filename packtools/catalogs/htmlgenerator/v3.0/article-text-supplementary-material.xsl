<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:template match="inline-supplementary-material">
        <!--
            No caso do conteúdo `inline-supplementary-material` e `supplementary-material` ser vazio,
            `<span class="INSERT_SUPPLEMENTARY_MATERIAL_TEXT"/>` identifica para o javascript,
            o local para incluir o texto do link do material suplementar, que é o nome do arquivo pdf,
            por exemplo: `0104-5970-hcsm-27-01-0275-suppl01.pdf`
            
            Este é o trecho de javascript a ser colocado na página do artigo no site
            (um trecho para cada material suplementar)

            ```javascript

            <script type="text/javascript">
                x = document.querySelector("a[href='https://minio.scielo.br/documentstore/1678-4758/TwZZBvMMN6XQNWb7C5Rc4qr/51c6856d1570190ab90aaa9b311a6ba1d762657a.pdf']").getElementsByClassName("REPLACE_BY_SUPPLEMENTARY_MATERIAL_TEXT");
                if (x) x[0].parentElement.innerHTML = "0104-5970-hcsm-27-01-0275-suppl01.pdf";
            </script>

            ```
        -->
        <a target="_blank">
            <xsl:apply-templates select="." mode="inline-supplementary-material-link"/>
            <xsl:apply-templates select="*|text()"/>

            <xsl:variable name="text"><xsl:apply-templates select="*|text()"/></xsl:variable>
            <xsl:if test="normalize-space($text)=''">
                <span class="REPLACE_BY_SUPPLEMENTARY_MATERIAL_TEXT">
                    <xsl:value-of select="@xlink:href"/>
                </span>
            </xsl:if>
        </a>
    </xsl:template>

    <xsl:template match="inline-supplementary-material[@xlink:href]" mode="inline-supplementary-material-link">
        <xsl:attribute name="href"><xsl:value-of select="@xlink:href"/></xsl:attribute>
    </xsl:template>

    <xsl:template match="inline-supplementary-material[media]" mode="inline-supplementary-material-link">
        <xsl:attribute name="href"><xsl:value-of select="media/@xlink:href"/></xsl:attribute>
    </xsl:template>

    <xsl:template match="inline-supplementary-material[graphic]" mode="inline-supplementary-material-link">
        <xsl:attribute name="href"><xsl:value-of select="graphic/@xlink:href"/></xsl:attribute>
    </xsl:template>

    <xsl:template match="inline-supplementary-material[@xlink:href]">
        <!--
            No caso do conteúdo `inline-supplementary-material` e `supplementary-material` ser vazio,
            `<span class="INSERT_SUPPLEMENTARY_MATERIAL_TEXT"/>` identifica para o javascript,
            o local para incluir o texto do link do material suplementar, que é o nome do arquivo pdf,
            por exemplo: `0104-5970-hcsm-27-01-0275-suppl01.pdf`
            
            Este é o trecho de javascript a ser colocado na página do artigo no site
            (um trecho para cada material suplementar)

            ```javascript

            <script type="text/javascript">
                x = document.querySelector("a[href='https://minio.scielo.br/documentstore/1678-4758/TwZZBvMMN6XQNWb7C5Rc4qr/51c6856d1570190ab90aaa9b311a6ba1d762657a.pdf']").getElementsByClassName("REPLACE_BY_SUPPLEMENTARY_MATERIAL_TEXT");
                if (x) x[0].parentElement.innerHTML = "0104-5970-hcsm-27-01-0275-suppl01.pdf";
            </script>

            ```
        -->
        <a target="_blank" href="{@xlink:href}">
            <xsl:apply-templates select="*|text()"/>

            <xsl:variable name="text"><xsl:apply-templates select="*|text()"/></xsl:variable>
            <xsl:if test="normalize-space($text)=''">
                <span class="REPLACE_BY_SUPPLEMENTARY_MATERIAL_TEXT">
                    <xsl:value-of select="@xlink:href"/>
                </span>
            </xsl:if>
        </a>
    </xsl:template>
    
    <xsl:template match="supplementary-material/media" mode="texts"><xsl:apply-templates select=".//text()"/></xsl:template>

    <!-- 
    <xsl:template match="supplementary-material">
        <div class="row fig" id="{@id}">
            <div class="col-md-1 col-sm-1">
                <a target="_blank">
                    <xsl:apply-templates select="." mode="supplementary-material-link"/>
                    <span class="material-icons-outlined">
                    download
                    </span>
                </a>
            </div>
            <div class="col-md-11 col-sm-11">
                <xsl:apply-templates select="." mode="supplementary-material-label-caption"/>
            </div>
        </div>
    </xsl:template>
    -->
    <xsl:template match="supplementary-material">
        <xsl:apply-templates select="." mode="supplementary-material-label-and-caption"/>
        <div class="row fig" id="{@id}">
            <a name="{@id}"></a>
            <div class="col-md-12 col-sm-12">
                <a target="_blank" download="1">
                    <xsl:apply-templates select="." mode="supplementary-material-link"/>
                    <xsl:apply-templates select="." mode="supplementary-material-lnktxt"/>
                </a>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="supplementary-material" mode="supplementary-material-label-and-caption">
        <xsl:if test="label">
            <h2 class="h5">
                <xsl:apply-templates select="label"/>
            </h2>
        </xsl:if>
    </xsl:template>

    <xsl:template match="supplementary-material" mode="supplementary-material-lnktxt">
        <xsl:variable name="text"><xsl:apply-templates select="." mode="supplementary-material-variable-text"/></xsl:variable>
        <xsl:apply-templates select="*|text()" mode="sm-link-text"/>
        <xsl:if test="normalize-space($text)=''">
            <xsl:apply-templates select="label" mode="sm-alt-link-text"/>
        </xsl:if>
    </xsl:template>

    <xsl:template match="*" mode="supplementary-material-variable-text">
        <xsl:apply-templates select="*|text()" mode="supplementary-material-variable-text"/>
    </xsl:template>
    <xsl:template match="text()" mode="supplementary-material-variable-text">
        <xsl:value-of select="."/>
    </xsl:template>
    <xsl:template match="supplementary-material/label" mode="supplementary-material-variable-text">
    </xsl:template>

    <xsl:template match="supplementary-material/*[text()]" mode="sm-link-text">
        <xsl:apply-templates select="."/>
    </xsl:template>
    <xsl:template match="supplementary-material/label" mode="sm-link-text">
    </xsl:template>
    <xsl:template match="supplementary-material/label" mode="sm-alt-link-text">
        <xsl:value-of select="."/>
    </xsl:template>

    <!--xsl:template match="supplementary-material//p" mode="supplementary-material-lnktxt">
        <p><xsl:apply-templates select="@*|*|text()"/></p>
    </xsl:template-->

    <xsl:template match="supplementary-material[@xlink:href]" mode="supplementary-material-link">
        <xsl:attribute name="href"><xsl:value-of select="@xlink:href"/></xsl:attribute>
    </xsl:template>

    <xsl:template match="supplementary-material[media]" mode="supplementary-material-link">
        <xsl:attribute name="href"><xsl:value-of select="media/@xlink:href"/></xsl:attribute>
    </xsl:template>

    <xsl:template match="supplementary-material[graphic]" mode="supplementary-material-link">
        <xsl:attribute name="href"><xsl:value-of select="graphic/@xlink:href"/></xsl:attribute>
    </xsl:template>
</xsl:stylesheet>