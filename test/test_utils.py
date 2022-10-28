import unittest
import src.utils as utils

class TestUtils(unittest.TestCase):

    def test_clean_sentence(self):

        self.assertEqual(utils.clean_sentence("@Rocky Island"), "at Rocky Island")
        self.assertEqual(utils.clean_sentence("Rockstar w/ Hotstar"), "Rockstar with Hotstar")
        self.assertEqual(utils.clean_sentence("El Destructor~La Fama"), "El Destructor, La Fama")
        self.assertEqual(utils.clean_sentence("Sally•Can't•Dance"), "Sally Can't Dance")
        self.assertEqual(utils.clean_sentence("Bülent Ceylan „Lassmalache“"), "Bülent Ceylan 'Lassmalache'")
        self.assertEqual(utils.clean_sentence("Future • Special guests THEMM • Bubba & Friends"), "Future | Special guests THEMM | Bubba & Friends")
        self.assertEqual(utils.clean_sentence("Luxtorpeda w Suwałkach >Piwiarnia<"),"Luxtorpeda with Suwałkach >Piwiarnia<")
    
if __name__ == '__main__':
    unittest.main()