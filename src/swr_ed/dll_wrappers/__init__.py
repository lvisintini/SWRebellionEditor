try:
    import win32api
    import pywintypes
except ModuleNotFoundError:
    text_stra = None
else:
    from .textstra import TextStraWrapper
    text_stra = TextStraWrapper()
