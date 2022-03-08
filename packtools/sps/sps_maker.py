from packtools.sps.models import packages, sps_package
from packtools.sps.libs import async_download, reqs
from packtools import file_utils
from packtools.sps import exceptions


FILE_PATHS_REQUIRED_KEYS = ['xml', 'assets', 'renditions']


def get_names_and_packages(path):
    return packages.explore_source(path)


def make_package_from_paths(paths, zip_folder=None):
    _check_keys_and_files(paths)

    package_metadata = {}
    xml_sps = _get_xml_sps_from_path(paths['xml'])

    package_metadata['xml'] = _get_xml_uri_and_name(xml_sps, paths['xml'])
    package_metadata['renditions'] = paths['renditions']
    package_metadata['assets'] = paths['assets']

    zip_filename = _get_zip_filename(xml_sps)
    package_metadata['temp-zipfile'] = _zip_files_from_paths(zip_filename, xml_sps, paths, zip_folder)

    return package_metadata


def make_package_from_uris(xml_uri, renditions_uris_and_names=[], zip_folder=None):
    package_metadata = {}

    try:
        sps_package = _get_xml_sps_from_uri(xml_uri)
    except exceptions.SPSDownloadXMLError:
        raise

    # guarda uri e nome de renditions em dicionário package
    package_metadata['renditions'] = renditions_uris_and_names

    # extra uri e nome de todos os assets registrados no XML
    package_metadata['assets'] = _get_assets_uris_and_names(sps_package)

    # extrai uri e nome do xml
    package_metadata['xml'] = _get_xml_uri_and_name(sps_package, xml_uri)

    # reúne todos os uris e nomes associados ao XML
    uris_and_names = [package_metadata['xml']] + package_metadata['assets'] + package_metadata['renditions']

    zip_filename = _get_zip_filename(sps_package)

    # cria um arquivo ZIP temporário com os arquivos das uris baixados
    package_metadata['temp-zipfile'] = _zip_files_from_uris_and_names(zip_filename, uris_and_names, zip_folder)

    return package_metadata


def _get_xml_sps_from_uri(xml_uri):
    if xml_uri == '':
        raise exceptions.SPSXMLLinkError('XML URI is empty. Please, informe a link address.')

    if 'http' in xml_uri:
        try:
            content = reqs.requests_get_content(xml_uri)
        except exceptions.SPSHTTPError as e:
            raise exceptions.SPSDownloadXMLError(f'It was not possible to download the XML file {xml_uri}. Status code {e}')

        try:
            return sps_package.SPS_Package(content)
        except:
            raise

    else:
        raise exceptions.SPSXMLLinkError(f'{xml_uri} is not a valid link. Please, inform a link address (e.g. http://...')


def _get_xml_sps_from_path(xml_path):
    if file_utils.is_valid_file(xml_path):
        with open(xml_path) as fin:
            content = fin.read()

            if content:
                return sps_package.SPS_Package(content)
            else:
                raise exceptions.SPSXMLContentError(f'It was not possible to read {xml_path}. Please, provide a valid XML path.')
    else:
        raise exceptions.SPSXMLFileError(f'{xml_path} is invalid. Please, provide a valid XML path.')


def _get_assets_uris_and_names(xml_sps):
    uris_and_filenames = []

    for asset in xml_sps.assets.items:
        uris_and_filenames.append({
            "uri": asset.uri or asset.xlink_href,
            "name": asset.get_name(xml_sps.package_name),
        })

    return uris_and_filenames


def _get_xml_uri_and_name(xml_sps, xml_uri=None):
    return {
        'name': f"{xml_sps.package_name}.xml",
        "uri": xml_uri
    }


def _get_zip_filename(xml_sps, output_filename=None):
    """
    Obtém o nome canônico de um arquivo ZIP a partir de `xml_sps: packtools.sps.models.sps_package.SPS_Package`.

    Parameters
    ----------
    xml_sps : packtools.sps.models.sps_package.SPS_Package
    output_filename: nome do arquivo zip

    Returns
    -------
    str
        "1414-431X-bjmbr-54-10-e11439.zip"

    """
    if not output_filename:
        return f'{xml_sps.package_name}.zip'
    else:
        return output_filename


def _zip_files_from_uris_and_names(zip_name, uris_and_names, zip_folder=None):
    uris_and_names = _remove_invalid_uris(uris_and_names)
    downloaded_files = async_download.download_files(uris_and_names)
    return file_utils.create_zip_file(downloaded_files, zip_name, zip_folder)


def _remove_invalid_uris(uris_and_names):
    """
    Remove as URIs inválidas, isto é, que não inicializam com o termo http.

    Parameters
    ----------
    uris_and_names : list
        Uma lista contendo dicionários do tipo {"uri": str, "name": str}.

    Returns
    -------
    list
        Uma lista contendo dicionários, porém, sem os registros de URIs consideradas inválidas

    """
    return [
        item
        for item in uris_and_names
        if item["uri"].startswith("http")
    ]


def _zip_files_from_paths(zip_name, xml_sps, paths, zip_folder=None):
    renamed_paths = _get_canonical_files_paths(xml_sps, paths)
    return file_utils.create_zip_file(renamed_paths, zip_name, zip_folder)


def _check_keys_and_files(paths: dict):
    """
    Verifica se todos as chaves esperadas do dicionário de caminhos foram informadas.
    São esperadas as chaves presentes em `FILE_PATHS_REQUIRED_KEYS`.
    Verifica se os arquivos informados existem.

    Parameters
    ----------
    paths : dict
        {
            "xml": "/home/user/fd89fb6a2a0f973016f2de7ee2b64b51ca573999.xml",
            "renditions": [
                "/home/user/aed92928a9b5e04e17fa5777d83e8430b9f98f6d.pdf",
                ...
            ],
            "assets": [
                "/home/user/fd89fb6a2a0f973016f2de7ee2b64b51ca573999.jpg",
                ...,
            ]
        }

    Returns
    -------
    boolean
    """
    for k in FILE_PATHS_REQUIRED_KEYS:
        if k not in paths.keys():
            raise exceptions.SPSMakePackageFromPathsMissingKeyError(f'Paths error: key {k} is missing.')

        if k != 'xml':
            for f in paths[k]:
                if not file_utils.is_valid_file(f):
                    raise exceptions.SPSAssetOrRenditionFileError(f'Invalid asset or rendition path: {f}')
        else:
            if not file_utils.is_valid_file(paths[k]):
                raise exceptions.SPSXMLFileError(f'Invalid XML path or content: {paths[k]}')

    return True


def _get_canonical_files_paths(xml_sps, paths):
    """
    Obtém nome canônico dos caminhos dos arquivos que comporão o pacote zip.

    Parameters
    ----------
    xml_sps : packtools.sps.models.sps_package.SPS_Package
    paths: dict
        Dicionário de caminhos no formato
            {
                "xml": "/home/user/fd89fb6a2a0f973016f2de7ee2b64b51ca573999.xml",
                "renditions": [
                    ...
                ],
                "assets": [
                    "/home/user/fd89fb6a2a0f973016f2de7ee2b64b51ca573999.jpg",
                    ...,
                ]
            }

    Returns
    -------
    list
        [
            "/home/user/1414-431X-bjmbr-54-10-e11439.xml",
            "/home/user/1414-431X-bjmbr-54-10-e11439-gf01.jpg",
                ...,
        ]
    """
    new_paths = []

    for k in FILE_PATHS_REQUIRED_KEYS:
        if k == 'xml':
            target = _get_xml_uri_and_name(xml_sps)['name']
            new_paths.append(file_utils.copy_file(paths[k], target))

        elif k == 'renditions':
            # Is not possible to discover the correct rendition name
            new_paths.extend(paths[k])

        elif k == 'assets':
            for v in paths[k]:
                # We use the information inside sps_package.assets.items to discover each asset's name
                target = sps_package.discover_asset_name(xml_sps, v)
                new_paths.append(file_utils.copy_file(v, target))

    return new_paths
