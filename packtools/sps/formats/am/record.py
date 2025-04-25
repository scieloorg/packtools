def simple_field(key, value):
    """
    Retorna um dicionário com uma estrutura simples de campo se o valor for fornecido.

    Exemplo:
        >>> simple_field("t", "Título")
        {'t': [{'_': 'Título'}]}

    Parâmetros:
        key (str): A chave a ser usada.
        value (str): O valor a ser inserido.

    Retorna:
        dict: Dicionário formatado se o valor for truthy, caso contrário um dicionário vazio.
    """
    if value:
        return {
                key: [
                    {
                        "_": value
                    }
                ]
            }
    return {}


def multiple_fields(keys, values):
    """
    Cria um dicionário associando chaves e valores, ignorando os valores None.

    Exemplo:
        >>> keys = ("k", "n", "1", "s", "r", "_")
        >>> values = ("0000-0002-6656-8155", "Adriana Valongo", "aff3", "Zani", "ND", "")
        >>> multiple_fields(keys, values)
        {'k': '0000-0002-6656-8155', 'n': 'Adriana Valongo', '1': 'aff3', 's': 'Zani', 'r': 'ND', '_': ''}

    Parâmetros:
        keys (iterable): Sequência de chaves.
        values (iterable): Sequência de valores correspondentes.

    Retorna:
        dict: Dicionário com pares chave/valor, ignorando os valores None.
    """
    d = {}
    for key, value in zip(keys, values):
        if value is not None:
            d[key] = value
    return d

def multiple_fields_list(key, nested_keys, iterator, extractor):
    """
    Gera uma lista de dicionários usando múltiplas chaves e valores extraídos de um iterador.

    Exemplo:
        >>> multiple_fields_list("v10", ("k", "n"), [obj1, obj2], extract_func)
        {'v10': [{'k': '...', 'n': '...'}, {'k': '...', 'n': '...'}]}

    Parâmetros:
        key (str): A chave que encapsulará a lista resultante.
        nested_keys (iterable): Chaves usadas para cada item.
        iterator (iterable): Iterável de onde os dados serão extraídos.
        extractor (callable): Função que extrai os valores de cada item.

    Retorna:
        dict: Dicionário com a chave `key` apontando para a lista de dicionários formatados.
    """
    values = []
    for item in iterator:
        values.append(multiple_fields(nested_keys, extractor(item)))

    return {key: values}