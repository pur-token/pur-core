# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
from pypurlib import pypurlib
from pypurlib.pypurlib import bin2hstr, getRandomSeed, str2bin, bin2mnemonic, mnemonic2bin  # noqa
from pypurlib.pypurlib import purssFast, purDescriptor

hash_functions = {
    "shake128": pypurlib.SHAKE_128,
    "shake256": pypurlib.SHAKE_256,
    "sha2_256": pypurlib.SHA2_256
}
hash_functions_reverse = {v: k for k, v in hash_functions.items()}


class purSS(object):
    @staticmethod
    def from_extended_seed(extended_seed: bytes):
        if len(extended_seed) != 51:
            raise Exception('Extended seed should be 51 bytes long')

        descr = purDescriptor.fromBytes(extended_seed[0:3])
        if descr.getSignatureType() != pypurlib.purSS:
            raise Exception('Signature type nor supported')

        height = descr.getHeight()
        hash_function = descr.getHashFunction()
        tmp = purssFast(extended_seed[3:], height, hash_function)
        return purSS(tmp)

    @staticmethod
    def from_height(tree_height: int, hash_function="shake128"):
        if hash_function not in hash_functions:
            raise Exception("purSS does not support this hash function!")

        seed = getRandomSeed(48, '')
        return purSS(purssFast(seed, tree_height, hash_functions[hash_function]))

    def __init__(self, _purssfast):
        """
        :param
        tree_height: height of the tree to generate. number of OTS keypairs=2**tree_height
        :param _purssfast:

        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed1)
        >>> tmp.height
        4

        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed1)
        >>> tmp._purss.getSignatureSize()
        2308

        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed1)
        >>> bin2hstr( tmp._purss.getPK() )
        '000200eb0372d56b886645e7c036b480be95ed97bc431b4e828befd4162bf432858df83191da3442686282b3d5160f25cf162a517fd2131f83fbf2698a58f9c46afc5d'

        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed1)
        >>> len( tmp._purss.getPK() )
        67

        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed1)
        >>> bin2hstr( tmp._purss.getSK() ) == purss_sk_expected1
        True

        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed1)
        >>> bin2hstr( tmp._purss.getRoot() )
        'eb0372d56b886645e7c036b480be95ed97bc431b4e828befd4162bf432858df8'

        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed1)
        >>> bin2hstr( tmp._purss.getPKSeed() )
        '3191da3442686282b3d5160f25cf162a517fd2131f83fbf2698a58f9c46afc5d'

        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed1)
        >>> tmp._purss.getIndex()
        0

        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed1)
        >>> bin2hstr( tmp._purss.getSKSeed() )
        'eda313c95591a023a5b37f361c07a5753a92d3d0427459f34c7895d727d62816'

        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed1)
        >>> bin2hstr( tmp._purss.getSKPRF() )
        'b3aa2224eb9d823127d4f9f8a30fd7a1a02c6483d9c0f1fd41957b9ae4dfc63a'

        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed1)
        >>> bin2hstr(tmp._purss.getAddress())
        '00020096e5c065cf961565169e795803c1e60f521af7a3ea0326b42aa40c0e75390e5d8f4336de'
        """
        self._purss = _purssfast

    @property
    def hash_function(self) -> str:
        descr = self._purss.getDescriptor()
        function_num = descr.getHashFunction()
        function_name = hash_functions_reverse[function_num]
        if not function_name:
            raise Exception("Could not reverse-lookup the hash function")

        return function_name

    @property
    def signature_type(self):
        descr = self._purss.getDescriptor()
        answer = descr.getSignatureType()
        return answer

    @property
    def height(self):
        return self._purss.getHeight()

    @property
    def _sk(self):
        """
        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed1)
        >>> len(tmp._sk)
        132

        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed1)
        >>> bin2hstr(tmp._sk) == purss_sk_expected1
        True

        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed2)
        >>> bin2hstr(tmp._sk) == purss_sk_expected2
        True
        """
        return bytes(self._purss.getSK())

    @property
    def pk(self):
        """
        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed1)
        >>> bin2hstr(tmp.pk) == purss_pk_expected1
        True
        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed1)
        >>> bin2hstr(tmp.pk) == purss_pk_expected2
        True
        """
        return bytes(self._purss.getPK())

    @property
    def number_signatures(self) -> int:
        """
        Returns the number of signatures in the purSS tree
        :return:
        :rtype:

        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed1)
        >>> tmp.number_signatures
        16
        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed1)
        >>> tmp.number_signatures
        16
        """
        return self._purss.getNumberSignatures()

    @property
    def remaining_signatures(self):
        """
        Returns the number of remaining signatures in the purSS tree
        :return:
        :rtype:

        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed1)
        >>> tmp.remaining_signatures
        16
        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed1)
        >>> tmp.remaining_signatures
        16
        """
        return self._purss.getRemainingSignatures()

    @property
    def mnemonic(self) -> str:
        """
        :return:
        :rtype:

        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(hstr2bin(purss_mnemonic_eseed1))
        >>> tmp.mnemonic == purss_mnemonic_test1
        True
        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(hstr2bin(purss_mnemonic_eseed2))
        >>> tmp.mnemonic == purss_mnemonic_test2
        True
        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(mnemonic2bin(purss_mnemonic_test1))
        >>> tmp.mnemonic == purss_mnemonic_test1
        True
        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(mnemonic2bin(purss_mnemonic_test2))
        >>> tmp.mnemonic == purss_mnemonic_test2
        True
        """
        return bin2mnemonic(self._purss.getExtendedSeed())

    @property
    def address(self) -> bytes:
        return bytes(self._purss.getAddress())

    @property
    def qaddress(self) -> str:
        return 'Q' + bin2hstr(self.address)

    @property
    def ots_index(self) -> int:
        """
        :return:
        :rtype:

        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed1)
        >>> tmp.ots_index
        0
        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed1)
        >>> tmp.ots_index
        0
        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed1)
        >>> s = tmp.sign(str2bin("test"))
        >>> tmp.ots_index
        1
        """
        return self._purss.getIndex()

    def set_ots_index(self, new_index):
        """
        :return:
        :rtype:

        >>> from pur.crypto.doctest_data import *
        >>> purss = purSS.from_extended_seed(purss_test_eseed1)
        >>> purss.set_ots_index(1)
        >>> purss.ots_index
        1
        >>> from pur.crypto.doctest_data import *
        >>> purss = purSS.from_extended_seed(purss_test_eseed1)
        >>> purss.set_ots_index(10)
        >>> purss.ots_index
        10
        """
        self._purss.setIndex(new_index)

    @property
    def hexseed(self) -> str:
        """
        :return:
        :rtype:

        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed1)
        >>> tmp.hexseed
        '000200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'

        >>> tmp = purSS.from_extended_seed(purss_test_eseed2)
        >>> tmp.hexseed
        '000200010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101'
        """
        return bin2hstr(self._purss.getExtendedSeed())

    @property
    def extended_seed(self):
        """
        :return:
        :rtype:

        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed1)
        >>> bin2hstr( tmp.seed )
        '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'

        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed2)
        >>> bin2hstr( tmp.extended_seed )
        '000200010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101'
        """
        return self._purss.getExtendedSeed()

    @property
    def seed(self):
        """
        :return:
        :rtype:

        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed1)
        >>> bin2hstr( tmp.seed )
        '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'

        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed2)
        >>> bin2hstr( tmp.seed )
        '010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101'
        """
        return self._purss.getSeed()

    def sign(self, message: bytes) -> bytes:
        """
        :param message:
        :return:

        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed1)
        >>> bin2hstr(tmp.sign(str2bin("test_message"))) == purss_sign_expected1
        True
        >>> from pur.crypto.doctest_data import *
        >>> tmp = purSS.from_extended_seed(purss_test_eseed2)
        >>> bin2hstr(tmp.sign(str2bin("test_message"))) == purss_sign_expected2
        True
        """
        return bytes(self._purss.sign(message))

    @staticmethod
    def get_height_from_sig_size(sig_size: int) -> int:
        min_size = 4 + 32 + 67 * 32

        if sig_size < min_size:
            raise Exception("Invalid Signature Size")

        if (sig_size - 4) % 32 != 0:
            raise Exception("Invalid Signature Size")

        height = (sig_size - min_size) // 32

        return height

    @staticmethod
    def validate_signature(signature, PK):
        height = purSS.get_height_from_sig_size(len(signature))

        if height == 0 or 2 * int(bin2hstr(PK)[2:4]) != height:
            return False

        return True


if __name__ == "__main__":
    import doctest

    doctest.testmod()
