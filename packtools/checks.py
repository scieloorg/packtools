#coding: utf-8
import re
import logging

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
_AWARDID_PATTERN_LIST = (
    # ENSP prefixed
    r'\bENSP[A-Z\d-]+\d\b',
    # FAEPA
    r'\bFAEPA[A-Z\d/-]+\d\b',

    # general purpose award-id matching
    r'\b\d[\d./-]+\d\b',
    )


_AWARDID_FALSE_POSITIVES = (
    # Year in format yyyy
    r'^[12]\d{3}$',
    )


AWARDID_PATTERN = re.compile(r'|'.join(_AWARDID_PATTERN_LIST), flags=re.L)
AWARDID_FALSE_POSITIVES = re.compile(r'|'.join(_AWARDID_FALSE_POSITIVES), flags=re.L)


def _find_contract_numbers(text,
                           pattern=AWARDID_PATTERN,
                           fpos_pattern=AWARDID_FALSE_POSITIVES):
    """Look for patterns that look like contract numbers.

    Assuming many false-positives are matched, `fpos_pattern` accepts a
    compiled regex pattern to fine-tune the result.
    """
    pre_result = pattern.findall(text)
    return [number for number in pre_result if not fpos_pattern.match(number)]


def find_contract_numbers(et):
    """Try to find the contract numbers insinde the elements <fn> and <ack>.

      - The actual text resides on <p> elements of each <fn> or <ack> occurence.
    :param et: an instance of etree.
    """
    fn_occs = et.findall('//fn[@fn-type="financial-disclosure"]/p')
    ack_occs = et.findall('//ack/p')

    found_contracts = {}
    for occ in fn_occs:
        res_element = found_contracts.setdefault('fn', [])
        try:
            res_element += _find_contract_numbers(occ.text)
        except TypeError:
            # skip when occ.text is None
            pass
    for occ in ack_occs:
        res_element = found_contracts.setdefault('ack', [])
        try:
            res_element += _find_contract_numbers(occ.text)
        except TypeError:
            # skip when occ.text is None
            pass

    return found_contracts

@plumber.pipe
def funding_group(message):
    """Validate the Funding Group element

    Ref. URI:
      - http://jats.nlm.nih.gov/publishing/tag-library/1.1d1/n-pdx0.html
      - http://ref.scielo.org/g388x3

    Element may be found in:
      - /article/front/article-meta/funding_group
      - /article/sub-article/front-stub/funding_group

    Spec:
      - HasExplicitContract(x) is True if x has explicit contract numbers in
        <ack> or <fn fn-type="financial-disclosure"> elements.
      - HasFundingGroup(x) is True if x has the <funding-group> element.
      - Funds(x, y) is True if x is funded by y.
      - Registered(x, y) is True if y is in x.
      - FundingGroup is the set of all funding-groups/award-group elements.
      - Ack is the set of all contract-ids in <ack> element.
      - Fn is the set of all contract-ids in <fn fn-type="financial-disclosure">
        element.

      - PROPOSITION1: ∀Article[ HasExplicitContract(Article) <=> HasFundingGroup(Article) ]
      - PROPOSITION2: ∀Article[ PROPOSITION1 => ( ∃S1 ∃S2[ Funds(Article, S1) v Funds(Article, S2) ] ) ]
      - PROPOSITION3: PROPOSITION2 => (
            ∀ContractNo<fn> [ Registered(FundingGroup, ContractNo) ] ^
            ∀ContractNo<ack> [ Registered(FundingGroup, ContractNo) ] ^
            ∀ContractNo<funding-group> [ Registered(Ack, ContractNo) v Registered(Fn, ContractNo) ]
            )
    """
    et, err_list = message

    found_contracts = find_contract_numbers(et)

    has_explicit_contract = bool(found_contracts.get('fn', None) or
                                 found_contracts.get('ack', None))
    has_funding_group = bool(et.findall('//funding-group'))

    if has_explicit_contract != has_funding_group:
        if has_explicit_contract:
            info = 'This element is not filled-in correctly.'
        else:
            info = 'This element is not expected.'

        err = StyleError()
        err.message = "Element 'funding-group': %s" % info
        err_list.append(err)

    elif has_explicit_contract:
        funding_group_ids_set = set(elem.text for elem in et.findall('//funding-group/award-group/award-id'))
        fn_set = set(found_contracts.get('fn', []))
        ack_set = set(found_contracts.get('ack', []))

        if fn_set.issubset(funding_group_ids_set):

            if ack_set.issubset(funding_group_ids_set):

                if funding_group_ids_set != fn_set.union(ack_set):
                    err = StyleError()
                    err.message = "Element 'funding-group': This element has occurrences not declared in fn or ack."
                    err_list.append(err)

            else:
                err = StyleError()
                err.message = "Element 'ack': This element has occurrences not declared in funding-group."
                err_list.append(err)

        else:
            err = StyleError()
            err.message = "Element 'fn-group': This element has occurrences not declared in funding-group."
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

