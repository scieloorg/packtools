# coding:utf-8
import os
import pkg_resources


try:
    PACKTOOLS_VERSION = pkg_resources.get_distribution("packtools").version
except pkg_resources.DistributionNotFound:
    PACKTOOLS_VERSION = None


class ProductionConfig(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True

    # Linguagens suportados
    LANGUAGES = {"pt_BR": "Português", "en": "English", "es": "Español"}

    # linguagem padrão:
    BABEL_DEFAULT_LOCALE = "pt_BR"
    SECRET_KEY = os.environ.get("SECRET_KEY", "s3kr3tk3y")
    LOCAL_ZONE = os.environ.get("LOCAL_ZONE", "America/Sao_Paulo")
    SETTINGS_MAX_UPLOAD_SIZE = 512 * 1024  # max size in byte to upload xml to validator
    PACKTOOLS_VERSION = PACKTOOLS_VERSION

    # Versão mais antiga suportada do SPS, na qual o usuario do
    # StyleChecker deve ser notficado do Deprecation Warning.
    # A versão deve respeitar o formato do atributo @specific-use: 'sps-1.1' ou 'sps-1.2'.
    PACKTOOLS_DEPRECATION_WARNING_VERSION = "sps-1.1"


class DevelopmentConfig(ProductionConfig):
    DEVELOPMENT = True
    DEBUG = True

    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG_TB_PANELS = [
        # default:
        "flask_debugtoolbar.panels.versions.VersionDebugPanel",
        "flask_debugtoolbar.panels.timer.TimerDebugPanel",
        "flask_debugtoolbar.panels.headers.HeaderDebugPanel",
        "flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel",
        "flask_debugtoolbar.panels.config_vars.ConfigVarsDebugPanel",
        "flask_debugtoolbar.panels.template.TemplateDebugPanel",
        "flask_debugtoolbar.panels.sqlalchemy.SQLAlchemyDebugPanel",
        "flask_debugtoolbar.panels.logger.LoggingPanel",
        "flask_debugtoolbar.panels.route_list.RouteListDebugPanel",
        "flask_debugtoolbar.panels.profiler.ProfilerDebugPanel",
    ]


class TestingConfig(ProductionConfig):
    TESTING = True
