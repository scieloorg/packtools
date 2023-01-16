<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:template match="xref">
        <!--
        <span class="ref" id="refId_1">
            <strong class="xref xrefblue">Pellerin <i>et al</i>. 2019</strong>
            <sup><a title="Pellerin, R.J., Waminal, N.E. & Kim, H.H. 2019. FISH mapping of rDNA and telomeric repeats in 10 Senna species. Horticulture, Environment, and Biotechnology 60: 253-260." name="" class="" href="#1_ref">1</a></sup>
        </span>   
        <a title="O CMS Axe foi escrito por mim em 2013, e penso que quem o usa hoje em dia somos apenas eu e o André Noel. Provavelmente o código que eu disponibilizei na época exigirá algumas atualizações para rodar no ambiente atualizado dos provedores de hospedagem." name="ret-1_tipografia-cms-axe-e-o-tema-rocket" class="rodape_link" href="#1_tipografia-cms-axe-e-o-tema-rocket">1</a>     
        -->
        <strong><xsl:apply-templates select="*|text()"></xsl:apply-templates></strong>
        <span class="ref">
            <a>
                <xsl:attribute name="title">
                    <xsl:apply-templates select="." mode="elem-texts-linked-to-xref">
                        <xsl:with-param name="id" select="$id"/>
                        <xsl:with-param name="text" select="$text"/>
                        <xsl:with-param name="elem" select="$elem"/>
                    </xsl:apply-templates>
                </xsl:attribute>
                <xsl:attribute name="name">xref_<xsl:value-of select="@rid"/></xsl:attribute>
                <xsl:attribute name="class"></xsl:attribute>
                <xsl:attribute name="href">#fn_<xsl:value-of select="@rid"/></xsl:attribute>
                
                <xsl:element name="{$elem}">
                    <xsl:attribute name="class">xref big</xsl:attribute>
                    <xsl:apply-templates select="*|text()"></xsl:apply-templates>
                </xsl:element>
            </a>
        </span>   
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
            <xsl:when test="contains('1234567890',substring(normalize-space($text),1,1))">sup</xsl:when>
            <xsl:otherwise>strong</xsl:otherwise>
        </xsl:choose></xsl:variable>
        <!--
        <span class="ref" id="refId_1">
            <strong class="xref xrefblue">Pellerin <i>et al</i>. 2019</strong>
            <sup><a title="Pellerin, R.J., Waminal, N.E. & Kim, H.H. 2019. FISH mapping of rDNA and telomeric repeats in 10 Senna species. Horticulture, Environment, and Biotechnology 60: 253-260." name="" class="" href="#1_ref">1</a></sup>
        </span>   
        <a title="O CMS Axe foi escrito por mim em 2013, e penso que quem o usa hoje em dia somos apenas eu e o André Noel. Provavelmente o código que eu disponibilizei na época exigirá algumas atualizações para rodar no ambiente atualizado dos provedores de hospedagem." name="ret-1_tipografia-cms-axe-e-o-tema-rocket" class="rodape_link" href="#1_tipografia-cms-axe-e-o-tema-rocket">1</a>     
        -->
        <span class="ref">
            <xsl:attribute name="id">refId_<xsl:value-of select="@rid"/></xsl:attribute>
            <a>
                <xsl:attribute name="title">
                    <xsl:apply-templates select="." mode="elem-texts-linked-to-xref">
                        <xsl:with-param name="id" select="$id"/>
                        <xsl:with-param name="text" select="$text"/>
                        <xsl:with-param name="elem" select="$elem"/>
                    </xsl:apply-templates>
                </xsl:attribute>
                <xsl:attribute name="name">xref_<xsl:value-of select="@rid"/></xsl:attribute>
                <xsl:attribute name="class"></xsl:attribute>
                <xsl:attribute name="href">#ref_<xsl:value-of select="@rid"/></xsl:attribute>
                
                <xsl:element name="{$elem}">
                    <xsl:attribute name="class">xref xrefblue</xsl:attribute>
                    <xsl:apply-templates select="*|text()"></xsl:apply-templates>
                </xsl:element>
            </a>
        </span>        
    </xsl:template>

    <xsl:template match="xref" mode="elem-texts-linked-to-xref">
        <xsl:param name="id"/>
        <xsl:param name="text"/>
        <xsl:param name="elem"/>

        <xsl:apply-templates select="$article//*[@id=$id]" mode="xref"/>
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
                        <xsl:apply-templates select="$article//ref[@id=$id]" mode="xref"></xsl:apply-templates>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:apply-templates select="$article//ref[@id=$id]" mode="xref"></xsl:apply-templates>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="$article//ref[@id=$id]" mode="xref"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>