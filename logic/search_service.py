import re
import logging

from elasticsearch import Elasticsearch

from config import settings


class SearchIndexer():
    """
    SearchIndexer indexes events in a search engine.
    This implementation uses "Bonsai ElasticSearch" provided
    as a Heroku Add-on.
    """

    def __init__(self, client=None):
        if client:
            # A client may get passed to inject a mock for testing.
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

            # Instantiate an Elasticsearch client.
            self.client = Elasticsearch(es_header)

    def create_or_update_listing(self, listing_data):
        # Create a doc for indexing.
        ipfs_data = listing_data['ipfs_data']
        doc = {
            'name': ipfs_data.get('name'),
            'category': ipfs_data.get('category'),
            'description': ipfs_data.get('description'),
            'location': ipfs_data.get('location'),
            'price': listing_data['price'],
        }
        # Use the Listing's contract address as unique doc id.
        doc_id = listing_data['contract_address']

        # Index the doc.
        res = self.client.index(
            index="origin",
            doc_type='listing',
            id=doc_id,
            body=doc)

        # TODO(franck): implement retry/error policy.
        if res['result'] not in ('created', 'updated'):
            logging.error("Failed indexing listing", res, listing_data)

    def create_or_update_purchase(self, purchase_data):
        # TODO(franck): delete the Listing from the index if no unit left.
        pass
