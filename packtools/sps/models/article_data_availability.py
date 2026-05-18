"""
<article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article">
    <back>
        <sec sec-type="data-availability" specific-use="data-available-upon-request">
            <label>Data availability statement</label>
            <p>Data will be available upon request.</p>
        </sec>
        <fn-group>
            <fn fn-type="data-availability" specific-use="data-available" id="fn1">
                <label>Data Availability Statement</label>
                <p>The data and code used to generate plots and perform statistical analyses have been
                uploaded to the Open Science Framework archive: <ext-link ext-link-type="uri"
                xlink:href="https://osf.io/jw6vg/?view_only=0335a15b6db3477f93d0ae636cdf3b4e">https://osf.io/j
                w6vg/?view_only=0335a15b6db3477f93d0ae636cdf3b4e</ext-link>.</p>
            </fn>
        </fn-group>
    </back>
</article>
"""

from packtools.sps.models.article_and_subarticles import Fulltext


import warnings as _warnings


def __getattr__(name):
    _moved = {
        "DataAvailability": "packtools.sps.validation.models.article_data_availability",
    }
    if name in _moved:
        import importlib
        _warnings.warn(
            f"{name} has moved to {_moved[name]}. "
            f"Importing from packtools.sps.models.article_data_availability is deprecated.",
            DeprecationWarning,
            stacklevel=2,
        )
        mod = importlib.import_module(_moved[name])
        return getattr(mod, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
