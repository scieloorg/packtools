#coding: utf-8
import plumber

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
    return plumber.Pipeline(setup, teardown)


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

      - PROPOSITION1: ∀Article[ HasExplicitContract(Article) => HasFundingGroup(Article) ]
      - PROPOSITION2: ∀Article[ PROPOSITION1 => ( ∃S1 ∃S2[ Funds(Article, S1) v Funds(Article, S2) ] ) ]
      - PROPOSITION3: PROPOSITION2 => (
            ∀ContractNo<fn> [ Registered(FundingGroup, ContractNo) ] ^
            ∀ContractNo<ack> [ Registered(FundingGroup, ContractNo) ] ^
            ∀ContractNo<funding-group> [ Registered(Ack, ContractNo) v Registered(Fn, ContractNo) ]
            )
    """
    et, err_list = message
    return message

