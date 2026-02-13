"""
Validation for ext-link elements according to SPS 1.10 specification.

Implements validations for external link elements to ensure:
- Mandatory attributes are present (@ext-link-type, @xlink:href)
- URL format is valid (starts with http:// or https://)
- ext-link-type values are in allowed list
- Link text is descriptive (accessibility)
- @xlink:title is present when text is generic or URL

Reference: https://docs.google.com/document/d/1GTv4Inc2LS_AXY-ToHT3HmO66UT0VAHWJNOIqzBNSgA/edit?tab=t.0#heading=h.n2z5yrri2aba
"""
import re
from packtools.sps.models.ext_link import ArticleExtLinks
from packtools.sps.validation.utils import build_response


class ExtLinkValidation:
    """
    Validates ext-link elements in scientific article XML.
    
    Validates presence of mandatory attributes, URL format, allowed values,
    and accessibility requirements (descriptive text).
    """
    
    # Generic phrases to avoid (case-insensitive)
    GENERIC_PHRASES = [
        "leia mais",
        "clique aqui",
        "acesse",
        "veja mais",
        "saiba mais",
        "click here",
        "read more",
        "see more",
        "learn more",
        "more info",
        "mais informações",
    ]
    
    # Allowed values for @ext-link-type
    ALLOWED_EXT_LINK_TYPES = [
        "uri",
        "doi",
        "pmid",
        "pmcid",
        "clinical-trial",
    ]
    
    def __init__(self, xmltree, params=None):
        """
        Initialize validation with XML tree and optional parameters.
        
        Parameters
        ----------
        xmltree : lxml.etree._Element
            The root element of the XML document
        params : dict, optional
            Configuration parameters including error levels
        """
        self.params = params or {}
        self.params.setdefault("ext_link_type_error_level", "CRITICAL")
        self.params.setdefault("xlink_href_error_level", "CRITICAL")
        self.params.setdefault("xlink_href_format_error_level", "ERROR")
        self.params.setdefault("ext_link_type_value_error_level", "ERROR")
        self.params.setdefault("descriptive_text_error_level", "WARNING")
        self.params.setdefault("xlink_title_error_level", "WARNING")
        
        self.xmltree = xmltree
        self.ext_links_model = ArticleExtLinks(xmltree)
    
    def validate_ext_link_type_presence(self, error_level=None):
        """
        Validate presence of @ext-link-type attribute (CRITICAL).
        
        SPS Rule: @ext-link-type is mandatory in all <ext-link> elements.
        
        Parameters
        ----------
        error_level : str, optional
            Override default error level (default: "CRITICAL")
        
        Yields
        ------
        dict
            Validation result for each ext-link
        """
        error_level = error_level or self.params.get("ext_link_type_error_level", "CRITICAL")
        
        for ext_link in self.ext_links_model.ext_links:
            ext_link_type = ext_link.get("ext_link_type")
            text = ext_link.get("text", "")[:50]  # First 50 chars for context
            
            is_valid = bool(ext_link_type)
            
            advice_text = 'Add @ext-link-type attribute to <ext-link> with text "{text}". Valid values: {allowed_values}'
            advice_params = {
                "text": text,
                "allowed_values": ", ".join(self.ALLOWED_EXT_LINK_TYPES),
            }
            
            parent = {
                "parent": ext_link.get("parent"),
                "parent_id": ext_link.get("parent_id"),
                "parent_article_type": ext_link.get("parent_article_type"),
                "parent_lang": ext_link.get("parent_lang"),
            }
            
            yield build_response(
                title="@ext-link-type attribute",
                parent=parent,
                item="ext-link",
                sub_item="@ext-link-type",
                validation_type="exist",
                is_valid=is_valid,
                expected="@ext-link-type attribute present",
                obtained=ext_link_type,
                advice=f'Add @ext-link-type attribute to <ext-link> with text "{text}". Valid values: {", ".join(self.ALLOWED_EXT_LINK_TYPES)}',
                data=ext_link,
                error_level=error_level,
                advice_text=advice_text,
                advice_params=advice_params,
            )
    
    def validate_xlink_href_presence(self, error_level=None):
        """
        Validate presence of @xlink:href attribute (CRITICAL).
        
        SPS Rule: @xlink:href is mandatory in all <ext-link> elements.
        
        Parameters
        ----------
        error_level : str, optional
            Override default error level (default: "CRITICAL")
        
        Yields
        ------
        dict
            Validation result for each ext-link
        """
        error_level = error_level or self.params.get("xlink_href_error_level", "CRITICAL")
        
        for ext_link in self.ext_links_model.ext_links:
            xlink_href = ext_link.get("xlink_href")
            text = ext_link.get("text", "")[:50]
            
            is_valid = bool(xlink_href)
            
            advice_text = 'Add @xlink:href attribute to <ext-link> with text "{text}"'
            advice_params = {
                "text": text,
            }
            
            parent = {
                "parent": ext_link.get("parent"),
                "parent_id": ext_link.get("parent_id"),
                "parent_article_type": ext_link.get("parent_article_type"),
                "parent_lang": ext_link.get("parent_lang"),
            }
            
            yield build_response(
                title="@xlink:href attribute",
                parent=parent,
                item="ext-link",
                sub_item="@xlink:href",
                validation_type="exist",
                is_valid=is_valid,
                expected="@xlink:href attribute present",
                obtained=xlink_href,
                advice=f'Add @xlink:href attribute to <ext-link> with text "{text}"',
                data=ext_link,
                error_level=error_level,
                advice_text=advice_text,
                advice_params=advice_params,
            )
    
    def validate_xlink_href_format(self, error_level=None):
        """
        Validate @xlink:href URL format (ERROR).
        
        SPS Rule: @xlink:href must be a complete URL starting with http:// or https://
        
        Parameters
        ----------
        error_level : str, optional
            Override default error level (default: "ERROR")
        
        Yields
        ------
        dict
            Validation result for each ext-link with xlink:href
        """
        error_level = error_level or self.params.get("xlink_href_format_error_level", "ERROR")
        
        for ext_link in self.ext_links_model.ext_links:
            xlink_href = ext_link.get("xlink_href")
            
            # Skip if xlink:href is not present (handled by another validation)
            if not xlink_href:
                continue
            
            # Check if URL starts with http:// or https://
            is_valid = bool(re.match(r'^https?://', xlink_href, re.IGNORECASE))
            
            advice_text = 'URL in @xlink:href="{xlink_href}" must start with http:// or https://'
            advice_params = {
                "xlink_href": xlink_href,
            }
            
            parent = {
                "parent": ext_link.get("parent"),
                "parent_id": ext_link.get("parent_id"),
                "parent_article_type": ext_link.get("parent_article_type"),
                "parent_lang": ext_link.get("parent_lang"),
            }
            
            yield build_response(
                title="@xlink:href URL format",
                parent=parent,
                item="ext-link",
                sub_item="@xlink:href",
                validation_type="format",
                is_valid=is_valid,
                expected="URL starting with http:// or https://",
                obtained=xlink_href,
                advice=f'URL in @xlink:href="{xlink_href}" must start with http:// or https://',
                data=ext_link,
                error_level=error_level,
                advice_text=advice_text,
                advice_params=advice_params,
            )
    
    def validate_ext_link_type_value(self, error_level=None):
        """
        Validate @ext-link-type value is in allowed list (ERROR).
        
        SPS Rule: @ext-link-type must be one of: uri, doi, pmid, pmcid, clinical-trial
        
        Parameters
        ----------
        error_level : str, optional
            Override default error level (default: "ERROR")
        
        Yields
        ------
        dict
            Validation result for each ext-link with ext-link-type
        """
        error_level = error_level or self.params.get("ext_link_type_value_error_level", "ERROR")
        
        for ext_link in self.ext_links_model.ext_links:
            ext_link_type = ext_link.get("ext_link_type")
            
            # Skip if ext-link-type is not present (handled by another validation)
            if not ext_link_type:
                continue
            
            is_valid = ext_link_type in self.ALLOWED_EXT_LINK_TYPES
            
            advice_text = 'Replace @ext-link-type="{ext_link_type}" with one of: {allowed_values}'
            advice_params = {
                "ext_link_type": ext_link_type,
                "allowed_values": ", ".join(self.ALLOWED_EXT_LINK_TYPES),
            }
            
            parent = {
                "parent": ext_link.get("parent"),
                "parent_id": ext_link.get("parent_id"),
                "parent_article_type": ext_link.get("parent_article_type"),
                "parent_lang": ext_link.get("parent_lang"),
            }
            
            yield build_response(
                title="@ext-link-type value",
                parent=parent,
                item="ext-link",
                sub_item="@ext-link-type",
                validation_type="value in list",
                is_valid=is_valid,
                expected=", ".join(self.ALLOWED_EXT_LINK_TYPES),
                obtained=ext_link_type,
                advice=f'Replace @ext-link-type="{ext_link_type}" with one of: {", ".join(self.ALLOWED_EXT_LINK_TYPES)}',
                data=ext_link,
                error_level=error_level,
                advice_text=advice_text,
                advice_params=advice_params,
            )
    
    def validate_descriptive_text(self, error_level=None):
        """
        Validate link text is descriptive, not generic (WARNING).
        
        SPS Rule: Text should not be generic phrases like "click here", "read more", etc.
        Validation is case-insensitive.
        
        Parameters
        ----------
        error_level : str, optional
            Override default error level (default: "WARNING")
        
        Yields
        ------
        dict
            Validation result for each ext-link with text
        """
        error_level = error_level or self.params.get("descriptive_text_error_level", "WARNING")
        
        for ext_link in self.ext_links_model.ext_links:
            text = ext_link.get("text", "").strip()
            
            # Skip if text is empty (no validation needed)
            if not text:
                continue
            
            # Check if text is generic (case-insensitive)
            text_lower = text.lower()
            is_generic = any(phrase in text_lower for phrase in self.GENERIC_PHRASES)
            is_valid = not is_generic
            
            # Only yield if text is generic
            if is_generic:
                advice_text = 'Replace generic text "{text}" in <ext-link> with descriptive text, or add @xlink:title attribute'
                advice_params = {
                    "text": text,
                }
                
                parent = {
                    "parent": ext_link.get("parent"),
                    "parent_id": ext_link.get("parent_id"),
                    "parent_article_type": ext_link.get("parent_article_type"),
                    "parent_lang": ext_link.get("parent_lang"),
                }
                
                yield build_response(
                    title="descriptive link text",
                    parent=parent,
                    item="ext-link",
                    sub_item="text()",
                    validation_type="value",
                    is_valid=is_valid,
                    expected="descriptive text (not generic)",
                    obtained=text,
                    advice=f'Replace generic text "{text}" in <ext-link> with descriptive text, or add @xlink:title attribute',
                    data=ext_link,
                    error_level=error_level,
                    advice_text=advice_text,
                    advice_params=advice_params,
                )
    
    def validate_xlink_title_when_generic(self, error_level=None):
        """
        Validate @xlink:title presence when text is generic or URL (WARNING).
        
        SPS Rule: When text is generic or is the URL itself, @xlink:title should
        be present with a description of the link destination.
        
        Parameters
        ----------
        error_level : str, optional
            Override default error level (default: "WARNING")
        
        Yields
        ------
        dict
            Validation result for ext-links with generic/URL text
        """
        error_level = error_level or self.params.get("xlink_title_error_level", "WARNING")
        
        for ext_link in self.ext_links_model.ext_links:
            text = ext_link.get("text", "").strip()
            xlink_href = ext_link.get("xlink_href", "")
            xlink_title = ext_link.get("xlink_title")
            
            # Skip if text is empty
            if not text:
                continue
            
            # Check if text is generic
            text_lower = text.lower()
            is_generic = any(phrase in text_lower for phrase in self.GENERIC_PHRASES)
            
            # Check if text is the URL itself (or similar)
            is_url_text = xlink_href and (text in xlink_href or xlink_href in text)
            
            # Only check if text is generic or is URL
            if not (is_generic or is_url_text):
                continue
            
            is_valid = bool(xlink_title)
            
            # Only yield if xlink:title is missing
            if not is_valid:
                reason = "generic" if is_generic else "URL"
                advice_text = 'Add @xlink:title attribute to <ext-link> with {reason} text "{text}" to describe link destination'
                advice_params = {
                    "reason": reason,
                    "text": text,
                }
                
                parent = {
                    "parent": ext_link.get("parent"),
                    "parent_id": ext_link.get("parent_id"),
                    "parent_article_type": ext_link.get("parent_article_type"),
                    "parent_lang": ext_link.get("parent_lang"),
                }
                
                yield build_response(
                    title="@xlink:title for generic/URL text",
                    parent=parent,
                    item="ext-link",
                    sub_item="@xlink:title",
                    validation_type="exist",
                    is_valid=is_valid,
                    expected="@xlink:title attribute when text is generic or URL",
                    obtained=xlink_title,
                    advice=f'Add @xlink:title attribute to <ext-link> with {reason} text "{text}" to describe link destination',
                    data=ext_link,
                    error_level=error_level,
                    advice_text=advice_text,
                    advice_params=advice_params,
                )
