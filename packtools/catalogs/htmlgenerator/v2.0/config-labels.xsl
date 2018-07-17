<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:variable name="LABELS" select="document('config-labels.xml')//term"></xsl:variable>
    
    <xsl:variable name="graphic_elements_title"><xsl:if test=".//fig">
        <xsl:apply-templates select="." mode="interface">
            <xsl:with-param name="text">Figures</xsl:with-param>
        </xsl:apply-templates>
        <xsl:if test=".//table-wrap or .//disp-formula[@id]"> | </xsl:if>
    </xsl:if>
        <xsl:if test=".//table-wrap">
            <xsl:apply-templates select="." mode="interface">
                <xsl:with-param name="text">Tables</xsl:with-param>
            </xsl:apply-templates>
            <xsl:if test=".//disp-formula[@id]"> | </xsl:if>
        </xsl:if>
        <xsl:if test=".//disp-formula[@id]">
            <xsl:apply-templates select="." mode="interface">
                <xsl:with-param name="text">Formulas</xsl:with-param>
            </xsl:apply-templates>
        </xsl:if></xsl:variable>
    
    <xsl:template match="*|@*|text()" mode="translate">
        <xsl:param name="term"></xsl:param>
        <xsl:param name="lang"></xsl:param>
        <xsl:choose>
            <xsl:when test="$LABELS[name=$term]//name[@lang=$lang]">
                <xsl:value-of select="$LABELS[name=$term]//name[@lang=$lang]"/>
            </xsl:when>
            <xsl:when test="$LABELS[name=$term]//name[@lang='en']">
                <xsl:value-of select="$LABELS[name=$term]//name[@lang='en']"/>
            </xsl:when>
            <xsl:when test="$LABELS[name=$term]">
                <xsl:value-of select="$LABELS[name=$term]//name[1]"/>
            </xsl:when>
            <xsl:otherwise><xsl:value-of select="$term"/></xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="*|@*|text()" mode="text-labels">
        <xsl:param name="text"></xsl:param>
        <xsl:apply-templates select="." mode="translate">
            <xsl:with-param name="term"><xsl:value-of select="$text"/></xsl:with-param>
            <xsl:with-param name="lang"><xsl:value-of select="$TEXT_LANG"/></xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="*|@*|text()" mode="interface">
        <xsl:param name="text"></xsl:param>
        <xsl:apply-templates select="." mode="translate">
            <xsl:with-param name="term"><xsl:value-of select="$text"/></xsl:with-param>
            <xsl:with-param name="lang"><xsl:value-of select="$INTERFACE_LANG"/></xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>
        
    <xsl:template match="*" mode="generated-label">
        <!--
        <xsl:comment> generated-label </xsl:comment>
        -->
        <xsl:apply-templates select="." mode="translate">
            <xsl:with-param name="term"><xsl:value-of select="name()"/></xsl:with-param>
            <xsl:with-param name="lang"><xsl:choose>
                <xsl:when test="@xml:lang"><xsl:value-of select="@xml:lang"/></xsl:when>
                <xsl:otherwise><xsl:value-of select="$TEXT_LANG"/></xsl:otherwise>
            </xsl:choose></xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>
    <xsl:template match="abstract | trans-abstract" mode="generated-label">
        <!--
        <xsl:comment> generated-label </xsl:comment>
        -->
        <xsl:apply-templates select="." mode="translate">
            <xsl:with-param name="term">Abstract</xsl:with-param>
            <xsl:with-param name="lang"><xsl:choose>
                <xsl:when test="@xml:lang"><xsl:value-of select="@xml:lang"/></xsl:when>
                <xsl:otherwise><xsl:value-of select="$TEXT_LANG"/></xsl:otherwise>
            </xsl:choose></xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>
    <xsl:template match="@pub-type" mode="generated-label">
        <xsl:apply-templates select="." mode="interface">
            <xsl:with-param name="text"><xsl:choose>
                <xsl:when test=".='epub'">Online</xsl:when>
                <xsl:otherwise>Print</xsl:otherwise>
            </xsl:choose></xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="history/date" mode="generated-label">
        <xsl:apply-templates select="." mode="text-labels">
            <xsl:with-param name="text"><xsl:value-of select="@date-type"/></xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="*" mode="title">
        <!--
        <xsl:comment> * mode=title </xsl:comment>
        -->
        <xsl:apply-templates select="label"/>
        <xsl:if test="label and title"> &#160; </xsl:if>
        <xsl:apply-templates select="title"/>
        <xsl:if test="not(label) and not(title)">
            <xsl:apply-templates select="." mode="generated-label"/>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="ref-list" mode="title">
        <xsl:choose>
            <xsl:when test="$article/@xml:lang=$TEXT_LANG and title">
                <xsl:apply-templates select="title"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="." mode="text-labels">
                    <xsl:with-param name="text">ref-list</xsl:with-param>
                </xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="*" mode="label-caption">
        <!--
        <xsl:comment> * mode=label-caption </xsl:comment>
        -->
        <xsl:apply-templates select="label"/>
        <xsl:if test="label and caption"> &#160; </xsl:if>
        <xsl:apply-templates select="caption"/>
    </xsl:template>
    
    <xsl:template match="*[label or caption]" mode="label-caption-thumb">
        <strong><xsl:apply-templates select="label" mode="label-caption-thumb"/></strong><br/>
        <xsl:apply-templates select="caption" mode="label-caption-thumb"/>
    </xsl:template>
    
    <xsl:template match="label|caption| *" mode="label-caption-thumb">
        <xsl:apply-templates select="*|text()" mode="label-caption-thumb"></xsl:apply-templates>
    </xsl:template>
    <xsl:template match="xref" mode="label-caption-thumb">
    </xsl:template>
    
    <xsl:template match="fn" mode="label">
        
    </xsl:template>
</xsl:stylesheet>
