#coding:utf-8
import os
import zipfile

from lxml import etree

from packtools import utils


class XMLPacker(object):
    """Adapter that puts all XML pieces together to make a SPS Package.

    :param file: the XML filepath.
    """
    def __init__(self, file):
        self.abs_filepath = os.path.abspath(os.path.expanduser(file))
        self.abs_basepath = os.path.dirname(self.abs_filepath)
        self.filename = os.path.basename(self.abs_filepath)

        try:
            self.xml = utils.XML(self.abs_filepath, load_dtd=False)
        except IOError:
            raise ValueError('Could not load file')

    @property
    def assets(self):
        """Lists all static assets referenced by the XML.
        """
        return utils.get_static_assets(self.xml)

    def check_assets(self):
        """Checks if all related assets are available.
        """
        is_available = utils.make_file_checker(self.abs_basepath)
        return all([is_available(asset) for asset in self.assets])

    def pack(self, file, force=False):
        """Generates a SPS Package.

        :param file: the filename of the output package.
        :param force: force overwrite if the file already exists.
        """
        if self.check_assets() == False:
            raise ValueError('There are missing assets')

        if not file.endswith('.zip'):
            file += '.zip'

        if os.path.exists(file) and force == False:
            raise ValueError('File already exists')

        with zipfile.ZipFile(file, 'w') as zpack:
            # write the XML file
            zpack.write(self.abs_filepath, self.filename)

            # write the PDF file, when available
            abs_pdffile = self.abs_filepath.replace('.xml', '.pdf')
            if os.path.exists(abs_pdffile):
                zpack.write(abs_pdffile, os.path.basename(abs_pdffile))

            # write its assets
            for asset in self.assets:
                abs_path_asset = os.path.join(self.abs_basepath, asset)
                zpack.write(abs_path_asset, asset)


def main():
    """
    Creates a SciELO PS package based on a given XML file.
    """
    import argparse
    import pkg_resources

    packtools_version = pkg_resources.get_distribution('packtools').version


    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('XML', nargs='+',
                        help='Filesystem path to the XML file.')
    parser.add_argument('--version', action='version', version=packtools_version)

    args = parser.parse_args()

    for xml in args.XML:
        try:
            packer = XMLPacker(xml)
        except IOError:
            print 'Error reading %s. Make sure it is a valid file-path.' % xml
        except etree.XMLSyntaxError as e:
            print 'Error reading %s. Syntax error: %s' % (xml, e.message)
        else:
            outfile = packer.abs_filepath.replace('.xml', '.zip')
            try:
                packer.pack(outfile)
            except ValueError as e:
                print 'Error:', e.message
            else:
                print 'Created:', outfile


if __name__ == '__main__':
    main()

