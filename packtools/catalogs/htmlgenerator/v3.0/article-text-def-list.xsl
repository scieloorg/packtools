<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    
    <!--xsl:template match="def-list/def-item">
        <dl>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </dl>
    </xsl:template>
    
    <xsl:template match="term">
        <dt>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </dt>
    </xsl:template>
    
    <xsl:template match="def/p">
        <xsl:apply-templates select="*|text()"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="def">
        <dd> 
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </dd>
    </xsl:template-->
    
    <xsl:template match="def-list">
        <ul>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </ul>
    </xsl:template>
    
    <xsl:template match="def-item">
        <li>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </li>
    </xsl:template>
    
    <xsl:template match="term">
       <strong><xsl:apply-templates select="*|text()"></xsl:apply-templates></strong>
    </xsl:template>
    
    <xsl:template match="def/p">
        <span>&#160;<xsl:apply-templates select="*|text()"></xsl:apply-templates></span>
    </xsl:template>
   
    <xsl:template match="def-list[term-head and def-head]">
        <table class="table">
            <tr>
                <xsl:apply-templates select="term-head | def-head"></xsl:apply-templates>
            </tr>
            <xsl:apply-templates select="def-item"></xsl:apply-templates>
        </table>
    </xsl:template>
    <xsl:template match="term-head | def-head">
        <th>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </th>
    </xsl:template>
    <xsl:template match="def-list[term-head and def-head]//*">
        <td>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </td>
    </xsl:template>
    <xsl:template match="def-list[term-head and def-head]//term">
        <td>
            <strong><xsl:apply-templates select="*|text()"></xsl:apply-templates></strong>
        </td>
    </xsl:template>
    <xsl:template match="def-list[term-head and def-head]/def-item">
        <tr>
            <xsl:apply-templates select="*"></xsl:apply-templates>
        </tr>
    </xsl:template>
    
    
</xsl:stylesheet>