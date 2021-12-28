from __future__ import annotations
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #
#           < IN THE NAME OF GOD >           #
# ------------------------------------------ #
__AUTHOR__ = "ToorajJahangiri"
__EMAIL__ = "Toorajjahangiri@gmail.com"
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< #


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\^////////////////////////////// #

# FILE ERROR
class FileIsNotWritableError(IOError):
    pass


# INDEXES ERROR
class IndexesIsNotDefinedError(ValueError):
    pass


# FILE INDEXES ERROR
class AccessDeniedFileIsClosed(IOError):
    pass


# MODE NOT EXISTS -> `ModeName`
class ModeNotExistsError(NameError):
    pass


# ACTION NOT EXISTS -> `ModeName`
class ActionNotExistsError(NameError):
    pass
