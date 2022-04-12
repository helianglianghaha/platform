def is_truthy(item):
    if is_string(item):
        return item.upper() not in ('FALSE', 'NO', '', 'NONE')
    return bool(item)
def is_string(item):
    # Returns False with `b'bytes'` on IronPython on purpose. Results of
    # `isinstance(item, basestring)` would depend on IronPython 2.7.x version.
    return isinstance(item,str)
def is_falsy(item):
    return not is_truthy(item)