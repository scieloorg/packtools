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

    <xsl:template match="supplementary-material">
        <xsl:variable name="media_text"><xsl:apply-templates select="media" mode="texts"/></xsl:variable>
        <xsl:choose>
            <xsl:when test="normalize-space($media_text)=''">
                <a href="{media/@xlink:href}" download="1">
                    <xsl:value-of select="label"/>
                </a>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="*|text()"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>