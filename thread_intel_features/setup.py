import os
import configparser
import os.path as op

from flask import Flask
from flask_restful import Api

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

from thread_intel_features.features import *

def load_ini_config(_app: Flask):
    """Try to find a 'config.ini' file in these places:
    - running directory
    - Other place specified by environment var 'INI_CONFIG_FILE'
    """
    running_dir = op.abspath(os.getcwd())

    loaded_config = None

    if op.exists(op.join(running_dir, "config.ini")):
        loaded_config = configparser.ConfigParser()
        loaded_config.read(op.join(running_dir, "config.ini"))

    elif _app.config.get("INI_CONFIG_FILE", None):
        _init_file = _app.config.get("INI_CONFIG_FILE", None)

        if op.exists(_init_file):
            loaded_config = configparser.ConfigParser()
            loaded_config.read(_init_file)

    features = (
        "ddns",
        "idnhattack",
        "favicon",
        "strcomparison",
        "webshell",
        "domainage",
        "dnsttl",
        "fw",
        "numberips",
        "numbercountries",
        "subdomains",
        "hsts",
        "iframe",
        "sfh",
        "formmail",
        "msltags",
        "phishingbrands",
    )

    if loaded_config:
        cfg = loaded_config['features']

        for fet in features:
            if cfg.getboolean(fet):
                _app.config[fet.upper()] = True

def enable_end_points(_app: Flask, _api):
    features = {
        "ddns": (DDns, '/ff/ddns/<domain>'),
        "idnhattack": (IDNHomographAttack, '/ff/idnhattack/<domain>'),
        "favicon": (Favicon, '/ff/favicon/<domain>'),
        "strcomparison": (StrComparison, '/ff/strcomparison/<domain>'),
        "webshell": (WebShell, '/ff/webshell/<domain>'),
        "domainage": (DomainAge, '/ff/domainage/<domain>'),
        "dnsttl": (DnsTTL, '/ff/dnsttl/<domain>'),
        "fw": (FW, '/ff/fw/<domain>'),
        "numberips": (NumberIPs, '/ff/numberips/<domain>'),
        "numbercountries": (NumberCountries, '/ff/numbercountries/<domain>'),
        "subdomains": (Subdomains, '/ff/subdomains/<domain>'),
        "hsts": (HSTS, '/ff/hsts/<domain>'),
        "iframe": (Iframe, '/ff/iframe/<domain>'),
        "sfh": (SHF, '/ff/sfh/<domain>'),
        "formmail": (FormMail, '/ff/formmail/<domain>'),
        "msltags": (MSLtags, '/ff/msltags/<domain>'),
        "phishingbrands": (PhishingBrands, '/ff/phishingbrands/<domain>')
    }

    for fet, (obj, end_point) in features.items():

        if fet.upper() in _app.config:
            _api.add_resource(obj, end_point)

def setup_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("thread_intel_features.settings.EnabledFeatures")
    load_ini_config(app)

    api = Api(app)

    enable_end_points(app, api)

    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='Threat Intel Features',
            version='v1',
            plugins=[MarshmallowPlugin()],
            openapi_version='2.0.0'
        ),
        'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
        'APISPEC_SWAGGER_UI_URL': '/'  # URI to access UI of API Doc
    })

    docs = FlaskApiSpec(app)
    docs.register(Favicon)
    docs.register(IDNHomographAttack)
    docs.register(DDns)
    docs.register(StrComparison)
    docs.register(WebShell)
    docs.register(DomainAge)
    docs.register(DnsTTL)
    docs.register(FW)
    docs.register(NumberIPs)
    docs.register(NumberCountries)
    docs.register(Subdomains)
    docs.register(HSTS)
    docs.register(Iframe)
    docs.register(SHF)
    docs.register(FormMail)
    docs.register(MSLtags)
    docs.register(PhishingBrands)

    return app
