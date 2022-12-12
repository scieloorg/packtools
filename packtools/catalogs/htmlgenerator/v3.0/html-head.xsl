<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:template match="*" mode="html-head-title">
		<title>
			<xsl:apply-templates select=".//article/journal-title"/>
		</title>
	</xsl:template>
	
	<xsl:template match="*" mode="html-head-meta">
	</xsl:template>

</xsl:stylesheet>
