<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
	<xsl:template match="article" mode="article-meta-product">
		<xsl:apply-templates select=".//article-meta//product"></xsl:apply-templates>
	</xsl:template>
	
	<xsl:template match="article-meta/product">
		<xsl:variable name="sep"><xsl:apply-templates select="text()"></xsl:apply-templates></xsl:variable>
		<xsl:comment> <xsl:value-of select="$sep"/></xsl:comment>
		<blockquote>
		<xsl:choose>
			<xsl:when test="normalize-space($sep)=''">
				<xsl:apply-templates select="*" mode="build"></xsl:apply-templates>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select="*|text()"></xsl:apply-templates>
			</xsl:otherwise>
		</xsl:choose>
		</blockquote>
	</xsl:template>
	
	<xsl:template match="product//*" mode="build">
		<xsl:choose>
			<xsl:when test="*">
				<xsl:apply-templates select="*|text()" mode="build"></xsl:apply-templates>		
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select="."></xsl:apply-templates>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:if test="position()!=last()"><xsl:if test="not(contains('.,;',substring(text(),string-length(text()))))">. </xsl:if></xsl:if>
	</xsl:template>
	
	<xsl:template match="product/person-group">
		<xsl:apply-templates select="name" mode="build"/>.
		<!-- <xsl:if test="position()!=last()"><xsl:if test="not(contains('.,;',substring(text(),string-length(text()))))">. </xsl:if></xsl:if> -->
	</xsl:template>
	
	<xsl:template match="product/person-group/name">
		<xsl:apply-templates select="*"/><xsl:if test="position()!=last()">; </xsl:if>
	</xsl:template>
	
	<xsl:template match="product/person-group/name/surname">
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
		<xsl:apply-templates select="*"/><xsl:if test="position()!=last()">; </xsl:if>
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