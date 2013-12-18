import pprint


def main():
    # zopeloader will be available during testing
    from zopeloader import zope_loader
    loader = zope_loader('app')
    # Print ordered config so we can check in doctest
    pprint.pprint(sorted(loader.read_configuration().items()))
