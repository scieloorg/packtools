<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="/" mode="js"><!--FIXME-->
        <script src="{$JS_PATH}/vendor/jquery-1.11.0.min.js"></script>
        <script src="{$JS_PATH}/vendor/bootstrap.min.js"></script>
        <script src="{$JS_PATH}/vendor/jquery-ui.min.js"></script>
        <script src="{$JS_PATH}/plugins.js"></script>
        <script src="{$JS_PATH}/main.js"></script>
    </xsl:template>
    <xsl:template match="/" mode="css"><!--FIXME-->
        <link rel="stylesheet" href="{$CSS_PATH}/bootstrap.min.css"/>
        <link rel="stylesheet" href="{$CSS_PATH}/scielo-portal.css"/>
        <link rel="stylesheet" href="{$CSS_PATH}/scielo-print.css" media="print"/>
    	<style>
    		table {
				font-size: 90%;
				background-color: #E8F3F8;
				font-family: courier;
			}
			.footnote {
			font-size: 70%;
			
			font-family: courier;
			}
			
    	</style>
    </xsl:template>
    <xsl:template match="/">
       <html>
       <xsl:text>
            <!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
            <!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
            <!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
            <!--[if gt IE 8]> <html class="no-js"> <![endif]-->
       </xsl:text>
	<head>
		<meta charset="utf-8"/>
		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>
				
		<xsl:apply-templates select="." mode="css"></xsl:apply-templates>

		<xsl:text>
		<!--[if lt IE 9]>
			<script src="../static/js/vendor/html5-3.6-respond-1.1.0.min.js"></script>
		<![endif]-->
            </xsl:text>
	</head>
	<body class="journal article">
		<a name="top"></a>
		<xsl:apply-templates select="." mode="article"></xsl:apply-templates>
        <xsl:apply-templates select="." mode="js"/>
	</body>
</html>
   </xsl:template>
</xsl:stylesheet>