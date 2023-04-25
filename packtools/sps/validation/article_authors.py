import re

from packtools.sps.models.article_authors import Authors


class ArticleAuthorsValidation:
    def __init__(self, xmltree):
        self._xmltree = xmltree
        self.article_authors = Authors(self._xmltree)

    def validate_authors_role(self, credit_terms_and_urls):
        _result_dict = []

        for author in self.article_authors.contribs:
            _author_name = f"{author['given_names']} {author['surname']}"
            
            # Verifica se há alguma tag <role> atribuida ao autor.
            if 'role' not in author:
                _result_dict.append({
                    'result': 'error', 
                    'error_type': f"No role found", 
                    'message': f"The author {_author_name} does not have a role. Please add a role according to the credit-taxonomy below.",
                    'credit_terms_and_urls': credit_terms_and_urls, 
                })
            else:
                # Percorre todas as role atribuida ao autor.
                for role in author['role']:

                    # Verifica se há role sem texto e sem content-type.
                    if not role['text'] and not role['content-type']:
                        _result_dict.append({
                            'result': 'error',
                            'error_type': f"Text and content-type not found",
                            'message': f"The author {_author_name} has a role with no text and content-type attributes. Please add valid text and content-type attributes according to the credit taxonomy below.",
                            'credit_terms_and_urls': credit_terms_and_urls,
                        })
            
                    # Verifica se há texto na tag role e nenhuma uri em content-type.
                    elif role['text'] and not role['content-type']:
                        _result_dict.append({
                            'result': 'error',
                            'error_type': f"No content-type found",
                            'message': f"The author {_author_name} has a role {role['text']} with text but no content-type attribute. Please add a valid URI to the content-type attribute according to the credit taxonomy below.",
                            'credit_terms_and_urls': credit_terms_and_urls,
                        })
            
                    #Verifica se há content-type em <role> sem texto
                    elif not role['text'] and role['content-type']:
                        _result_dict.append({
                            'result': 'error',
                            'error_type': f"No text found",
                            'message': f"The author {_author_name} has a role with no text. Please add valid text to the role according to the credit taxonomy below.",
                            'credit_terms_and_urls': credit_terms_and_urls,
                        })                           
                    
                    # Verifica se há texto na <role> e url em content-type.
                    elif role['text'] and role['content-type']:
                        _role = role['text']
                        _content_type = role['content-type']
                        
                        # Verifica se o par 'role' e 'content type' está presente na lista fornecida.
                        # Torna case-insensitive
                        if not any(item['term'].lower() == _role.lower() and item['uri'].lower() == _content_type.lower() for item in credit_terms_and_urls):
                           _result_dict.append({
                               'result': 'error',
                               'error_type': f"Role and content-type not found",
                               'message': f"The author {_author_name} has a role and content-type that are not found in the credit taxonomy. Please check the role and content-type attributes according to the credit taxonomy below.",
                               'credit_terms_and_urls': credit_terms_and_urls,
                           })
                        else:
                            _result_dict.append({
                                'result': 'success',
                                'message': f"The author {_author_name} has a valid role and content-type attribute for the role {role['text']}."
                            })
        return _result_dict

    def validate_authors_orcid(self):
        _result_dict = []
        _default_orcid = r'^[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}$'

        for author in self.article_authors.contribs:
            _author_name = f"{author['given_names']} {author['surname']}"

            if 'orcid' not in author:                 
                _result_dict.append({
                    'result': "error",
                    'error_type': "Orcid not found",
                    'message': f"The author {_author_name} does not have an orcid. Please add a valid orcid.",
                    'author': author, 
                })
            else:
                if re.match(_default_orcid, author['orcid']):
                    _result_dict.append({
                        'result': 'success',
                        'message': f"The author {_author_name} has a valid orcid.",
                        'author': author,
                    })
                else:
                    _result_dict.append({
                        'result': 'error',
                        'error_type': "Format invalid",
                        'message': f"The author {_author_name} has an orcid in an invalid format. Please ensure that the ORCID is entered correctly, including the proper format (e.g., 0000-0002-1825-0097).",
                        'author': author,
                    })
        return _result_dict
    

    def validate(self, data):
        """
        Função que executa as validações da classe ArticleAuthorsValidation.

        Returns:
            dict: Um dicionário contendo os resultados das validações realizadas.
        
        """
        credit_terms_and_urls_results = {
            'authors_credit_terms_and_urls_validation': self.validate_authors_role(data['credit_terms_and_urls'])
            }
        orcid_results = {
            'authors_orcid_validation': self.validate_authors_orcid()
            }
        credit_terms_and_urls_results.update(orcid_results)
        return credit_terms_and_urls_results