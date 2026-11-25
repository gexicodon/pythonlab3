class ObjectCatalogError(Exception):
    pass

class InvalidItemError(ObjectCatalogError):
    pass

class DuplicateError(ObjectCatalogError):
    pass