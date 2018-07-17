<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xlink="http://www.w3.org/1999/xlink" 
    version="1.0">
	<xsl:template match="article" mode="article-meta-product">
		<xsl:apply-templates select="front/article-meta//product"></xsl:apply-templates>
	</xsl:template>
	
	<xsl:template match="article-meta/product">
		<xsl:variable name="sep"><xsl:apply-templates select="text()"></xsl:apply-templates></xsl:variable>
        <!--
		<xsl:comment> <xsl:value-of select="$sep"/></xsl:comment>
        -->
		<div>
			<xsl:choose>
				<xsl:when test=".//graphic or .//inline-graphic">
					<xsl:attribute name="class">articleReferral</xsl:attribute>
					<div class="arPicture">
						<xsl:apply-templates select=".//graphic | .//inline-graphic"></xsl:apply-templates>
					</div>
				</xsl:when>
				<xsl:otherwise>
					<xsl:attribute name="class">articleReferral noPicture</xsl:attribute>
				</xsl:otherwise>
			</xsl:choose>
			
			<div class="arText">
				<xsl:choose>
					<xsl:when test="normalize-space($sep)=''">
						<xsl:apply-templates select="*" mode="build"></xsl:apply-templates>
					</xsl:when>
					<xsl:otherwise>
						<xsl:apply-templates select="*|text()" mode="display"></xsl:apply-templates>
					</xsl:otherwise>
				</xsl:choose>
			</div>			
		</div>
	</xsl:template>
	
	<xsl:template match="product//*" mode="build">
		<xsl:choose>
			<xsl:when test="*">
				<xsl:apply-templates select="*|text()" mode="build"></xsl:apply-templates>		
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select="*|text()" mode="display"/>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:if test="position()!=last()"><xsl:if test="not(contains('.,;',substring(text(),string-length(text()))))">. </xsl:if></xsl:if>
	</xsl:template>
	
	<xsl:template match="product//*[@xlink:href]" mode="display">
        <!--
		<xsl:comment> ignored <xsl:value-of select="name()"/> </xsl:comment>
        -->
	</xsl:template>
	
	<xsl:template match="product/person-group" mode="display">
		<xsl:apply-templates select="name" mode="build"/>.
		<!-- <xsl:if test="position()!=last()"><xsl:if test="not(contains('.,;',substring(text(),string-length(text()))))">. </xsl:if></xsl:if> -->
	</xsl:template>
	
	<xsl:template match="product/person-group/name/surname" mode="build">
		<xsl:value-of select="."/>,
	</xsl:template>
	
	<xsl:template match="product/isbn">
		<xsl:if test="not(contains(.,'ISBN'))">ISBN </xsl:if><xsl:value-of select="."/>
	</xsl:template>
	
	<xsl:template match="product/person-group" mode="build">
		<xsl:apply-templates select="name" mode="build"/>.
		<!-- <xsl:if test="position()!=last()"><xsl:if test="not(contains('.,;',substring(text(),string-length(text()))))">. </xsl:if></xsl:if> -->
	</xsl:template>
	
	<xsl:template match="product/person-group/name" mode="build">
		<xsl:apply-templates select="*" mode="build"/><xsl:if test="position()!=last()">; </xsl:if>
	</xsl:template>

	<xsl:template match="product/publisher-loc" mode="build">
		<xsl:apply-templates select="*|text()" mode="build"></xsl:apply-templates>
		<xsl:if test="position()!=last()"><xsl:if test="not(contains('.,;',substring(text(),string-length(text()))))">: </xsl:if></xsl:if>
	</xsl:template>
	
	<xsl:template match="product/publisher-name" mode="build">
		<xsl:apply-templates select="*|text()" mode="build"></xsl:apply-templates>
		<xsl:if test="position()!=last()"><xsl:if test="not(contains('.,;',substring(text(),string-length(text()))))">, </xsl:if></xsl:if>
	</xsl:template>
	
</xsl:stylesheet>
