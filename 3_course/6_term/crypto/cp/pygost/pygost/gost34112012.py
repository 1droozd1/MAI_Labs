# coding: utf-8
# PyGOST -- Pure Python GOST cryptographic functions library
# Copyright (C) 2015-2023 Sergey Matveev <stargrave@stargrave.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""GOST R 34.11-2012 (Streebog) hash function common files

This is implementation of :rfc:`6986`. Most function and variable names are
taken according to specification's terminology.
"""

from copy import copy
from struct import pack
from struct import unpack

from pygost.iface import PEP247
from pygost.utils import hexdec
from pygost.utils import strxor
from pygost.utils import xrange


BLOCKSIZE = 64
Pi = bytearray((
    252, 238, 221,  17, 207, 110,  49,  22, 251, 196, 250,
    218,  35, 197,   4,  77, 233, 119, 240, 219, 147,  46,
    153, 186,  23,  54, 241, 187,  20, 205,  95, 193, 249,
     24, 101,  90, 226,  92, 239,  33, 129,  28,  60,  66,
    139,   1, 142,  79,   5, 132,   2, 174, 227, 106, 143,
    160,   6,  11, 237, 152, 127, 212, 211,  31, 235,  52,
     44,  81, 234, 200,  72, 171, 242,  42, 104, 162, 253,
     58, 206, 204, 181, 112,  14,  86,   8,  12, 118,  18,
    191, 114,  19,  71, 156, 183,  93, 135,  21, 161, 150,
     41,  16, 123, 154, 199, 243, 145, 120, 111, 157, 158,
    178, 177,  50, 117,  25,  61, 255,  53, 138, 126, 109,
     84, 198, 128, 195, 189,  13,  87, 223, 245,  36, 169,
     62, 168,  67, 201, 215, 121, 214, 246, 124,  34, 185,
      3, 224,  15, 236, 222, 122, 148, 176, 188, 220, 232,
     40,  80,  78,  51,  10,  74, 167, 151,  96, 115,  30,
      0,  98,  68,  26, 184,  56, 130, 100, 159,  38,  65,
    173,  69,  70, 146,  39,  94,  85,  47, 140, 163, 165,
    125, 105, 213, 149,  59,   7,  88, 179,  64, 134, 172,
     29, 247,  48,  55, 107, 228, 136, 217, 231, 137, 225,
     27, 131,  73,  76,  63, 248, 254, 141,  83, 170, 144,
    202, 216, 133,  97,  32, 113, 103, 164,  45,  43,   9,
     91, 203, 155,  37, 208, 190, 229, 108,  82,  89, 166,
    116, 210, 230, 244, 180, 192, 209, 102, 175, 194,  57,
     75,  99, 182,
))

A = [unpack(">Q", hexdec(s))[0] for s in (
    "8e20faa72ba0b470", "47107ddd9b505a38", "ad08b0e0c3282d1c", "d8045870ef14980e",
    "6c022c38f90a4c07", "3601161cf205268d", "1b8e0b0e798c13c8", "83478b07b2468764",
    "a011d380818e8f40", "5086e740ce47c920", "2843fd2067adea10", "14aff010bdd87508",
    "0ad97808d06cb404", "05e23c0468365a02", "8c711e02341b2d01", "46b60f011a83988e",
    "90dab52a387ae76f", "486dd4151c3dfdb9", "24b86a840e90f0d2", "125c354207487869",
    "092e94218d243cba", "8a174a9ec8121e5d", "4585254f64090fa0", "accc9ca9328a8950",
    "9d4df05d5f661451", "c0a878a0a1330aa6", "60543c50de970553", "302a1e286fc58ca7",
    "18150f14b9ec46dd", "0c84890ad27623e0", "0642ca05693b9f70", "0321658cba93c138",
    "86275df09ce8aaa8", "439da0784e745554", "afc0503c273aa42a", "d960281e9d1d5215",
    "e230140fc0802984", "71180a8960409a42", "b60c05ca30204d21", "5b068c651810a89e",
    "456c34887a3805b9", "ac361a443d1c8cd2", "561b0d22900e4669", "2b838811480723ba",
    "9bcf4486248d9f5d", "c3e9224312c8c1a0", "effa11af0964ee50", "f97d86d98a327728",
    "e4fa2054a80b329c", "727d102a548b194e", "39b008152acb8227", "9258048415eb419d",
    "492c024284fbaec0", "aa16012142f35760", "550b8e9e21f7a530", "a48b474f9ef5dc18",
    "70a6a56e2440598e", "3853dc371220a247", "1ca76e95091051ad", "0edd37c48a08a6d8",
    "07e095624504536c", "8d70c431ac02a736", "c83862965601dd1b", "641c314b2b8ee083",
)]

Tau = (
    0,  8, 16, 24, 32, 40, 48, 56,
    1,  9, 17, 25, 33, 41, 49, 57,
    2, 10, 18, 26, 34, 42, 50, 58,
    3, 11, 19, 27, 35, 43, 51, 59,
    4, 12, 20, 28, 36, 44, 52, 60,
    5, 13, 21, 29, 37, 45, 53, 61,
    6, 14, 22, 30, 38, 46, 54, 62,
    7, 15, 23, 31, 39, 47, 55, 63,
)

C = [hexdec("".join(s))[::-1] for s in (
    (
        "b1085bda1ecadae9ebcb2f81c0657c1f",
        "2f6a76432e45d016714eb88d7585c4fc",
        "4b7ce09192676901a2422a08a460d315",
        "05767436cc744d23dd806559f2a64507",
    ),
    (
        "6fa3b58aa99d2f1a4fe39d460f70b5d7",
        "f3feea720a232b9861d55e0f16b50131",
        "9ab5176b12d699585cb561c2db0aa7ca",
        "55dda21bd7cbcd56e679047021b19bb7",
    ),
    (
        "f574dcac2bce2fc70a39fc286a3d8435",
        "06f15e5f529c1f8bf2ea7514b1297b7b",
        "d3e20fe490359eb1c1c93a376062db09",
        "c2b6f443867adb31991e96f50aba0ab2",
    ),
    (
        "ef1fdfb3e81566d2f948e1a05d71e4dd",
        "488e857e335c3c7d9d721cad685e353f",
        "a9d72c82ed03d675d8b71333935203be",
        "3453eaa193e837f1220cbebc84e3d12e",
    ),
    (
        "4bea6bacad4747999a3f410c6ca92363",
        "7f151c1f1686104a359e35d7800fffbd",
        "bfcd1747253af5a3dfff00b723271a16",
        "7a56a27ea9ea63f5601758fd7c6cfe57",
    ),
    (
        "ae4faeae1d3ad3d96fa4c33b7a3039c0",
        "2d66c4f95142a46c187f9ab49af08ec6",
        "cffaa6b71c9ab7b40af21f66c2bec6b6",
        "bf71c57236904f35fa68407a46647d6e",
    ),
    (
        "f4c70e16eeaac5ec51ac86febf240954",
        "399ec6c7e6bf87c9d3473e33197a93c9",
        "0992abc52d822c3706476983284a0504",
        "3517454ca23c4af38886564d3a14d493",
    ),
    (
        "9b1f5b424d93c9a703e7aa020c6e4141",
        "4eb7f8719c36de1e89b4443b4ddbc49a",
        "f4892bcb929b069069d18d2bd1a5c42f",
        "36acc2355951a8d9a47f0dd4bf02e71e",
    ),
    (
        "378f5a541631229b944c9ad8ec165fde",
        "3a7d3a1b258942243cd955b7e00d0984",
        "800a440bdbb2ceb17b2b8a9aa6079c54",
        "0e38dc92cb1f2a607261445183235adb",
    ),
    (
        "abbedea680056f52382ae548b2e4f3f3",
        "8941e71cff8a78db1fffe18a1b336103",
        "9fe76702af69334b7a1e6c303b7652f4",
        "3698fad1153bb6c374b4c7fb98459ced",
    ),
    (
        "7bcd9ed0efc889fb3002c6cd635afe94",
        "d8fa6bbbebab07612001802114846679",
        "8a1d71efea48b9caefbacd1d7d476e98",
        "dea2594ac06fd85d6bcaa4cd81f32d1b",
    ),
    (
        "378ee767f11631bad21380b00449b17a",
        "cda43c32bcdf1d77f82012d430219f9b",
        "5d80ef9d1891cc86e71da4aa88e12852",
        "faf417d5d9b21b9948bc924af11bd720",
    ),
)]


def _lcache():
    cache = []
    for byteN in xrange(8):
        cache.append([0 for _ in xrange(256)])
    for byteN in xrange(8):
        for byteVal in xrange(256):
            res64 = 0
            val = byteVal
            for bitN in xrange(8):
                if val & 0x80 > 0:
                    res64 ^= A[(7 - byteN) * 8 + bitN]
                val <<= 1
            cache[byteN][byteVal] = res64
    return cache


# Trade memory for CPU for part of L() calculations
LCache = _lcache()


def add512bit(a, b):
    a = int.from_bytes(a, "little")
    b = int.from_bytes(b, "little")
    r = (a + b) % (1 << 512)
    return r.to_bytes(512 // 8, "little")


def g(n, hsh, msg):
    res = E(LPS(strxor(hsh[:8], pack("<Q", n)) + hsh[8:]), msg)
    return strxor(strxor(res, hsh), msg)


def E(k, msg):
    for i in range(12):
        msg = LPS(strxor(k, msg))
        k = LPS(strxor(k, C[i]))
    return strxor(k, msg)


def LPS(data):
    return L(PS(bytearray(data)))


def PS(data):
    res = bytearray(BLOCKSIZE)
    for i in range(BLOCKSIZE):
        res[Tau[i]] = Pi[data[i]]
    return res


def L(data):
    res = []
    for i in range(8):
        res64 = 0
        for j in range(8):
            res64 ^= LCache[j][data[8 * i + j]]
        res.append(pack("<Q", res64))
    return b"".join(res)


class GOST34112012(PEP247):
    """GOST 34.11-2012 big-endian hash

    >>> m = GOST34112012(digest_size=32)
    >>> m.update("foo")
    >>> m.update("bar")
    >>> m.hexdigest()
    'e3c9fd89226d93b489a9fe27d686806e24a514e3787bca053c698ec4616ceb78'
    """
    block_size = BLOCKSIZE

    def __init__(self, data=b"", digest_size=64):
        """
        :param digest_size: hash digest size to compute
        :type digest_size: 32 or 64 bytes
        """
        self._digest_size = digest_size
        self.hsh = BLOCKSIZE * (b"\x01" if digest_size == 32 else b"\x00")
        self.chk = bytearray(BLOCKSIZE * b"\x00")
        self.n = 0
        self.buf = b""
        self.update(data)

    def copy(self):
        obj = GOST34112012()
        obj._digest_size = self._digest_size
        obj.hsh = self.hsh
        obj.chk = copy(self.chk)
        obj.n = self.n
        obj.buf = self.buf
        return obj

    @property
    def digest_size(self):
        return self._digest_size

    def _update_block(self, block):
        self.hsh = g(self.n, self.hsh, block)
        self.chk = add512bit(self.chk, block)
        self.n += 512

    def update(self, data):
        """Update state with the new data
        """
        if len(self.buf) > 0:
            chunk_len = BLOCKSIZE - len(self.buf)
            self.buf += data[:chunk_len]
            data = data[chunk_len:]
            if len(self.buf) == BLOCKSIZE:
                self._update_block(self.buf)
                self.buf = b""
        while len(data) >= BLOCKSIZE:
            self._update_block(data[:BLOCKSIZE])
            data = data[BLOCKSIZE:]
        self.buf += data

    def digest(self):
        """Get hash of the provided data
        """
        data = self.buf

        # Padding
        padblock_size = len(data) * 8
        data += b"\x01"
        padlen = BLOCKSIZE - len(data)
        if padlen != BLOCKSIZE:
            data += b"\x00" * padlen

        hsh = g(self.n, self.hsh, data)
        n = self.n + padblock_size
        chk = add512bit(self.chk, data)
        hsh = g(0, hsh, pack("<Q", n) + 56 * b"\x00")
        hsh = g(0, hsh, chk)
        return hsh[-self._digest_size:]
