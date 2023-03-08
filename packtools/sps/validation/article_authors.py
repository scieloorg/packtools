from packtools.sps.models.article_authors import Authors


class ArticleAuthorsValidation:
    def __init__(self, xmltree):
        self._xmltree = xmltree
        self.article_authors = Authors(self._xmltree)

    def validate_authors_role(self, content_type_url):
        _result_dict = {'errors': [], 'warnings': [],
                   'invalid_role': [], 'invalid_content_type': []}
        count = 0
        
        for author in self.article_authors.contribs:
            _author_name = f"{author['given_names']} {author['surname']}"
            
            # Verifica se há alguma tag <role> atribuida ao autor.
            if 'role' not in author:
                _result_dict['errors'].append(
                    f"The author '{_author_name}' has no <role> tag assigned to him")
            elif 'role' in author:
                
                # Percorre todas as role atribuida ao autor.
                for role in author['role']:
                    # Verifica se há tag <role> está vazia.
                    if not role['text']:
                        _result_dict['errors'].append(
                            f"The author '{_author_name}' has an <role> tag empty assigned to him")
                    
                    # Verifica se há texto na tag <role> e nenhuma url em content-type.
                    if role['text'] and not role['content-type']:
                        _result_dict['warnings'].append(
                            f"The author '{_author_name}' has no content-type assign to <role>{role['text']}</role>")
                    
                    # Verifica se há texto na tag <role> e url em content-type.
                    if role['text'] and role['content-type']:
                        _role = role['text']
                        _content_type = role['content-type']
                        expected_role, expected_content_type = content_type_url[count]
                        
                        # Verifica se o par 'role' e 'content type' está presente na lista fornecida.
                        # Caso contrário, identifica qual dos dois está incorreto e informa qual é o esperado e recebido.
                        # Supõe-se que a lista 'content_type_url' está ordenada de acordo com o XML.
                        if (_role, _content_type) != content_type_url[count]:
                            if str(_role).lower() != str(expected_role).lower():
                                _result_dict['invalid_role'].append(
                                    f"Author: {_author_name} - Received: {_role}, Expected: {expected_role}")

                            if str(_content_type).lower() != str(expected_content_type).lower():
                                _result_dict['invalid_content_type'].append(
                                    f"Author: {_author_name} - Received: {_content_type}, Expected: {expected_content_type}")
                    count += 1
        return _result_dict
