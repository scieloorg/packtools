<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    
    <xsl:include href="../v2.0/article-text-fn.xsl"/>

    <xsl:template match="fn[@fn-type='edited-by'] | fn[@fn-type='data-availability']" mode="open-science-notes">
        <xsl:variable name="title"><xsl:apply-templates select="label"/><xsl:if test="not(label)"><xsl:apply-templates select="." mode="text-labels">
                 <xsl:with-param name="text"><xsl:value-of select="@fn-type"/></xsl:with-param>
             </xsl:apply-templates></xsl:if></xsl:variable>
        <div>
            <xsl:attribute name="class">articleSection</xsl:attribute>
            <xsl:attribute name="data-anchor"><xsl:value-of select="translate($title, ':', '')"/></xsl:attribute>
            <h3><xsl:value-of select="translate($title, ':', '')"/></h3>
            <xsl:apply-templates select="." mode="a_name"/>
            <xsl:apply-templates select="*[name()!='label']|text()"/>
        </div>
    </xsl:template>

    <xsl:template match="fn[@id] | author-notes/*[@id]">
        <!-- 
        <li>
            <a name="fn12_ref"></a><span class="xref big">12</span>
            <div>Frases como “Estou olhando para esse sujeito com deficiência, sei que ele existe, mas Deus/deus quis assim e eu não posso fazer nada”, infelizmente, ainda são muito recorrentes nas várias esferas de nossa sociedade.</div>
        </li>
        -->
        <xsl:variable name="id"><xsl:value-of select="@id"/></xsl:variable>
        
        <li>
            <a name="{@id}_ref"/>
            <xsl:apply-templates select="*|text()"/>
            <!-- 
                adiciona "back". Concluimos que há problema para múltiplas
                menções, além disso, javascript não funcionaria no modo leitura
                Fica comentado se, por acaso, decidir implementar a volta
                <xsl:apply-templates select="." mode="go_to_xref"/>
            -->
        </li>
    </xsl:template>

    <xsl:template match="fn[@id]/label | author-notes/*[@id]/label">
        <span class="xref big"><xsl:apply-templates select="*|text()"/></span>
    </xsl:template>
</xsl:stylesheet>
