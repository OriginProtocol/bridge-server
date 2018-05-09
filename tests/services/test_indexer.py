from logic.indexer_service import DatabaseIndexer, EventHandler

from database.db_models import Listing, Purchase


class TestDBIndexer():

    def test_new_listing_create(self, db, web3, wait_for_block,
                                wait_for_transaction, listing_contract, mock_ipfs,
                                eth_tester_provider):
        address = listing_contract.address
        handler = EventHandler(web3=web3)
        listing_data = handler._fetch_listing_data(address)

        event_names = ['NewListing(uint256)',
                        'ListingPurchased(address)',
                        'ListingChange()',
                        'PurchaseChange(uint8)']
        event_name_hashes = []
        for name in event_names:
            event_name_hashes.append(web3.sha3(text=name).hex())
        filter = web3.eth.filter({
#            "topics": [event_name_hashes],
            "fromBlock": 0,
            "toBlock": 'latest'
        })
        counter = 0
        for event in events.get_all_entries():
            print("EVENT RECEIVED: %s" % event)
            counter += 1
        assert counter == 100

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

