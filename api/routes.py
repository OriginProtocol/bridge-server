from api.modules import attestations, search


def add_resources(api, resources, namespace):
    for path, resource in resources.items():
        print("Adding resource %s -> %s" % (resource, namespace+path))
        api.add_resource(resource, namespace + path)


def init_routes(api):
    # add routes for new modules here
    add_resources(api, attestations.resources, '/api/attestations/')
    add_resources(api, search.resources, '/api/search/')
