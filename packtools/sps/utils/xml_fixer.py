import logging
from lxml import etree

logger = logging.getLogger(__name__)


def _remove_and_get_info(xmltree, inline_graphic):
    """
    Removes inline-graphic from its current position and returns information about it.

    Args:
        xmltree: XML tree for XPath generation
        inline_graphic: inline-graphic element to be removed

    Returns:
        tuple: (old_parent, xpath) - parent element and XPath of the removed element

    Raises:
        ValueError: If inline-graphic has no parent
    """
    # Store information before modification
    old_parent = inline_graphic.getparent()

    if old_parent is None:
        raise ValueError("inline-graphic has no parent element")

    # Generate XPath for modification record
    try:
        xpath = xmltree.getroottree().getpath(inline_graphic)
    except (AttributeError, ValueError):
        xpath = f"./{old_parent.tag}/inline-graphic"

    # Remove inline-graphic from current position
    old_parent.remove(inline_graphic)

    return old_parent, xpath


def fix_inline_graphic_in_caption(xmltree):
    """
    Fixes inline-graphic elements incorrectly positioned inside caption/label.

    This function searches for containers (fig, table-wrap, disp-formula) that:
    - Contain inline-graphic inside label or caption
    - Do NOT have a graphic element
    - Do NOT have other child elements besides label and caption

    For each container found, if there is exactly one inline-graphic,
    it removes it from inside label/caption and creates a graphic element at the container level.

    Args:
        xmltree: XML tree to be processed

    Returns:
        list: List of dictionaries with the modifications performed
    """
    if xmltree is None:
        raise ValueError("xmltree cannot be None")

    modifications = []

    # XPath that searches for valid containers needing correction:
    # - Are fig, table-wrap or disp-formula
    # - Have inline-graphic inside label or caption
    # - Do NOT have a direct child graphic element
    xpath_containers = """
        (//fig | //table-wrap | //disp-formula)
        [(label//inline-graphic or caption//inline-graphic) and not(.//graphic)]
    """

    containers = xmltree.xpath(xpath_containers)

    for container in containers:
        # Search for all inline-graphics inside label or caption of this container
        inline_graphics = container.xpath(
            ".//label//inline-graphic | .//caption//inline-graphic"
        )

        # Process only if there is exactly 1 inline-graphic
        if len(inline_graphics) != 1:
            continue

        # Check if the container has only label and/or caption as children
        # If there are other elements (table, mathml:math, etc.), do not process
        has_only_label_caption = True
        for child in container.getchildren():
            if child.tag not in ("label", "caption"):
                has_only_label_caption = False
                break

        if not has_only_label_caption:
            logger.debug(
                f"Container {container.tag} has other children besides label/caption, skipping",
                extra={'container_tag': container.tag, 'container_id': container.get('id')}
            )
            continue

        inline_graphic = inline_graphics[0]

        try:
            # Remove inline-graphic and get its information
            old_parent, xpath = _remove_and_get_info(xmltree, inline_graphic)

            # Change tag from inline-graphic to graphic (preserves all attributes, text, tail, and children)
            inline_graphic.tag = "graphic"

            # Append graphic after label and caption (container only has label/caption at this point)
            container.append(inline_graphic)

            # Record modification performed
            modifications.append({
                "xpath": xpath,
                "action": "moved_and_renamed",
                "old_parent": old_parent.tag if old_parent is not None else "unknown",
                "new_parent": container.tag
            })

        except AttributeError as e:
            logger.error(
                f"Error processing inline-graphic in container {container.tag}: "
                f"missing attribute - {e}",
                extra={'container_tag': container.tag}
            )
            continue
        except ValueError as e:
            logger.error(
                f"Error processing inline-graphic in container {container.tag}: "
                f"invalid value - {e}",
                extra={'container_tag': container.tag}
            )
            continue
        except (etree.Error, etree.LxmlError) as e:
            logger.error(
                f"Error processing inline-graphic in container {container.tag}: "
                f"XML structure error - {e}",
                extra={'container_tag': container.tag}
            )
            continue
        except TypeError as e:
            logger.error(
                f"Error processing inline-graphic in container {container.tag}: "
                f"type error - {e}",
                extra={'container_tag': container.tag}
            )
            continue

    return modifications
