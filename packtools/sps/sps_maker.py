from packtools.sps.models import packages, sps_package
from packtools.sps.libs import async_download, reqs
from packtools.sps.utils import file_utils
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
        content = reqs.requests_get_content(xml_uri)
        
        if not content:
            raise exceptions.SPSDownloadXMLError(f'It was not possible to download the XML file {xml_uri}.')

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
        raise exceptions.SPSXMLFileError(f'{xml_path} is invalid. Please, provide a valid XML path.')

