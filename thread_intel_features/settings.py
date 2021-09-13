from sanic_envconfig import EnvConfig

class EnabledFeatures(EnvConfig):
    DDNS: bool = True
    IDNHATTACK: bool = True
    FAVICON: bool = True
    STRCOMPARISON: bool = True
    WEBSHELL: bool = True
    DOMAINAGE: bool = True
    DNSTTL: bool = True
    FW: bool = True
    NUMBERIPS: bool = True
    NUMBERCOUNTRIES: bool = True
    SUBDOMAINS: bool = True
    HSTS: bool = True
    IFRAME: bool = True
    SFH: bool = True
    FORMMAIL: bool = True
    MSLTAGS: bool = True
    PHISHINGBRANDS: bool = True
    INI_CONFIG_FILE: str = None

