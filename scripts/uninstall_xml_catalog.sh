#!/bin/bash
#
# Unregister the local xmlcatalog from the supercatalog
#
ROOTCATALOG=/etc/xml/catalog

if [ -w $ROOTCATALOG ]
then
    xmlcatalog --noout --del \
        "-//NLM//DTD JATS" $ROOTCATALOG
    xmlcatalog --noout --del \
        "-//NLM//DTD Journal" $ROOTCATALOG
    xmlcatalog --noout --del \
        "JATS-journalpublishing1.dtd" $ROOTCATALOG
    xmlcatalog --noout --del \
        "journalpublishing3.dtd" $ROOTCATALOG
fi

