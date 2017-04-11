#coding: utf-8
from __future__ import unicode_literals
import logging
import itertools
import json

import plumber

from .style_errors import StyleError
from . import catalogs


LOGGER = logging.getLogger(__name__)


with open(catalogs.ISO3166_CODES) as f:
    ISO3166_CODES_SET = set(json.load(f))


# --------------------------------
# Basic functionality
# --------------------------------
@plumber.filter
def setup(message):
    """Prepare the message to traverse the pipeline.

    The input `message` is an `etree` instance. The pipeline will inspect
    this etree and append the errors on an errors list. This errors list
    is instantiated at this setup pipe.
    """
    return message, []


@plumber.filter
def teardown(message):
    """Finalize the processing pipeline and return the errors list.
    """
    _, err_list = message
    return err_list


def StyleCheckingPipeline():
    """Factory for style checking pipelines.
    """
    return plumber.Pipeline(setup, funding_group, doctype, country_code, teardown)


# --------------------------------
# Funding Group check
# --------------------------------
@plumber.filter
def funding_group(message):
    """Validate the Funding Group element

    Ref. URI:
      - http://jats.nlm.nih.gov/publishing/tag-library/1.1d1/n-pdx0.html
      - http://ref.scielo.org/g388x3

    Element may be found in:
      - /article/front/article-meta/funding_group
    """
    et, err_list = message

    funding_groups = et.findall('front//funding-group//award-id')
    financial_disclosures = et.findall(
            'back//fn[@fn-type="financial-disclosure"]')
    has_funding_group = bool(all([bool(elem.text)
                                  for elem in funding_groups]))
    has_financial_disclosure = bool(financial_disclosures)

    if has_financial_disclosure and not has_funding_group or (
            len(financial_disclosures) > len(funding_groups)):
        err = StyleError()
        err.message = "Element 'fn-group': This element has occurrences not declared in funding-group."
        err_list.append(err)

    if has_funding_group:
        def get_text(elem):
            """Always returns a text string.
            """
            try:
                return u''.join(elem.itertext())
            except:
                return u''

        # only the main document is relevant
        award_ids = [elem.text for elem in et.findall(
            'front//funding-group/award-group/award-id')
            if elem.text is not None]
        fn_occs = [get_text(elem) for elem in et.findall(
            'back//fn[@fn-type="financial-disclosure"]/p')]
        ack_occs = [get_text(elem) for elem in et.findall(
            'back//ack/p')]

        def in_there(award_id, texts):
            for text in texts:
                if award_id in text:
                    return True
                else:
                    LOGGER.info('cannot find award-id "%s" in text', award_id)

            return False

        LOGGER.info('declared contract numbers: %s', award_ids)

        missing_award_ids = set(award_ids)
        paragraphs = [p for p in itertools.chain(fn_occs, ack_occs) if p]

        for award_id in award_ids:
            if in_there(award_id, paragraphs):
                try:
                    missing_award_ids.remove(award_id)
                except KeyError:
                    LOGGER.info('many occurences of award-id: "%s"',
                                award_id)
            else:
                LOGGER.info('cannot find contract number "%s" in set "%s"',
                        award_id, award_ids)

        if missing_award_ids:
            LOGGER.info('missing award-id: "%s"', missing_award_ids)
            err = StyleError()
            err.message = "Element 'funding-group': This element has occurrences not declared in fn or ack."
            err_list.append(err)
    else:
        LOGGER.info('no contract numbers found in %s', et)

    return message


@plumber.filter
def doctype(message):
    """Make sure the DOCTYPE declaration is present.
    """
    et, err_list = message

    if not et.docinfo.doctype:
        err = StyleError()
        err.message = "Missing DOCTYPE declaration."
        err_list.append(err)

    return message


@plumber.filter
def country_code(message):
    """Check country codes against iso3166 alpha-2 list.
    """
    et, err_list = message

    elements = et.findall('//*[@country]')
    for elem in elements:
        value = elem.attrib['country']
        if value not in ISO3166_CODES_SET:
            err = StyleError()
            err.line = elem.sourceline
            err.message = "Element '%s', attribute country: Invalid country code \"%s\"." % (elem.tag, value)
            err_list.append(err)

    return message

