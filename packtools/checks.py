#coding: utf-8
from __future__ import unicode_literals
import re
import logging
import itertools
from datetime import datetime

import plumber

from .style_errors import StyleError


logger = logging.getLogger(__name__)


# --------------------------------
# Basic functionality
# --------------------------------
@plumber.pipe
def setup(message):
    """Prepare the message to traverse the pipeline.

    The input `message` is an `etree` instance. The pipeline will inspect
    this etree and append the errors on an errors list. This errors list
    is instantiated at this setup pipe.
    """
    return message, []


@plumber.pipe
def teardown(message):
    """Finalize the processing pipeline and return the errors list.
    """
    et, err_list = message
    return err_list


def StyleCheckingPipeline():
    """Factory for style checking pipelines.
    """
    return plumber.Pipeline(setup, funding_group, doctype, teardown)


# --------------------------------
# Funding Group check
# --------------------------------
@plumber.pipe
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

    logger.info('here: %s', datetime.now())

    if has_funding_group:
        def get_text(elem):
            return ''.join(elem.itertext())

        # only the main document is relevant
        award_ids = [elem.text for elem in et.findall(
            'front//funding-group/award-group/award-id')
            if elem.text is not None]
        fn_occs = [get_text(elem) for elem in et.findall(
            'back//fn[@fn-type="financial-disclosure"]/p')
            if elem.text is not None]
        ack_occs = [get_text(elem) for elem in et.findall(
            'back//ack/p')
            if elem.text is not None]

        def in_there(award_id, texts):
            for text in texts:
                if award_id in text:
                    return True
                else:
                    logger.debug('Cannot find "%s" in "%s".', award_id, text)

            return False

        logger.info('Declared contract numbers: %s', award_ids)

        missing_award_ids = set(award_ids)
        for award_id in award_ids:
            if in_there(award_id, itertools.chain(fn_occs, ack_occs)):
                try:
                    missing_award_ids.remove(award_id)
                except KeyError:
                    logger.info('The award-id %s is mentioned more than once.',
                                award_id)
            else:
                logger.info('Cannot find contract number "%s" in the set "%s".',
                        award_id, award_ids)

        if missing_award_ids:
            logger.debug('Missing award-id: %s.', missing_award_ids)
            err = StyleError()
            err.message = "Element 'funding-group': This element has occurrences not declared in fn or ack."
            err_list.append(err)
    else:
        logger.debug('No contract numbers found in %s.' % et)

    return message


@plumber.pipe
def doctype(message):
    """Make sure the DOCTYPE declaration is present.
    """
    et, err_list = message

    if not et.docinfo.doctype:
        err = StyleError()
        err.message = "Missing DOCTYPE declaration."
        err_list.append(err)

    return message

