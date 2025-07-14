<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/article-text-xref.xsl"/>

    <!--
        <p>O presente artigo tem como escopo principal investigar e analisar o retrato de concepções <span class="ref footnote"><sup class="xref"><a href="#fn1_ref" data-ref="Compreendemos por concepção como sendo a faculdade, o modo ou o ato de apreender, compreender, perceber, ver ou sentir algo, uma ideia, um fato, uma questão ou uma pessoa, o qual subsidia o processo de construção de uma perspectiva, um entendimento ou uma noção. A esse movimento pode estar atrelada sua sinonímia, ou seja, o julgamento, o qual é resultante de operações mentais do pensamento abstrato, baseadas na produção, ou utilização, de conceitos teóricos para uma representação, apreciação crítica, parecer ou opinião (favorável ou desfavorável). Mendes (1995) expõe que as concepções estariam relacionadas a um processo de construção em nível pessoal, social e cultural.">1</a></sup></span></span> sobre deficiências, expostas por universitários matriculados em Instituições da Educação Superior (IES), públicas e privadas, do estado de São Paulo. Isso porque, ao considerarmos os contextos educacionais, enquanto importantes espaços de formação do indivíduo, compreendemos que os elementos sócio-histórico-culturais, ainda que veladamente, podem potencializar ou minimizar atitudes discriminatórias frente a pessoas com deficiência ( <span class="ref"><strong class="xref xrefblue"><a href="#B32_ref" data-ref="LEITE, L. P.; LACERDA, C. The construction of a scale on the conceptions of disability: methodological procedures. Psicologia USP, v. 29, n. 3, p. 432-441, 2018. Disponível em: https://doi.org/10.1590/0103-65642018109">LEITE; LACERDA, 2018</a></strong></span></span> ).</p>
    -->

    <xsl:template match="xref[@ref-type='fn']">
        <xsl:variable name="id"><xsl:value-of select="@rid"/></xsl:variable>
        <xsl:variable name="text"><xsl:apply-templates select=".//text()"/></xsl:variable>
        <xsl:variable name="elem"><xsl:choose>
            <xsl:when test="contains('1234567890',substring(normalize-space($text),1,1))">sup</xsl:when>
            <xsl:otherwise>span</xsl:otherwise>
        </xsl:choose></xsl:variable>

        <!--
        <p>O presente artigo tem como escopo principal investigar e analisar o retrato de concepções <span class="ref footnote"><sup class="xref"><a href="#fn1_ref" data-ref="Compreendemos por concepção como sendo a faculdade, o modo ou o ato de apreender, compreender, perceber, ver ou sentir algo, uma ideia, um fato, uma questão ou uma pessoa, o qual subsidia o processo de construção de uma perspectiva, um entendimento ou uma noção. A esse movimento pode estar atrelada sua sinonímia, ou seja, o julgamento, o qual é resultante de operações mentais do pensamento abstrato, baseadas na produção, ou utilização, de conceitos teóricos para uma representação, apreciação crítica, parecer ou opinião (favorável ou desfavorável). Mendes (1995) expõe que as concepções estariam relacionadas a um processo de construção em nível pessoal, social e cultural.">1</a></sup></span></span> sobre deficiências, expostas por universitários matriculados em Instituições da Educação Superior (IES), públicas e privadas, do estado de São Paulo.     
        -->
        <span class="ref footnote">
            <sup class="xref">
                <a href="#{@rid}_ref" name="xref_{@rid}">
                    <xsl:attribute name="data-ref">
                        <xsl:apply-templates select="." mode="elem-texts-linked-to-xref">
                            <xsl:with-param name="id" select="$id"/>
                            <xsl:with-param name="text" select="$text"/>
                            <xsl:with-param name="elem" select="$elem"/>
                        </xsl:apply-templates>
                    </xsl:attribute>
                    <xsl:apply-templates select="*|text()" mode="ignore-sup"/>
                </a>
            </sup>
        </span>  
    </xsl:template>

    <xsl:template match="text()" mode="ignore-sup">
        <xsl:value-of select="."/>
    </xsl:template>
    <xsl:template match="*" mode="ignore-sup">
        <xsl:apply-templates select="."/>
    </xsl:template>
    <xsl:template match="sup" mode="ignore-sup">
        <xsl:apply-templates select="*|text()"/>
    </xsl:template>

    <xsl:template match="xref[@ref-type='equation' or @ref-type='disp-formula']">
        <!-- <a href="#{@rid}" class="goto"><span class="sci-ico-fileFormula"></span> <xsl:apply-templates select="*|text()"></xsl:apply-templates></a> -->
        <a href="" class="open-asset-modal" data-toggle="modal" data-target="#ModalScheme{translate(@rid,'.','_')}">
            <span class="sci-ico-fileFormula"></span> 
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </a>
    </xsl:template>
    
    <xsl:template match="xref[@ref-type='fig']">
        <a href="" class="open-asset-modal" data-toggle="modal" data-target="#ModalFig{translate(@rid,'.','_')}">
            <span class="sci-ico-fileFigure"></span> 
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </a>        
    </xsl:template>
    
    <xsl:template match="xref[@ref-type='table']">
        <a href="" class="open-asset-modal" data-toggle="modal" data-target="#ModalTable{translate(@rid,'.','_')}">
            <span class="sci-ico-fileTable"></span> 
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </a>        
    </xsl:template>
    <xsl:template match="xref[@ref-type='equation' or @ref-type='disp-formula']">
        <!-- <a href="#{@rid}" class="goto"><span class="sci-ico-fileFormula"></span> <xsl:apply-templates select="*|text()"></xsl:apply-templates></a> -->
        <a href="" class="open-asset-modal" data-bs-toggle="modal" data-bs-target="#ModalScheme{translate(@rid,'.','_')}">
            <span class="sci-ico-fileFormula"></span> 
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </a>
    </xsl:template>
    
    <xsl:template match="xref[@ref-type='fig']">
        <a href="" class="open-asset-modal" data-bs-toggle="modal" data-bs-target="#ModalFig{translate(@rid,'.','_')}">
            <span class="sci-ico-fileFigure"></span> 
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </a>        
    </xsl:template>
    
    <xsl:template match="xref[@ref-type='table']">
        <a href="" class="open-asset-modal" data-bs-toggle="modal" data-bs-target="#ModalTable{translate(@rid,'.','_')}">
            <span class="sci-ico-fileTable"></span> 
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </a>        
    </xsl:template>

    <xsl:template match="xref[@ref-type='bibr']">
        <xsl:variable name="id"><xsl:value-of select="@rid"/></xsl:variable>
        <xsl:variable name="text"><xsl:apply-templates select=".//text()"/></xsl:variable>
        <xsl:variable name="elem"><xsl:choose>
            <xsl:when test="sup">sup</xsl:when>
            <xsl:when test="$article//ref[@id=$id]/label">sup</xsl:when>
            <xsl:when test="starts-with($article//ref/mixed-citation)">1</xsl:when>
            <xsl:otherwise>span</xsl:otherwise>
        </xsl:choose></xsl:variable>
        <!--
        Isso porque, ao considerarmos os contextos educacionais, enquanto importantes espaços de formação do indivíduo, compreendemos que os elementos sócio-histórico-culturais, ainda que veladamente, podem potencializar ou minimizar atitudes discriminatórias frente a pessoas com deficiência ( <span class="ref"><strong class="xref xrefblue"><a href="#B32_ref" data-ref="LEITE, L. P.; LACERDA, C. The construction of a scale on the conceptions of disability: methodological procedures. Psicologia USP, v. 29, n. 3, p. 432-441, 2018. Disponível em: https://doi.org/10.1590/0103-65642018109">LEITE; LACERDA, 2018</a></strong></span></span> ).  
        -->

        <span class="ref">
            <xsl:element name="{$elem}">
                <xsl:attribute name="class">xref xrefblue</xsl:attribute>
                <a href="#{@rid}_ref">
                    <xsl:attribute name="data-ref">
                        <xsl:apply-templates select="." mode="elem-texts-linked-to-xref">
                            <xsl:with-param name="id" select="$id"/>
                            <xsl:with-param name="text" select="$text"/>
                            <xsl:with-param name="elem" select="$elem"/>
                        </xsl:apply-templates>
                    </xsl:attribute>
                    <xsl:apply-templates select="*|text()" mode="ignore-sup"/>
                </a>
            </xsl:element>
        </span>
    </xsl:template>

    <!--xsl:template match="*" mode="elem-texts-linked-to-xref">
        <xsl:apply-templates select="."/>
    </xsl:template-->

    <xsl:template match="xref" mode="elem-texts-linked-to-xref">
        <xsl:param name="id"/>
        <xsl:param name="text"/>
        <xsl:param name="elem"/>

        <xsl:apply-templates select="$article//*[@id=$id]" mode="elem-texts-linked-to-xref"/>
    </xsl:template>

    <xsl:template match="xref[@ref-type='bibr']" mode="elem-texts-linked-to-xref">
        <xsl:param name="id"/>
        <xsl:param name="text"/>
        <xsl:param name="elem"/>

        <xsl:choose>
            <xsl:when test="$elem='sup'">
                <xsl:variable name="following"><xsl:apply-templates select="." mode="exist-following-bibr-xref"></xsl:apply-templates></xsl:variable>
                <xsl:variable name="preceding"><xsl:apply-templates select="." mode="exist-preceding-bibr-xref"></xsl:apply-templates></xsl:variable>
                
                <xsl:choose>
                    <xsl:when test="substring-before($following,'XREF')='-'">
                        <xsl:apply-templates select="$article//ref" mode="repete">
                            <xsl:with-param name="from"><xsl:value-of select="@rid"/></xsl:with-param>
                            <xsl:with-param name="to"><xsl:value-of select="following-sibling::node()[name()='xref' and @ref-type='bibr'][1]/@rid"/></xsl:with-param>
                        </xsl:apply-templates>
                    </xsl:when>
                    <xsl:when test="substring($preceding, string-length($preceding) - string-length('[/xref]-')+1)='[/xref]-'">
                        <xsl:apply-templates select="$article//ref[@id=$id]" mode="elem-texts-linked-to-xref"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:apply-templates select="$article//ref[@id=$id]" mode="elem-texts-linked-to-xref"/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="$article//ref[@id=$id]" mode="elem-texts-linked-to-xref"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="label" mode="elem-texts-linked-to-xref">
        <xsl:apply-templates select="."/>&#160;
    </xsl:template>

    <xsl:template match="*[@id]" mode="elem-texts-linked-to-xref">
        <xsl:apply-templates select="*|text()" mode="elem-texts-linked-to-xref"/>
    </xsl:template>

    <xsl:template match="ref[@id]" mode="elem-texts-linked-to-xref">
        <xsl:apply-templates select="label | mixed-citation" mode="elem-texts-linked-to-xref"/>
    </xsl:template>

</xsl:stylesheet>