"""
data = {
    "aff_id": "aff01", (obrigatório)
    "label": "1",
    "orgname": "Fundação Oswaldo Cruz",
    "orgdiv1": "Escola Nacional de Saúde Pública Sérgio Arouca",
    "orgdiv2": "Centro de Estudos da Saúde do Trabalhador e Ecologia Humana",
    "original": "Prof. da Fundação Oswaldo Cruz",
    "country_code": "BR",
    "country_name": "Brazil",
    "city": "Manguinhos",
    "state": "RJ",
    "email": "maurosilva@foo.com"
}
"""

from lxml import etree as ET


def build_aff(data):
    aff_id = data.get("aff_id")
    if aff_id:
        aff_elem = ET.Element("aff", attrib={"id": aff_id})
        for content_type in ("orgname", "orgdiv1", "orgdiv2", "original"):
            instituion_text = data.get(content_type)
            if instituion_text:
                instituion_elem = ET.Element("institution", attrib={"content-type": content_type})
                instituion_elem.text = instituion_text
                aff_elem.append(instituion_elem)

        label = data.get("label")
        if label:
            label_elem = ET.Element("label")
            label_elem.text = label
            aff_elem.append(label_elem)

        city = data.get("city")
        state = data.get("state")
        if city or state:
            addr_line_elem = ET.Element("addr-line")
            if city:
                city_elem = ET.Element("city")
                city_elem.text = city
                addr_line_elem.append(city_elem)
            if state:
                state_elem = ET.Element("state")
                state_elem.text = state
                addr_line_elem.append(state_elem)
            aff_elem.append(addr_line_elem)

        country_code = data.get("country_code")
        country_name = data.get("country_name")
        if country_code and country_name:
            country_elem = ET.Element("country", attrib={"country": country_code})
            country_elem.text = country_name
            aff_elem.append(country_elem)

        email = data.get("email")
        if email:
            email_elem = ET.Element("email")
            email_elem.text = email
            aff_elem.append(email_elem)

        return aff_elem
