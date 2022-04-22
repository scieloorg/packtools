<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    
    <xsl:template match="table-wrap" mode="modal"/>
    <xsl:template match="table-wrap" mode="modal-header"/>
    <xsl:template match="table-wrap" mode="modal-body"/>
    <xsl:template match="table-wrap" mode="modal-footer"/>
    
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
                        <xsl:apply-templates select="." mode="modal-footer"/>
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
            <button type="button" class="close" data-dismiss="modal">
                <span aria-hidden="true">&#xd7;</span>
                <span class="sr-only">
                    <xsl:apply-templates select="." mode="interface">
                        <xsl:with-param name="text">Close</xsl:with-param>
                    </xsl:apply-templates>
                </span>
            </button>
            <!-- FIXME -->
            <!-- a class="link-newWindow showTooltip" href="" target="_blank"  data-placement="left">
                <xsl:attribute name="title"><xsl:apply-templates select="." mode="interface">
                    <xsl:with-param name="text">Open new window</xsl:with-param>
                </xsl:apply-templates></xsl:attribute>
                <span class="sci-ico-newWindow"></span></a -->
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
        <xsl:apply-templates select="." mode="label-caption"/><br/>
    </xsl:template>

    <xsl:template match="table-wrap-group[@id]" mode="modal-body">
        <xsl:apply-templates select="table-wrap" mode="modal-body"/>
    </xsl:template>

    <xsl:template match="table-wrap-group[@id]" mode="modal-footer">
        <xsl:apply-templates select="table-wrap" mode="modal-footer"/>
    </xsl:template>
    
    <xsl:template match="table-wrap[table] | table-wrap[graphic] | table-wrap[alternatives]" mode="modal-body">
        <!--
        Template para criar a área do corpo e nota de rodapé da tabela
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
    
    <xsl:template match="table-wrap[table-wrap-foot]" mode="modal-footer">
        <!--
        Template para criar a área do corpo e nota de rodapé da tabela
        -->
        <xsl:apply-templates select="table-wrap-foot"></xsl:apply-templates>
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