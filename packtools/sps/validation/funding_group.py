from packtools.sps.models.funding_group import FundingGroup


def equalize_list_sizes(list1, list2):
    len1, len2 = len(list1), len(list2)
    if len1 < len2:
        list1.extend([None] * (len2 - len1))
    elif len2 < len1:
        list2.extend([None] * (len1 - len2))
    return list1, list2


