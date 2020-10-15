<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="*" mode="article-modals">
        <!--
            Cria todos os modals do documento
        -->
        <!-- modal do contribs -->
        <xsl:apply-templates select="." mode="modal-contribs"/>

        <!-- modal que apresenta juntos figuras, tabelas e fórmulas -->
        <xsl:apply-templates select="." mode="modal-all-items"/>

        <!-- cria um modal para cada figura -->
        <xsl:apply-templates select="." mode="modal-figs"/>
        
        <!-- cria um modal para cada tabela -->
        <xsl:apply-templates select="." mode="modal-tables"/>
        
        <!-- cria um modal para cada fórmula -->
        <xsl:apply-templates select="." mode="modal-disp-formulas"/>
        
        <!-- cria um modal para como citar -->
        <xsl:apply-templates select="." mode="modal-how2cite"/>
    </xsl:template>
    
    <xsl:template match="*" mode="modal-tables">
        <!-- cria um modal para cada tabela -->
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']">
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//body//table-wrap" mode="modal"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="./body//table-wrap" mode="modal"/>                    
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="*" mode="modal-disp-formulas">
        <!-- cria um modal para cada fórmula -->
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']">
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//body//disp-formula" mode="modal"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="./body//disp-formula" mode="modal"/>                    
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="*" mode="modal-figs">
        <!-- cria um modal para cada figura -->
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']">
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//body" mode="modal-figs"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="./body" mode="modal-figs"/>                    
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="body" mode="modal-figs">
        <!-- cria um modal para cada figura existente no body-->
        <xsl:apply-templates select=".//fig-group[@id] | .//fig[@id]" mode="modal"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="*" mode="modal-all-items">
        <!-- modal que apresenta juntos figuras, tabelas e fórmulas -->
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']">
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//body" mode="modal-all-items"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="./body" mode="modal-all-items"/>                    
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="body" mode="modal-all-items">
        <!-- modal que apresenta juntos figuras, tabelas e fórmulas presentes dentro de body-->
         <xsl:if test=".//fig or .//table-wrap or .//disp-formula[@id]">
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
                             <h4 class="modal-title"><xsl:value-of select="$graphic_elements_title"/></h4>
                         </div>
                         <div class="modal-body">
                             <ul class="nav nav-tabs md-tabs" role="tablist">
                                <xsl:if test=".//fig">
                                    <!--
                                        cria aba com rótulo "Figures" e quantidade de figuras
                                    -->
                                    <li role="presentation" class="col-md-4 col-sm-4 active">
                                         <a href="#figures" aria-controls="figures" role="tab" data-toggle="tab">
                                             <xsl:apply-templates select="." mode="interface">
                                                 <xsl:with-param name="text">Figures</xsl:with-param>
                                             </xsl:apply-templates>
                                             (<xsl:value-of select="count(.//fig-group[@id])+count(.//fig[@id])"/>)
                                         </a>
                                     </li>
                                 </xsl:if>
                                 <xsl:if test=".//table-wrap">
                                     <!--
                                        cria aba com rótulo "Tables" e quantidade de tabelas
                                    -->
                                     <li role="presentation">
                                         <xsl:attribute name="class">col-md-4 col-sm-4 <xsl:if test="not(.//fig)"> active</xsl:if></xsl:attribute>
                                         <a href="#tables" aria-controls="tables" role="tab" data-toggle="tab">
                                             <xsl:apply-templates select="." mode="interface">
                                                 <xsl:with-param name="text">Tables</xsl:with-param>
                                             </xsl:apply-templates>
                                             (<xsl:value-of select="count(.//table-wrap-group)+count(.//*[table-wrap and name()!='table-wrap-group']//table-wrap)"/>)
                                         </a>
                                     </li>
                                 </xsl:if>
                                 <xsl:if test=".//disp-formula[@id]">
                                     <!--
                                        cria aba com rótulo "Scheme" e quantidade de fórmulas
                                    -->
                                     <li role="presentation">
                                         <xsl:attribute name="class">col-md-4 col-sm-4<xsl:if test="not(.//fig) and not(.//table-wrap)"> active</xsl:if></xsl:attribute>
                                         
                                         <a href="#schemes" aria-controls="schemes" role="tab" data-toggle="tab">
                                             <xsl:apply-templates select="." mode="interface">
                                                 <xsl:with-param name="text">Formulas</xsl:with-param>
                                             </xsl:apply-templates>
                                             (<xsl:value-of select="count(.//disp-formula[@id])"/>)
                                         </a>
                                     </li>
                                 </xsl:if>
                             </ul>
                             <div class="clearfix"></div>
                             <div class="tab-content">
                                 <xsl:if test=".//fig">
                                    <!--
                                        cria o conteúdo da aba com rótulo "Figures"
                                    -->
                                     <div role="tabpanel" class="tab-pane active" id="figures">
                                         <xsl:apply-templates select=".//fig-group[@id] | .//fig[@id]" mode="modal-all-item"></xsl:apply-templates>
                                     </div>
                                 </xsl:if>
                                 <xsl:if test=".//table-wrap">
                                    <!--
                                        cria o conteúdo da aba com rótulo "Tables"
                                    -->
                                     <div role="tabpanel">
                                         <xsl:attribute name="class">tab-pane <xsl:if test="not(.//fig)"> active</xsl:if></xsl:attribute>
                                         <xsl:attribute name="id">tables</xsl:attribute>
                                         
                                         <xsl:apply-templates select=".//table-wrap-group[table-wrap] | .//*[table-wrap and name()!='table-wrap-group']/table-wrap" mode="modal-all-item"></xsl:apply-templates>
                                     </div>
                                 </xsl:if>
                                 <xsl:if test=".//disp-formula[@id]">
                                    <!--
                                        cria o conteúdo da aba com rótulo "Formulas"
                                    -->
                                     <div role="tabpanel">
                                         <xsl:attribute name="class">tab-pane <xsl:if test="not(.//fig) and not(.//table-wrap)"> active</xsl:if></xsl:attribute>
                                         <xsl:attribute name="id">schemes</xsl:attribute>
                                         
                                         <xsl:apply-templates select=".//disp-formula[@id]" mode="modal-all-item"></xsl:apply-templates>
                                     </div>
                                 </xsl:if>
                             </div>
                         </div>
                     </div>
                 </div>
             </div>
         </xsl:if>
    </xsl:template>
    
    <xsl:template match="fig-group[@id]" mode="modal-all-item">
        <!--
            cria no conteúdo da ABA "Figures" a miniatura e legenda de uma figura
            (cujo label e caption estão em mais de um idioma)
        -->       
        <div class="row fig">
            <xsl:apply-templates select="." mode="modal-all-item-display"></xsl:apply-templates>
            <xsl:apply-templates select="fig[@xml:lang=$TEXT_LANG]" mode="modal-all-item-info"></xsl:apply-templates>
        </div>        
    </xsl:template>
    <xsl:template match="fig[@id]" mode="modal-all-item">
        <!--
            cria no conteúdo da ABA "Figures" a miniatura e legenda de uma figura
            (cujo label e caption estão em apenas um idioma)
        -->         
        <div class="row fig">
            <!-- miniatura -->
            <xsl:apply-templates select="." mode="modal-all-item-display"></xsl:apply-templates>
            <!-- legenda -->
            <xsl:apply-templates select="." mode="modal-all-item-info"></xsl:apply-templates>
        </div>        
    </xsl:template>
    
    <xsl:template match="fig[@id] | fig-group[@id]" mode="modal-all-item-display">
        <!--
            cria a miniatura de uma figura no conteúdo da ABA "Figures" 
        --> 
        <xsl:choose>
            <xsl:when test="graphic">
                <xsl:variable name="location"><xsl:apply-templates select="." mode="file-location"/></xsl:variable>
                <div class="col-md-4">
                    <a data-toggle="modal" data-target="#ModalFig{@id}">
                        <div class="thumb" style="background-image: url({$location});">
                            Thumbnail
                            <div class="zoom"><span class="sci-ico-zoom"></span></div>
                        </div>
                    </a>
                </div>                
            </xsl:when>
            <xsl:otherwise>
                <div class="col-md-4">
                    <a data-toggle="modal" data-target="#ModalFig{@id}">
                        <div>
                            <xsl:apply-templates select="disp-formula"></xsl:apply-templates>
                        </div>
                    </a>
                </div>   
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="fig" mode="modal-all-item-info">
        <!--
            cria a legenda de uma figura no conteúdo da ABA "Figures" 
        -->
        <div class="col-md-8">
            <xsl:apply-templates select="." mode="label-caption-thumb"></xsl:apply-templates>
        </div>
    </xsl:template>
    
    <xsl:template match="table-wrap-group[table-wrap]" mode="modal-all-item">
        <!--
            cria no conteúdo da ABA "Tables" a miniatura e legenda de uma tabela
            do idioma selecionado
        -->         
        <div class="row table">
            <!-- miniatura -->
            <xsl:apply-templates select="." mode="modal-all-item-display"></xsl:apply-templates>
            <!-- legenda -->
            <xsl:apply-templates select="table-wrap[@xml:lang=$TEXT_LANG]" mode="modal-all-item-info"></xsl:apply-templates>
        </div>        
    </xsl:template>
    
    <xsl:template match="table-wrap[not(@xml:lang)]" mode="modal-all-item">
        <!--
            cria no conteúdo da ABA "Tables" a miniatura e legenda de uma tabela
            que não depende do idioma
        -->       
        <div class="row table">
            <!-- miniatura -->
            <xsl:apply-templates select="." mode="modal-all-item-display"></xsl:apply-templates>
            <!-- legenda -->
            <xsl:apply-templates select="." mode="modal-all-item-info"></xsl:apply-templates>
        </div>        
    </xsl:template>
    
    <xsl:template match="table-wrap | table-wrap-group" mode="modal-all-item-display">
        <!--
            cria no conteúdo da ABA "Tables" a miniatura de uma tabela
            que não depende do idioma
        -->
        <xsl:variable name="location"><xsl:apply-templates select="." mode="file-location"/></xsl:variable>
        <div class="col-md-4">
            <a data-toggle="modal" data-target="#ModalTable{@id}">
                <div class="thumbOff">
                    Thumbnail
                    <div class="zoom"><span class="sci-ico-zoom"></span></div>
                </div>
            </a>
        </div>
    </xsl:template>
    
    <xsl:template match="table-wrap" mode="modal-all-item-info">
        <!--
            cria no conteúdo da ABA "Tables" a legenda de uma tabela
        -->
        <div class="col-md-8">
            <xsl:apply-templates select="." mode="label-caption-thumb"></xsl:apply-templates>
        </div>
    </xsl:template>
    
    <xsl:template match="disp-formula[@id]" mode="modal-all-item">
        <!--
            cria no conteúdo da ABA "Scheme" a miniatura e legenda de uma fórmula
        -->       
        <div class="row fig">
            <!-- miniatura -->
            <xsl:apply-templates select="." mode="modal-all-item-display"></xsl:apply-templates>
            <!-- legenda -->
            <xsl:apply-templates select="." mode="modal-all-item-info"></xsl:apply-templates>
        </div>        
    </xsl:template>
     
    <xsl:template match="disp-formula[@id]" mode="modal-all-item-display">
        <!--
            cria no conteúdo da ABA "Schemes" a miniatura de uma fórmula
        -->
        <xsl:variable name="location"><xsl:apply-templates select="." mode="file-location"/></xsl:variable>
        <div class="col-md-4">
            <a data-toggle="modal" data-target="#ModalScheme{@id}">
                <div>
                    <xsl:choose>
                        <xsl:when test="graphic">
                            <xsl:attribute name="class">thumb</xsl:attribute>
                            <xsl:attribute name="style">background-image: url(<xsl:value-of select="$location"/>);</xsl:attribute>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:attribute name="class">thumbOff</xsl:attribute>
                        </xsl:otherwise>
                    </xsl:choose>
                    Thumbnail
                    <div class="zoom"><span class="sci-ico-zoom"></span></div>
                </div>
            </a>
        </div>
    </xsl:template>
    
    <xsl:template match="disp-formula[@id]" mode="modal-all-item-info">
        <!--
            cria no conteúdo da ABA "Schemes" a legenda de uma fórmula
        -->
        <div class="col-md-8">
            <xsl:apply-templates select="label"></xsl:apply-templates>
        </div>
    </xsl:template>
    
    
</xsl:stylesheet>