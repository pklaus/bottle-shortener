
class ContainerPlugin(object):
    # http://docs.python.org/3.3/reference/datamodel.html#sequence-types
    def __len__(self):
        raise NotImplementedError()
    def __getitem__(self, key):
        raise NotImplementedError()
    def __setitem__(self, key, value):
        raise NotImplementedError()
    def __delitem__(self, key):
        raise NotImplementedError()
    def __iter__(self):
        raise NotImplementedError()
    def iterkeys(self):
        raise NotImplementedError()
    def __contains__(self, key):
        raise NotImplementedError()
    def clear(self):
        raise NotImplementedError()

class DictContainer(dict, ContainerPlugin):
    pass

