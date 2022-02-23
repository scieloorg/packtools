import os
import tempfile

import logging
import asyncio

import aiohttp
from tenacity import retry, wait_exponential

LOGGER_FORMAT = u"%(asctime)s %(levelname)-5.5s %(message)s"
logging.basicConfig(format=LOGGER_FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)


@retry(wait=wait_exponential(multiplier=1, min=4, max=20))
async def _get(session, uri):
    """
    Obtém um recurso com acesso HTTP.

    Retentativas: Aguarde 2 ^ x * 1 segundo entre cada nova tentativa,
                  começando com 4 segundos, depois até 10 segundos e 10
                  segundos depois

    Args:
        session: http session object(aiohttp), sessão http
        uri: Endereço para URL contento uma posição de interpolação.
    Retornos:
        Retorno o corpo da resposta HTTP.
    Exceções:
        Trata a exceções de conexão com o endpoint HTTP.
    """
    logger.info("Obtendo recurso com a uri: %s" % uri)

    try:
        async with session.get(uri) as response:
            if response.status != 200:
                logger.error(
                    "Recurso não encontrado '%s'" %
                    uri,
                )
                return None

            return await response.content.read()
    except Exception as e:
        logger.error(
            "Erro ao obter o recurso: %s, retentando...., erro: %s" %
            (uri, e))


async def _download_file(session, uri, download_filename, download_folder):
    """
    """
    content = await _get(session, uri)
    if content:
        download_file_path = os.path.join(download_folder, download_filename)
        with open(download_file_path, "wb") as fp:
            fp.write(content)


async def _bound_download_file(sem, session, uri, download_filename, download_folder):
    """
    Responsável por envolver a função de obter os artigos por um semáforo.

    Args:
        fetcher: callable, função responsável por obter os dados da URL
        session: http session object(aiohttp), sessão http
        sem: semaphore object, um objeto semáforo para envolver a função.
    """

    async with sem:
        await _download_file(session, uri, download_filename, download_folder)


async def _download_files(
    uris_and_names,
    downloads_path,
    ssl=False,
    semaphore_value=20,
):
    """
    """

    tasks = []
    sem = asyncio.Semaphore(semaphore_value)

    try:
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)
        ) as session:

            for uri_and_name in uris_and_names:
                tasks.append(
                    _bound_download_file(
                        sem,
                        session,
                        uri_and_name["uri"],
                        uri_and_name["name"],
                        downloads_path,
                    )
                )

            if tasks:
                logger.info("Qty tasks: %s", len(tasks))
                responses = asyncio.gather(*tasks)
                await responses

    except Exception as e:
        logger.error("Erro: %s.", e)
        logger.exception(e)


def _get_or_create_eventloop():
    """

    """
    # https://techoverflow.net/2020/10/01/how-to-fix-python-asyncio-runtimeerror-there-is-no-current-event-loop-in-thread/
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()


def download_files(uris_and_names, downloads_path=None):
    downloads_path = downloads_path or tempfile.mkdtemp()
    loop = _get_or_create_eventloop()
    loop.run_until_complete(
        _download_files(uris_and_names, downloads_path))
    return [os.path.join(downloads_path, f)
            for f in os.listdir(downloads_path)]
