from tomodachi.__version__ import __version__  # noqa

CLASS_ATTRIBUTE = 'TOMODACHI_SERVICE_CLASS'


def service(cls):
    setattr(cls, CLASS_ATTRIBUTE, True)
    return cls
