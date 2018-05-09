from logic.indexer_service import DatabaseIndexer, EventHandler

from database.db_models import Listing, Purchase


class TestDBIndexer():

    def test_new_listing_create(self, db, web3, wait_for_block,
                                wait_for_transaction, listing_contract, mock_ipfs,
                                eth_tester_provider):
        address = listing_contract.address
        handler = EventHandler(web3=web3)
        listing_data = handler._fetch_listing_data(address)

        db_indexer = DatabaseIndexer()
        db_indexer.create_or_update_listing(listing_data)

        assert Listing.query.filter_by(contract_address=address).count() == 1


    def test_new_purchase_create(self, db, web3, wait_for_block,
                                 wait_for_transaction, listing_contract,
                                 purchase_contract, mock_ipfs):
        handler = EventHandler(web3=web3)
        listing_data = handler._fetch_listing_data(listing_contract.address)
        purchase_data = handler._fetch_purchase_data(purchase_contract.address)

        db_indexer = DatabaseIndexer()
        db_indexer.create_or_update_listing(listing_data)
        db_indexer.create_or_update_purchase(purchase_data)

        assert Listing.query\
            .filter_by(contract_address=listing_contract.address).count() == 1
        assert Purchase.query\
            .filter_by(contract_address=purchase_contract.address,
                       listing_address=listing_contract.address).count() == 1

