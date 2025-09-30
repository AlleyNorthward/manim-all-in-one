
def override_insert_sq(decorator_method, mode):
    if not hasattr(decorator_method, "_overrides"):
        decorator_method._overrides = {}
    def decorator(actual_method):
        decorator_method._overrides[mode] = actual_method
        return actual_method
    return decorator