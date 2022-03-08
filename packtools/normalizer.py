def extract_number_and_supplment_from_issue_element(issue):
    """
    Extrai do conteúdo de <issue>xxxx</issue>, os valores number e suppl.
    Valores possíveis
    5 (suppl), 5 Suppl, 5 Suppl 1, 5 spe, 5 suppl, 5 suppl 1, 5 suppl. 1,
    25 Suppl 1, 2-5 suppl 1, 2spe, Spe, Supl. 1, Suppl, Suppl 12,
    s2, spe, spe 1, spe pr, spe2, spe.2, spepr, supp 1, supp5 1, suppl,
    suppl 1, suppl 5 pr, suppl 12, suppl 1-2, suppl. 1
    """
    if not issue:
        return None, None
    issue = issue.strip().replace(".", "")
    splitted = [s for s in issue.split() if s]

    splitted = ["spe"
                if "spe" in s.lower() and s.isalpha() else s
                for s in splitted
                ]
    if len(splitted) == 1:
        issue = splitted[0]
        if issue.isdigit():
            return issue, None
        if "sup" in issue.lower():
            # match como sup*
            return None, "0"
        if issue.startswith("s"):
            if issue[1:].isdigit():
                return None, issue[1:]
        # match com spe, 2-5, 3B
        return issue, None

    if len(splitted) == 2:
        if "sup" in splitted[0].lower():
            return None, splitted[1]
        if "sup" in splitted[1].lower():
            return splitted[0], "0"
        # match spe 4 -> spe4
        return "".join(splitted), None

    if len(splitted) == 3:
        if "sup" in splitted[1].lower():
            return splitted[0], splitted[2]
    # match ????
    return "".join(splitted), None