<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">

    <xsl:template match="table-wrap[@id] | table-wrap-group[@id]" mode="table-id">
        <xsl:value-of select="translate(@id,'.','_')"/>
    </xsl:template>

    <xsl:template match="table-wrap[@id] | table-wrap-group[@id]" mode="modal">
        <xsl:variable name="id"><xsl:apply-templates select="." mode="table-id"/></xsl:variable>

        <div class="modal fade ModalTables" id="ModalTable{$id}" tabindex="-1" role="dialog" aria-hidden="true">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">

                    <xsl:apply-templates select="." mode="modal-header"/>
                    <xsl:apply-templates select="." mode="modal-body"/>
                    
                    <div class="modal-footer">
                        <xsl:apply-templates select=".//table-wrap-foot" mode="modal-footer"/>
                    </div>

                </div>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="table-wrap[@id] | table-wrap-group[@id]" mode="modal-header">
        <!--
        Template para criar a área do título da tabela
        -->
        <div class="modal-header">
            <h5 class="modal-title">
                <span class="material-icons-outlined">table_chart</span>
                <xsl:apply-templates select="." mode="modal-header-label-caption"/>
            </h5>
            <button class="btn-close" data-bs-dismiss="modal">
                <xsl:attribute name="aria-label">
                     <xsl:apply-templates select="." mode="interface">
                         <xsl:with-param name="text">Close</xsl:with-param>
                     </xsl:apply-templates>
                </xsl:attribute>
            </button>
            <xsl:variable name="location"><xsl:apply-templates select="." mode="original-file-location"/></xsl:variable>
            <xsl:if test="$location!=''">
                <a class="link-newWindow showTooltip" href="{$location}" target="_blank"  data-placement="left">
                <xsl:attribute name="title"><xsl:apply-templates select="." mode="interface">
                    <xsl:with-param name="text">Open new window</xsl:with-param>
                </xsl:apply-templates></xsl:attribute>
                <span class="sci-ico-newWindow"></span></a>
            </xsl:if>
            
            <h4 class="modal-title">
                <span class="sci-ico-fileTable"></span>
                <xsl:apply-templates select="." mode="modal-header-label-caption"/>
            </h4>
        </div>
    </xsl:template>
    
    <xsl:template match="table-wrap-group[@id]" mode="modal-header-label-caption">
        <!--
        Template para os títulos da tabela
        -->
        <xsl:apply-templates select="table-wrap" mode="modal-header-label-caption"/>
    </xsl:template>

    <xsl:template match="table-wrap" mode="modal-header-label-caption">
        <!--
        Template para o título da tabela
        -->
        <xsl:apply-templates select="." mode="inline-label-caption"/><br/>
    </xsl:template>

    <xsl:template match="table-wrap-group" mode="modal-body">
        <xsl:apply-templates select=".//table-wrap" mode="modal-body"/>
    </xsl:template>

    <xsl:template match="*[table] | *[graphic] | *[alternatives]" mode="modal-body">
        <!--
        Template para criar a área do corpo da tabela
        -->
        <div class="modal-body">
            <xsl:choose>
                <xsl:when test="table">
                    <xsl:apply-templates select="table"/>
                </xsl:when>
                <xsl:when test="graphic">
                    <xsl:apply-templates select="graphic"/>
                </xsl:when>
                <xsl:when test="alternatives">
                    <xsl:apply-templates select="alternatives"/>
                </xsl:when>
            </xsl:choose>
        </div>
    </xsl:template>   
    
    <xsl:template match="*" mode="modal-footer">
        <xsl:choose>
            <xsl:when test="*">
                <xsl:apply-templates select="*" mode="modal-footer"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="."/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>   
    
    <xsl:template match="@*" mode="modal-footer">
        <xsl:attribute name="{name()}"><xsl:value-of select="."/></xsl:attribute>
    </xsl:template>   
    
    <xsl:template match="text()" mode="modal-footer">
        <xsl:value-of select="."/>
    </xsl:template>   
        
    <xsl:template match="table-wrap-foot" mode="modal-footer">
        <div class="ref-list">
            <ul class="refList footnote">
                <xsl:apply-templates select="*" mode="modal-footer"/>
            </ul>
        </div>
    </xsl:template>

    <xsl:template match="table-wrap-foot//fn" mode="modal-footer">
        <li>
            <xsl:apply-templates select="@*| *|text()" mode="modal-footer"/>
        </li>
    </xsl:template>

    <xsl:template match="table-wrap-foot//label" mode="modal-footer">
        <sup class="xref big"><xsl:value-of select="."/></sup>
    </xsl:template>

    <xsl:template match="table-wrap-foot//p" mode="modal-footer">
        <div>
            <xsl:apply-templates select="*|text()"  mode="modal-footer"/>
        </div>
    </xsl:template>

    <xsl:template match="ref" mode="select">
        <xsl:param name="xref_nodes"></xsl:param>
        <xsl:variable name="id" select="@id"></xsl:variable>
        <xsl:if test="$xref_nodes[@rid=$id]">
            <xsl:apply-templates select="." mode="table-wrap-foot"></xsl:apply-templates>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="fn" mode="select">
        <xsl:param name="xref_nodes"></xsl:param>
        <xsl:variable name="id" select="@id"></xsl:variable>
        <xsl:if test="$xref_nodes[@rid=$id]">
            <xsl:apply-templates select="." mode="list-item"></xsl:apply-templates>
        </xsl:if>
    </xsl:template>
    
</xsl:stylesheet>