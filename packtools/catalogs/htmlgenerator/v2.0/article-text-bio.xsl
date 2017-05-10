<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    version="1.0" >
    <xsl:template match="bio//fig" mode="modal"></xsl:template>
    
    <xsl:template match="bio" mode="bio-picture">
        <xsl:apply-templates select=".//fig" mode="bio-picture"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="bio//fig//title">
        <strong><xsl:apply-templates select="*|text()"></xsl:apply-templates></strong>
    </xsl:template>
    
    <xsl:template match="bio//fig" mode="bio-picture">
        <div class="arPicture">
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </div>
    </xsl:template>
    
    <xsl:template match="bio//fig">
    </xsl:template>
    
    <xsl:template match="back/bio" mode="back-section-content">
        <div>
            <xsl:attribute name="class">articleReferral
                <xsl:choose>
                    <xsl:when test=".//graphic"> biography</xsl:when>
                    <xsl:otherwise> noPicture</xsl:otherwise>
                </xsl:choose>
            </xsl:attribute>
            <xsl:apply-templates select="." mode="bio-picture"></xsl:apply-templates>
            <div class="arText">
                <xsl:apply-templates select="*[name()!='title']"></xsl:apply-templates>
            </div>
        </div>        
    </xsl:template>
</xsl:stylesheet>

<!-- 
    
    <div class="articleReferral biography">
									<div class="arPicture">
										<img src="../static/trash/bibliografia.jpg" width="98" height="132" alt="">
										<small>
											Courtesy of Philip James
											<span>Philip James</span>
										</small>
									</div>
									<div class="arText">
										<h2>Professor Philip James</h2>
										<p>Professor Philip James has devoted the last four decades to the study of obesity and raising awareness of the problem. He trained in physiology and medicine at University College London, and did postgraduate training in Jamaica, the United Kingdom and the United States of America. From 1971 to 1974 he worked on the first national study of obesity in the United Kingdom and in 1976 established the Dunn Clinical Nutrition Centre in Cambridge to research obesity and the dietary aspects of adult chronic diseases. In 1982 he was appointed Director of the Rowett Research Institute in Aberdeen and in 1996 returned to the London School of Hygiene with his newly established International Obesity Task Force (IOTF). Working as an adviser to WHO, he helped to establish strategies for tackling the current global epidemic of obesity and adult chronic diseases.</p>
									</div>
								</div>

								<div class="articleReferral noPicture">
									<div class="arText">
										<h2>Professor Philip James</h2>
										<p>Professor Philip James has devoted the last four decades to the study of obesity and raising awareness of the problem. He trained in physiology and medicine at University College London, and did postgraduate training in Jamaica, the United Kingdom and the United States of America. From 1971 to 1974 he worked on the first national study of obesity in the United Kingdom and in 1976 established the Dunn Clinical Nutrition Centre in Cambridge to research obesity and the dietary aspects of adult chronic diseases. In 1982 he was appointed Director of the Rowett Research Institute in Aberdeen and in 1996 returned to the London School of Hygiene with his newly established International Obesity Task Force (IOTF). Working as an adviser to WHO, he helped to establish strategies for tackling the current global epidemic of obesity and adult chronic diseases.</p>
									</div>
								</div>
								
								-->