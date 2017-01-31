#!/bin/bash
#
# Register the local catalog in the super catalog with the appropriate delegates.
#
ROOTCATALOG=/etc/xml/catalog
CATALOG="$(python -c "import sys, packtools; sys.stdout.write(packtools.catalogs.XML_CATALOG)")" 

if [ $? -ne 0 ]
then
    echo "Cannot load packtools lib. Make sure it is installed and on path."
    exit $?
fi

if [ ! -r $ROOTCATALOG ]
then
    xmlcatalog --noout --create $ROOTCATALOG
fi

if [ -w $ROOTCATALOG ]
then
    xmlcatalog --noout --add "delegatePublic" \
        "-//NLM//DTD JATS" \
        "file://$CATALOG" $ROOTCATALOG
    xmlcatalog --noout --add "delegatePublic" \
        "-//NLM//DTD Journal" \
        "file://$CATALOG" $ROOTCATALOG
    xmlcatalog --noout --add "delegateSystem" \
        "JATS-journalpublishing1.dtd" \
        "file://$CATALOG" $ROOTCATALOG
    xmlcatalog --noout --add "delegateSystem" \
        "journalpublishing3.dtd" \
        "file://$CATALOG" $ROOTCATALOG
    xmlcatalog --noout --add "delegateSystem" \
        "http://jats.nlm.nih.gov/publishing" \
        "file://$CATALOG" $ROOTCATALOG
fi

