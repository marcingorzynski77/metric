from time import time
import unittest2
from sqlalchemy.orm import sessionmaker
from crypto.domain import suggestion, pair, opportunity, tick
from crypto.db import api

class TestDb(unittest2.TestCase):

    def test_db_interactions(self):
        engine = api.Api.create_sqlite_db()
        #api.Api.create_postgres_db()

        DBSession = sessionmaker(bind=engine)
        # A DBSession() instance establishes all conversations with the database
        # and represents a "staging zone" for all the objects loaded into the
        # database session object. Any change made against the objects in the
        # session won't be persisted into the database until you call
        # session.commit(). If you're not happy about the changes, you can
        # revert all of them back to the last commit by calling
        # session.rollback()
        session = DBSession()

        suggestion_obj = suggestion.Suggestion(tick.Bid.create(int(time()), 1,1,1,"cexio"), tick.Ask.create(int(time()),1,1,1,"binance"), "cexio", "binance", 10, 1, "GBP", pair.Pair("ETH","EUR"), 1,2,50,23)
        db_obj = api.Suggestion.create(suggestion_obj)

        session.query(api.Suggestion).delete()
        session.add(db_obj)
        session.commit()

        suggestions = [suggestion_obj]
        self.assertEqual(session.query(api.Suggestion).count(), 1)

        session.query(api.Opportunity).delete()
        opportunity_obj = opportunity.Opportunity(suggestions, pair.Pair("ETH","EUR"), 10, 10, 1, 20,  "GBP", 50, 23)
        db_obj = api.Opportunity.create(opportunity_obj)
        session.add(db_obj)
        session.commit()

        self.assertEqual(session.query(api.Opportunity).count(), 1)

        self.assertEqual(session.query(api.Opportunity.suggestions).count(), 2)

        #load full object
        record =  session.query(api.Opportunity).first()
        self.assertEqual(record.qty, 10)

        domain_deserialized = api.Opportunity.convert_to_domain(record)
        self.assertEqual(domain_deserialized.qty, 10)
        self.assertEqual(len(domain_deserialized.suggestions), 1)