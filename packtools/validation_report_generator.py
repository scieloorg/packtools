import csv
import argparse
from packtools.sps.utils import xml_utils
from packtools.sps.validation.aff import AffiliationsListValidation
from packtools.sps.validation.article_and_subarticles import ArticleLangValidation
from packtools.sps.validation.article_xref import ArticleXrefValidation


def get_xml_tree(file_to_read):
    with open(file_to_read, 'r') as file:
        return xml_utils.get_xml_tree(file.read())


def validate_xml_tree(xml_tree, validation_params):
    data = AffiliationsListValidation(xml_tree).validate(validation_params)['affiliations_validation']

    validators = [
        ArticleLangValidation(xml_tree),
        ArticleXrefValidation(xml_tree)
    ]

    for validator in validators:
        for key in validator.validate(validation_params):
            for item in validator.validate(validation_params)[key]:
                data.append(item)

    return data


def write_to_csv(data, file_to_write):
    headers = data[0].keys()
    with open(file_to_write, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', dest='file_to_read', required=True, help='XML file path to validate')
    parser.add_argument('-c', dest='country_list', required=False, help='Comma separated list of country codes for validation')
    parser.add_argument('-l', dest='lang_list', required=False, help='Comma separated list of languages for validation')
    parser.add_argument('-w', dest='file_to_write', required=True, help='CSV file path to receive the validation result')
    args = parser.parse_args()

    file_to_read = args.file_to_read
    file_to_write = args.file_to_write
    xml_tree = get_xml_tree(file_to_read)
    validation_params = {
            'country_codes_list': list(args.country_list.split(',')),
            'language_codes_list': list(args.lang_list.split(','))
        }

    data = validate_xml_tree(xml_tree, validation_params)

    write_to_csv(data, file_to_write)
