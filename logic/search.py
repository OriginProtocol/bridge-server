import re

from elasticsearch import Elasticsearch

from config import settings
from util.singleton import Singleton


class QueryError(Exception):
    pass


class SearchClient(Singleton):
    """
    Client for back-end search engine.

    This implementation uses ElasticSearch. On dev environment it connects to
    a local instance while in prod environment it uses "Bonsai ElasticSearch"
    which is a hosted solution provided as a Heroku add-on.

    Callers should call the SearchClient.instance() method to get an
    instance of the client.
    """
    def __init__(self, client=None):
        if client:
            self.client = client
        elif settings.DEBUG:
            # Point to local ElasticSearch instance running on local host.
            self.client = Elasticsearch()
        else:
            # Prod environment. Parse the auth and host from BONSAI_URL env.
            bonsai = settings.BONSAI_URL
            assert bonsai
            (user, pwd) = re.search(r'https://(.*)@', bonsai).group(1).split(':')
            host = bonsai.replace('https://%s:%s@' % (user, pwd), '')

            # Connect to cluster over SSL using auth for best security:
            es_header = [{
                'host': host,
                'port': 443,
                'use_ssl': True,
                'http_auth': (user, pwd)
            }]
            self.client = Elasticsearch(es_header)

    def listings(self, query, category=None, location=None, num=0, offset=100):
        """
        Issues a search query against the listing data.
        """
        # Query for searching Listing data.
        # TODO(franck): If query gets more complex, consider using the
        # ElasticSearch DSL library for building it.
        query_template = '''{
          "from" : %d, "size" : %d,
          "query": {
            "bool": {
              "should": [
                {"match": {"name": "%s"}},
                {"match": {"description": "%s"}}
              ]
              %s
            }
          }
        }'''

        # Construct the optional filter clause.
        filters = []
        filter_clause = ""
        if category:
            filters.append('{"match": {"category": "%s"}}' % category)
        if location:
            filters.append('{"match": {"location": "%s"}}' % location)
        if filters:
            filter_clause = ',"must": [' + ",".join(filters) + ']'

        # Construct the query.
        query = query_template % (offset, num, query, query, filter_clause)

        # Query the search engine.
        res = self.client.search(
            index=["origin"],
            doc_type="listing",
            body=query)
        if res.get("error"):
            raise QueryError(res.get("reason"))

        # TODO(franck): Translate the "hit" object into a generic object that 
        # does not contain any ElasticSearch specifics since we should not
        # expose these to the DAPP.
        hits = res["hits"]["hits"]
        return {"listings": hits}
