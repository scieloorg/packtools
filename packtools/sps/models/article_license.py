import re
from urllib.parse import urlparse

from packtools.sps.utils import xml_utils
from packtools.sps.models.article_and_subarticles import Fulltext


"""
<article-meta>
    <permissions>
        <license license-type="open-access"
                 xlink:href="http://creativecommons.org/licenses/by/4.0/"
                 xml:lang="en">
            <license-p>This is an article published in open access under a Creative Commons license.</license-p>
        </license>
        <license license-type="open-access"
                 xlink:href="http://creativecommons.org/licenses/by/4.0/"
                 xml:lang="pt">
            <license-p>Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.</license-p>
        </license>
        <license license-type="open-access"
                 xlink:href="http://creativecommons.org/licenses/by/4.0/"
                 xml:lang="es">
            <license-p>Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.</license-p>
        </license>
    </permissions>
</article-meta>
"""


class ArticleLicense:
    def __init__(self,
                 xmltree,
                 tags_to_keep=None,
                 tags_to_keep_with_content=None,
                 tags_to_remove_with_content=None,
                 tags_to_convert_to_html=None
                 ):
        self.xmltree = xmltree
        self.tags_to_keep = tags_to_keep
        self.tags_to_keep_with_content = tags_to_keep_with_content
        self.tags_to_remove_with_content = tags_to_remove_with_content
        self.tags_to_convert_to_html = tags_to_convert_to_html
        self._fulltext = Fulltext(xmltree.find("."))

    @property
    def licenses(self):
        for license_node in self.xmltree.xpath('./front//permissions//license'):
            license = License(
                license_node,
                tags_to_keep=self.tags_to_keep,
                tags_to_keep_with_content=self.tags_to_keep_with_content,
                tags_to_remove_with_content=self.tags_to_remove_with_content,
                tags_to_convert_to_html=self.tags_to_convert_to_html
            )
            response = license.data
            response.update(self._fulltext.attribs_parent_prefixed)
            yield response

    @property
    def licenses_by_lang(self):
        return {
            item['lang']: item
            for item in self.licenses
        }


class License:
    """
    Represents a single license node from the XML.
    
    Parameters:
    -----------
    license_node : ElementTree.Element
        The XML node representing the license
    tags_to_keep : list, optional
        List of tags to keep in the HTML output
    tags_to_keep_with_content : list, optional
        List of tags to keep with their content in the HTML output
    tags_to_remove_with_content : list, optional
        List of tags to remove along with their content
    tags_to_convert_to_html : list, optional
        List of tags to convert to HTML format
    """
    
    def __init__(
        self,
        license_node,
        tags_to_keep=None,
        tags_to_keep_with_content=None,
        tags_to_remove_with_content=None,
        tags_to_convert_to_html=None
    ):
        self._node = license_node
        self._license_p = self._node.find('license-p')
        self._tags_to_keep = tags_to_keep
        self._tags_to_keep_with_content = tags_to_keep_with_content
        self._tags_to_remove_with_content = tags_to_remove_with_content
        self._tags_to_convert_to_html = tags_to_convert_to_html
    
    @property
    def type(self):
        """Get the license type"""
        return self._node.get('license-type', '')
    
    @property
    def lang(self):
        """Get the language of the license"""
        return self._node.get('{http://www.w3.org/XML/1998/namespace}lang', '')
    
    @property
    def link(self):
        """Get the license URL"""
        return self._node.get('{http://www.w3.org/1999/xlink}href', '')
    
    @property
    def code(self):
        """
        Get the Creative Commons license code from the URL, without version.
        Examples:
            - http://creativecommons.org/licenses/by/4.0/ -> 'by'
            - http://creativecommons.org/licenses/by-nc-sa/4.0/ -> 'by-nc-sa'
            - https://creativecommons.org/licenses/by-nc/3.0/ -> 'by-nc'
        
        Returns:
        --------
        str
            The CC license code or empty string if not a valid CC license URL
        """
        if not self.link:
            return ''
            
        # Parse the URL
        parsed_url = urlparse(self.link)
        
        # Check if it's a Creative Commons URL
        if not any(domain in parsed_url.netloc 
                  for domain in ['creativecommons.org', 'www.creativecommons.org']):
            return ''
            
        # Extract the path parts
        path_parts = parsed_url.path.strip('/').split('/')
        
        # Look for the license code part (typically after 'licenses/')
        try:
            licenses_index = path_parts.index('licenses')
            if len(path_parts) > licenses_index + 1:
                # Get the code part and remove any version number
                code_part = path_parts[licenses_index + 1]
                # Remove version number if present (e.g., '4.0' from 'by-nc-4.0')
                code = re.sub(r'-?\d+\.?\d*$', '', code_part)
                return code
        except ValueError:
            pass
            
        return ''
    
    @property
    def license_p_plain_text(self):
        """Get the license text without any markup"""
        if self._license_p is not None:
            return xml_utils.node_plain_text(self._license_p)
        return ''
    
    @property
    def license_p_text(self):
        """Get the license text without xref tags"""
        if self._license_p is not None:
            return xml_utils.node_text_without_fn_xref(self._license_p)
        return ''
    
    @property
    def license_p_html_text(self):
        """Get the license text with HTML formatting"""
        if self._license_p is not None:
            return xml_utils.process_subtags(
                self._license_p,
                tags_to_keep=self._tags_to_keep,
                tags_to_keep_with_content=self._tags_to_keep_with_content,
                tags_to_remove_with_content=self._tags_to_remove_with_content,
                tags_to_convert_to_html=self._tags_to_convert_to_html
            )
        return ''
    
    @property
    def data(self):
        """
        Convert the license to a dictionary format
        
        Returns:
        --------
        dict
            Dictionary containing all license information
        """
        return {
            'type': self.type,
            'lang': self.lang,
            'link': self.link,
            'code': self.code,
            'license_p': {
                'plain_text': self.license_p_plain_text,
                'text': self.license_p_text,
                'html_text': self.license_p_html_text
            }
        }


# Example usage
def test_license_code():
    from lxml import etree
    
    # Test cases
    test_cases = [
        """
        <license license-type="open-access" 
                xlink:href="http://creativecommons.org/licenses/by/4.0/"
                xml:lang="en">
            <license-p>Test license</license-p>
        </license>
        """,
        """
        <license license-type="open-access"
                xlink:href="http://creativecommons.org/licenses/by-nc-sa/4.0/"
                xml:lang="en">
            <license-p>Test license</license-p>
        </license>
        """,
        """
        <license license-type="open-access"
                xlink:href="https://creativecommons.org/licenses/by-nc/3.0/"
                xml:lang="en">
            <license-p>Test license</license-p>
        </license>
        """
    ]
    
    for xml in test_cases:
        license_node = etree.fromstring(xml)
        license = License(license_node)
        print(f"URL: {license.link}")
        print(f"Code: {license.code}")
        print("---")



# Example usage
def example_usage():
    from lxml import etree
    
    xml = """
    <article-meta>
        <permissions>
            <license license-type="open-access"
                     xlink:href="http://creativecommons.org/licenses/by/4.0/"
                     xml:lang="en">
                <license-p>This is an article published in open access under a Creative Commons license.</license-p>
            </license>
        </permissions>
    </article-meta>
    """
    
    # Parse XML
    tree = etree.fromstring(xml)
    license_node = tree.find('.//license')
    
    # Create License instance
    license = License(
        license_node,
        tags_to_keep=['p', 'bold'],
        tags_to_keep_with_content=['italic'],
        tags_to_remove_with_content=['sup'],
        tags_to_convert_to_html=['sub']
    )
    
    # Access license properties
    print(f"Language: {license.lang}")
    print(f"Link: {license.link}")
    print(f"Type: {license.type}")
    print(f"Plain text: {license.license_p_plain_text}")
    print(f"Text without xref: {license.license_p_text}")
    print(f"HTML text: {license.license_p_html_text}")
    
    # Get all information as dictionary
    license_dict = license.to_dict()
    print("\nLicense dictionary:", license_dict)


if __name__ == "__main__":
    example_usage()
