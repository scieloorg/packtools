<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="*" mode="article-modals">
        <xsl:apply-templates select="." mode="modal-contribs"/>
        <xsl:apply-templates select="." mode="modal-tables"/>
        <xsl:apply-templates select="." mode="modal-figs"/>
        <xsl:apply-templates select="." mode="modal-all-items"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="*" mode="modal-tables">
        <xsl:apply-templates select=".//table-wrap" mode="modal"></xsl:apply-templates>
    </xsl:template>
    <xsl:template match="*" mode="modal-figs">
        <xsl:apply-templates select=".//fig-group[fig] | .//*[not(fig-group)]/fig" mode="modal"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="*" mode="modal-all-items">
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG]">
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG]//body" mode="modal-all-items"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="./body" mode="modal-all-items"/>                    
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="body" mode="modal-all-items">
         <xsl:if test=".//fig or .//table-wrap or .//disp-formula">
             <div class="modal fade ModalDefault" id="ModalTablesFigures" tabindex="-1" role="dialog" aria-hidden="true">
                 <div class="modal-dialog">
                     <div class="modal-content">
                         <div class="modal-header">
                             <button type="button" class="close" data-dismiss="modal">
                                 <span aria-hidden="true">&#xd7;</span>
                                 <span class="sr-only">
                                     <xsl:apply-templates select="." mode="interface">
                                         <xsl:with-param name="text">Close</xsl:with-param>
                                     </xsl:apply-templates>
                                 </span>
                             </button>
                             <h4 class="modal-title">
                                 <xsl:if test=".//fig">
                                     <xsl:apply-templates select="." mode="interface">
                                         <xsl:with-param name="text">Figures</xsl:with-param>
                                     </xsl:apply-templates>
                                     <xsl:if test=".//table-wrap or .//disp-formula"> | </xsl:if>
                                 </xsl:if>
                                 <xsl:if test=".//table-wrap">
                                     <xsl:apply-templates select="." mode="interface">
                                         <xsl:with-param name="text">Tables</xsl:with-param>
                                     </xsl:apply-templates>
                                     <xsl:if test=".//disp-formula"> | </xsl:if>
                                 </xsl:if>
                                 <xsl:if test=".//disp-formula">
                                     <xsl:apply-templates select="." mode="interface">
                                         <xsl:with-param name="text">Formulas</xsl:with-param>
                                     </xsl:apply-templates>
                                 </xsl:if>
                             </h4>
                         </div>
                         <div class="modal-body">
                             <ul class="nav nav-tabs md-tabs" role="tablist">
                                <xsl:if test=".//fig">
                                     <li role="presentation" class="col-md-4 active">
                                         <a href="#figures" aria-controls="figures" role="tab" data-toggle="tab">
                                             <xsl:apply-templates select="." mode="interface">
                                                 <xsl:with-param name="text">Figures</xsl:with-param>
                                             </xsl:apply-templates>
                                             (<xsl:value-of select="count(.//fig-group)+count(.//*[fig and name()!='fig-group']//fig)"/>)
                                         </a>
                                     </li>
                                 </xsl:if>
                                 <xsl:if test=".//table-wrap">
                                     <li role="presentation" class="col-md-4 active">
                                         <a href="#figures" aria-controls="figures" role="tab" data-toggle="tab">
                                             <xsl:apply-templates select="." mode="interface">
                                                 <xsl:with-param name="text">Tables</xsl:with-param>
                                             </xsl:apply-templates>
                                             (<xsl:value-of select="count(.//table-wrap-group)+count(.//*[table-wrap and name()!='table-wrap-group']//table-wrap)"/>)
                                         </a>
                                     </li>
                                 </xsl:if>
                                 <xsl:if test=".//disp-formula">
                                     <li role="presentation" class="col-md-4">
                                         <a href="#schemes" aria-controls="tables" role="tab" data-toggle="tab">
                                             <xsl:apply-templates select="." mode="interface">
                                                 <xsl:with-param name="text">Formulas</xsl:with-param>
                                             </xsl:apply-templates>
                                             (<xsl:value-of select="count(.//disp-formula)"/>)
                                         </a>
                                     </li>
                                 </xsl:if>
                             </ul>
                             <div class="clearfix"></div>
                             <div class="tab-content">
                                 <xsl:if test=".//fig">
                                     <div role="tabpanel" class="tab-pane active" id="figures">
                                         <xsl:apply-templates select=".//fig-group[fig] | .//*[name()!='fig-group']//fig" mode="modal-all-item"></xsl:apply-templates>
                                     </div>
                                 </xsl:if>
                                 <xsl:if test=".//table-wrap">
                                     <div role="tabpanel" class="tab-pane" id="tables">
                                         <xsl:apply-templates select=".//table-wrap-group[table-wrap] | .//*[name()!='table-wrap-group']//table-wrap" mode="modal-all-item"></xsl:apply-templates>
                                     </div>
                                 </xsl:if>
                                 <xsl:if test=".//disp-formula">
                                     <div role="tabpanel" class="tab-pane" id="schemes">
                                         <xsl:apply-templates select=".//disp-formula" mode="modal-all-item"></xsl:apply-templates>
                                         
                                     </div>
                                 </xsl:if>
                             </div>
                         </div>
                     </div>
                 </div>
             </div>
         </xsl:if>
    </xsl:template>
    
    <xsl:template match="fig-group[fig]" mode="modal-all-item">       
        <div class="row fig">
            <xsl:apply-templates select="." mode="modal-all-item-display"></xsl:apply-templates>
            <xsl:apply-templates select="fig[@xml:lang=$TEXT_LANG]" mode="modal-all-item-info"></xsl:apply-templates>
        </div>        
    </xsl:template>
    <xsl:template match="fig[not(@xml:lang)]" mode="modal-all-item">       
        <div class="row fig">
            <xsl:apply-templates select="." mode="modal-all-item-display"></xsl:apply-templates>
            <xsl:apply-templates select="." mode="modal-all-item-info"></xsl:apply-templates>
        </div>        
    </xsl:template>
    
    <xsl:template match="fig | fig-group" mode="modal-all-item-display">
        <xsl:variable name="location"><xsl:apply-templates select="." mode="file-location"/></xsl:variable>
        <div class="col-md-4">
            <a data-toggle="modal" data-target="#ModalFig{@id}ente">
                <div class="thumb" style="background-image: url({$location});">
                    Thumbnail
                    <div class="zoom"><span class="sci-ico-zoom"></span></div>
                </div>
            </a>
        </div>
    </xsl:template>
    
    <xsl:template match="fig" mode="modal-all-item-info">
        <div class="col-md-8">
            <xsl:apply-templates select="label | caption"></xsl:apply-templates>
        </div>
    </xsl:template>
    
    <xsl:template match="table-wrap-group[table-wrap]" mode="modal-all-item">       
        <div class="row table">
            <xsl:apply-templates select="." mode="modal-all-item-display"></xsl:apply-templates>
            <xsl:apply-templates select="table-wrap[@xml:lang=$TEXT_LANG]" mode="modal-all-item-info"></xsl:apply-templates>
        </div>        
    </xsl:template>
    
    <xsl:template match="table-wrap[not(@xml:lang)]" mode="modal-all-item">       
        <div class="row table">
            <xsl:apply-templates select="." mode="modal-all-item-display"></xsl:apply-templates>
            <xsl:apply-templates select="." mode="modal-all-item-info"></xsl:apply-templates>
        </div>        
    </xsl:template>
    
    <xsl:template match="table-wrap | table-wrap-group" mode="modal-all-item-display">
        <xsl:variable name="location"><xsl:apply-templates select="." mode="file-location"/></xsl:variable>
        <div class="col-md-4">
            <a data-toggle="modal" data-target="#ModalTable{@id}ente">
                <div class="thumb" style="background-image: url({$location});">
                    Thumbnail
                    <div class="zoom"><span class="sci-ico-zoom"></span></div>
                </div>
            </a>
        </div>
    </xsl:template>
    
    <xsl:template match="table-wrap" mode="modal-all-item-info">
        <div class="col-md-8">
            <xsl:apply-templates select="label | caption"></xsl:apply-templates>
        </div>
    </xsl:template>
    
    <xsl:template match="disp-formula" mode="modal-all-item">       
        <div class="row fig">
            <xsl:apply-templates select="." mode="modal-all-item-display"></xsl:apply-templates>
            <xsl:apply-templates select="fig[@xml:lang=$TEXT_LANG]" mode="modal-all-item-info"></xsl:apply-templates>
        </div>        
    </xsl:template>
     
    <xsl:template match="disp-formula" mode="modal-all-item-display">
        <xsl:variable name="location"><xsl:apply-templates select="." mode="file-location"/></xsl:variable>
        <div class="col-md-4">
            <a data-toggle="modal" data-target="#ModalScheme{@id}">
                <div class="thumb" style="background-image: url({$location});">
                    Thumbnail
                    <div class="zoom"><span class="sci-ico-zoom"></span></div>
                </div>
            </a>
        </div>
    </xsl:template>
    
    <xsl:template match="disp-formula" mode="modal-all-item-info">
        <div class="col-md-8">
            <xsl:apply-templates select="label"></xsl:apply-templates>
        </div>
    </xsl:template>
 
</xsl:stylesheet>