"""
XMLAbstracts moved back to packtools.sps.models.v2.abstract.

PR #1180 (2026-05) moved it here believing it was used only by validation
code; that premise was wrong (scms-upload's TOC builder consumes it
directly for presentation data via packtools.sps.models.v2.abstract, not
for validation). Kept as a compatibility redirect only: this module
should not gain new logic, since the class itself carries no
validation-rule/expected-value concerns and doesn't belong here.
"""
from packtools.sps.models.v2.abstract import Abstract, XMLAbstracts
