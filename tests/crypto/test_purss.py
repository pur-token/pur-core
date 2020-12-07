# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
from unittest import TestCase

from pypurlib.pypurlib import str2bin, purssFast, bin2hstr, SHAKE_128, SHAKE_256, SHA2_256

from pur.core.misc import logger
from pur.crypto.purss import purSS
from tests.misc.helper import get_alice_purss

logger.initialize_default()


class TestpurSS(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestpurSS, self).__init__(*args, **kwargs)

    def test_sign_verify(self):
        message = "This is a test"
        message_bin = str2bin(message)

        purss_height = 10
        seed = bytearray([i for i in range(48)])
        purss = purSS(purssFast(seed, purss_height))

        pk = purss.pk

        purss.set_ots_index(1)

        for i in range(10):
            self.assertTrue(purss.ots_index == i + 1)
            signature = purss.sign(message_bin)
            self.assertTrue(purssFast.verify(message_bin, signature, pk))

    def test_PK(self):
        purss_height = 10
        seed = bytearray([i for i in range(48)])
        purss = purSS(purssFast(seed, purss_height))

        pk = purss.pk
        self.assertEqual('010500ffc6e502e2a8244aed6a8cd67531e79f95baa638615ba789c194a1d15d7eb'
                         '77e4e3983bd564298c49ae2e7fa6e28d4b954d8cd59398f1225b08d6144854aee0e', bin2hstr(pk))

    def test_hash_function(self):
        purss_height = 4
        seed = bytearray([i for i in range(48)])
        purss = purSS(purssFast(seed, purss_height, SHAKE_128))
        self.assertEqual('shake128', purss.hash_function)

        purss = purSS(purssFast(seed, purss_height, SHAKE_256))
        self.assertEqual('shake256', purss.hash_function)

        purss = purSS(purssFast(seed, purss_height, SHA2_256))
        self.assertEqual('sha2_256', purss.hash_function)

    def test_signature_type(self):
        purss_height = 4
        seed = bytearray([i for i in range(48)])
        purss = purSS(purssFast(seed, purss_height))
        self.assertEqual(0, purss.signature_type)

    def test_from_height_custom_hash(self):
        purss_height = 4
        purss = purSS.from_height(purss_height, "shake128")
        self.assertEqual('shake128', purss.hash_function)

    def test_get_height_from_sig_size(self):
        with self.assertRaises(Exception):
            purSS.get_height_from_sig_size(2179)

        with self.assertRaises(Exception):
            purSS.get_height_from_sig_size(0)

        with self.assertRaises(Exception):
            purSS.get_height_from_sig_size(-1)

        height = purSS.get_height_from_sig_size(3204)
        self.assertEqual(height, 32)

        height = purSS.get_height_from_sig_size(2180)
        self.assertEqual(height, 0)

    def test_validate_signature(self):
        purss = get_alice_purss()
        purss2 = get_alice_purss(8)
        pk = purss.pk
        signature = purss.sign(b"hello")

        self.assertTrue(purSS.validate_signature(signature, pk))

        with self.assertRaises(ValueError):
            purSS.validate_signature(signature, None)

        self.assertFalse(purSS.validate_signature(signature, purss2.pk))
