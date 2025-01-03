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

from os import urandom
from unittest import TestCase

from pygost.gost28147 import block2ns
from pygost.gost28147 import BLOCKSIZE
from pygost.gost28147 import cbc_decrypt
from pygost.gost28147 import cbc_encrypt
from pygost.gost28147 import cfb_decrypt
from pygost.gost28147 import cfb_encrypt
from pygost.gost28147 import cnt
from pygost.gost28147 import DEFAULT_SBOX
from pygost.gost28147 import ecb_decrypt
from pygost.gost28147 import ecb_encrypt
from pygost.gost28147 import encrypt
from pygost.gost28147 import KEYSIZE
from pygost.gost28147 import MESH_MAX_DATA
from pygost.gost28147 import ns2block
from pygost.utils import hexdec
from pygost.utils import strxor


class ECBTest(TestCase):
    def test_gcl(self):
        """Test vectors from libgcl3
        """
        sbox = "id-Gost28147-89-TestParamSet"
        key = hexdec(b"0475f6e05038fbfad2c7c390edb3ca3d1547124291ae1e8a2f79cd9ed2bcefbd")
        plaintext = bytes(bytearray((
            0x07, 0x06, 0x05, 0x04, 0x03, 0x02, 0x01, 0x00,
            0x0f, 0x0e, 0x0d, 0x0c, 0x0b, 0x0a, 0x09, 0x08,
            0x17, 0x16, 0x15, 0x14, 0x13, 0x12, 0x11, 0x10,
            0x1f, 0x1e, 0x1d, 0x1c, 0x1b, 0x1a, 0x19, 0x18,
            0x27, 0x26, 0x25, 0x24, 0x23, 0x22, 0x21, 0x20,
            0x2f, 0x2e, 0x2d, 0x2c, 0x2b, 0x2a, 0x29, 0x28,
            0x37, 0x36, 0x35, 0x34, 0x33, 0x32, 0x31, 0x30,
            0x3f, 0x3e, 0x3d, 0x3c, 0x3b, 0x3a, 0x39, 0x38,
            0x47, 0x46, 0x45, 0x44, 0x43, 0x42, 0x41, 0x40,
            0x4f, 0x4e, 0x4d, 0x4c, 0x4b, 0x4a, 0x49, 0x48,
            0x57, 0x56, 0x55, 0x54, 0x53, 0x52, 0x51, 0x50,
            0x5f, 0x5e, 0x5d, 0x5c, 0x5b, 0x5a, 0x59, 0x58,
            0x67, 0x66, 0x65, 0x64, 0x63, 0x62, 0x61, 0x60,
            0x6f, 0x6e, 0x6d, 0x6c, 0x6b, 0x6a, 0x69, 0x68,
            0x77, 0x76, 0x75, 0x74, 0x73, 0x72, 0x71, 0x70,
            0x7f, 0x7e, 0x7d, 0x7c, 0x7b, 0x7a, 0x79, 0x78,
            0x87, 0x86, 0x85, 0x84, 0x83, 0x82, 0x81, 0x80,
            0x8f, 0x8e, 0x8d, 0x8c, 0x8b, 0x8a, 0x89, 0x88,
            0x97, 0x96, 0x95, 0x94, 0x93, 0x92, 0x91, 0x90,
            0x9f, 0x9e, 0x9d, 0x9c, 0x9b, 0x9a, 0x99, 0x98,
            0xa7, 0xa6, 0xa5, 0xa4, 0xa3, 0xa2, 0xa1, 0xa0,
            0xaf, 0xae, 0xad, 0xac, 0xab, 0xaa, 0xa9, 0xa8,
            0xb7, 0xb6, 0xb5, 0xb4, 0xb3, 0xb2, 0xb1, 0xb0,
            0xbf, 0xbe, 0xbd, 0xbc, 0xbb, 0xba, 0xb9, 0xb8,
            0xc7, 0xc6, 0xc5, 0xc4, 0xc3, 0xc2, 0xc1, 0xc0,
            0xcf, 0xce, 0xcd, 0xcc, 0xcb, 0xca, 0xc9, 0xc8,
            0xd7, 0xd6, 0xd5, 0xd4, 0xd3, 0xd2, 0xd1, 0xd0,
            0xdf, 0xde, 0xdd, 0xdc, 0xdb, 0xda, 0xd9, 0xd8,
            0xe7, 0xe6, 0xe5, 0xe4, 0xe3, 0xe2, 0xe1, 0xe0,
            0xef, 0xee, 0xed, 0xec, 0xeb, 0xea, 0xe9, 0xe8,
            0xf7, 0xf6, 0xf5, 0xf4, 0xf3, 0xf2, 0xf1, 0xf0,
            0xff, 0xfe, 0xfd, 0xfc, 0xfb, 0xfa, 0xf9, 0xf8,
        )))
        ciphertext = bytes(bytearray((
            0x4b, 0x8c, 0x4c, 0x98, 0x15, 0xf2, 0x4a, 0xea,
            0x1e, 0xc3, 0x57, 0x09, 0xb3, 0xbc, 0x2e, 0xd1,
            0xe0, 0xd1, 0xf2, 0x22, 0x65, 0x2d, 0x59, 0x18,
            0xf7, 0xdf, 0xfc, 0x80, 0x4b, 0xde, 0x5c, 0x68,
            0x46, 0x53, 0x75, 0x53, 0xa7, 0x46, 0x0d, 0xec,
            0x05, 0x1f, 0x1b, 0xd3, 0x0a, 0x63, 0x1a, 0xb7,
            0x78, 0xc4, 0x43, 0xe0, 0x5d, 0x3e, 0xa4, 0x0e,
            0x2d, 0x7e, 0x23, 0xa9, 0x1b, 0xc9, 0x02, 0xbc,
            0x21, 0x0c, 0x84, 0xcb, 0x0d, 0x0a, 0x07, 0xc8,
            0x7b, 0xd0, 0xfb, 0xb5, 0x1a, 0x14, 0x04, 0x5c,
            0xa2, 0x53, 0x97, 0x71, 0x2e, 0x5c, 0xc2, 0x8f,
            0x39, 0x3f, 0x6f, 0x52, 0xf2, 0x30, 0x26, 0x4e,
            0x8c, 0xe0, 0xd1, 0x01, 0x75, 0x6d, 0xdc, 0xd3,
            0x03, 0x79, 0x1e, 0xca, 0xd5, 0xc1, 0x0e, 0x12,
            0x53, 0x0a, 0x78, 0xe2, 0x0a, 0xb1, 0x1c, 0xea,
            0x3a, 0xf8, 0x55, 0xb9, 0x7c, 0xe1, 0x0b, 0xba,
            0xa0, 0xc8, 0x96, 0xeb, 0x50, 0x5a, 0xd3, 0x60,
            0x43, 0xa3, 0x0f, 0x98, 0xdb, 0xd9, 0x50, 0x6d,
            0x63, 0x91, 0xaf, 0x01, 0x40, 0xe9, 0x75, 0x5a,
            0x46, 0x5c, 0x1f, 0x19, 0x4a, 0x0b, 0x89, 0x9b,
            0xc4, 0xf6, 0xf8, 0xf5, 0x2f, 0x87, 0x3f, 0xfa,
            0x26, 0xd4, 0xf8, 0x25, 0xba, 0x1f, 0x98, 0x82,
            0xfc, 0x26, 0xaf, 0x2d, 0xc0, 0xf9, 0xc4, 0x58,
            0x49, 0xfa, 0x09, 0x80, 0x02, 0x62, 0xa4, 0x34,
            0x2d, 0xcb, 0x5a, 0x6b, 0xab, 0x61, 0x5d, 0x08,
            0xd4, 0x26, 0xe0, 0x08, 0x13, 0xd6, 0x2e, 0x02,
            0x2a, 0x37, 0xe8, 0xd0, 0xcf, 0x36, 0xf1, 0xc7,
            0xc0, 0x3f, 0x9b, 0x21, 0x60, 0xbd, 0x29, 0x2d,
            0x2e, 0x01, 0x48, 0x4e, 0xf8, 0x8f, 0x20, 0x16,
            0x8a, 0xbf, 0x82, 0xdc, 0x32, 0x7a, 0xa3, 0x18,
            0x69, 0xd1, 0x50, 0x59, 0x31, 0x91, 0xf2, 0x6c,
            0x5a, 0x5f, 0xca, 0x58, 0x9a, 0xb2, 0x2d, 0xb2,
        )))
        encrypted = ecb_encrypt(key, plaintext, sbox=sbox)
        self.assertSequenceEqual(encrypted, ciphertext)
        decrypted = ecb_decrypt(key, encrypted, sbox=sbox)
        self.assertSequenceEqual(decrypted, plaintext)

    def test_cryptopp(self):
        """Test vectors from Crypto++ 5.6.2
        """
        sbox = "AppliedCryptography"
        data = (
            (b"BE5EC2006CFF9DCF52354959F1FF0CBFE95061B5A648C10387069C25997C0672", b"0DF82802B741A292", b"07F9027DF7F7DF89"),
            (b"B385272AC8D72A5A8B344BC80363AC4D09BF58F41F540624CBCB8FDCF55307D7", b"1354EE9C0A11CD4C", b"4FB50536F960A7B1"),
            (b"AEE02F609A35660E4097E546FD3026B032CD107C7D459977ADF489BEF2652262", b"6693D492C4B0CC39", b"670034AC0FA811B5"),
            (b"320E9D8422165D58911DFC7D8BBB1F81B0ECD924023BF94D9DF7DCF7801240E0", b"99E2D13080928D79", b"8118FF9D3B3CFE7D"),
            (b"C9F703BBBFC63691BFA3B7B87EA8FD5E8E8EF384EF733F1A61AEF68C8FFA265F", b"D1E787749C72814C", b"A083826A790D3E0C"),
            (b"728FEE32F04B4C654AD7F607D71C660C2C2670D7C999713233149A1C0C17A1F0", b"D4C05323A4F7A7B5", b"4D1F2E6B0D9DE2CE"),
            (b"35FC96402209500FCFDEF5352D1ABB038FE33FC0D9D58512E56370B22BAA133B", b"8742D9A05F6A3AF6", b"2F3BB84879D11E52"),
            (b"D416F630BE65B7FE150656183370E07018234EE5DA3D89C4CE9152A03E5BFB77", b"F86506DA04E41CB8", b"96F0A5C77A04F5CE"),
        )
        for key, pt, ct in data:
            key = hexdec(key)
            pt = hexdec(pt)
            ct = hexdec(ct)
            self.assertSequenceEqual(ecb_encrypt(key, pt, sbox=sbox), ct)

    def test_cryptomanager(self):
        """Test vector from http://cryptomanager.com/tv.html
        """
        sbox = "id-GostR3411-94-TestParamSet"
        key = hexdec(b"75713134B60FEC45A607BB83AA3746AF4FF99DA6D1B53B5B1B402A1BAA030D1B")
        self.assertSequenceEqual(
            ecb_encrypt(key, hexdec(b"1122334455667788"), sbox=sbox),
            hexdec(b"03251E14F9D28ACB"),
        )


class CFBTest(TestCase):
    def test_cryptomanager(self):
        """Test vector from http://cryptomanager.com/tv.html
        """
        key = hexdec(b"75713134B60FEC45A607BB83AA3746AF4FF99DA6D1B53B5B1B402A1BAA030D1B")
        sbox = "id-GostR3411-94-TestParamSet"
        self.assertSequenceEqual(
            cfb_encrypt(
                key,
                hexdec(b"112233445566778899AABBCCDD800000"),
                iv=hexdec(b"0102030405060708"),
                sbox=sbox,
            ),
            hexdec(b"6EE84586DD2BCA0CAD3616940E164242"),
        )
        self.assertSequenceEqual(
            cfb_decrypt(
                key,
                hexdec(b"6EE84586DD2BCA0CAD3616940E164242"),
                iv=hexdec(b"0102030405060708"),
                sbox=sbox,
            ),
            hexdec(b"112233445566778899AABBCCDD800000"),
        )

    def test_steps(self):
        """Check step-by-step operation manually
        """
        key = urandom(KEYSIZE)
        iv = urandom(BLOCKSIZE)
        plaintext = urandom(20)
        ciphertext = cfb_encrypt(key, plaintext, iv)

        # First full block
        step = encrypt(DEFAULT_SBOX, key, block2ns(iv))
        step = strxor(plaintext[:8], ns2block(step))
        self.assertSequenceEqual(step, ciphertext[:8])

        # Second full block
        step = encrypt(DEFAULT_SBOX, key, block2ns(step))
        step = strxor(plaintext[8:16], ns2block(step))
        self.assertSequenceEqual(step, ciphertext[8:16])

        # Third non-full block
        step = encrypt(DEFAULT_SBOX, key, block2ns(step))
        step = strxor(plaintext[16:] + 4 * b"\x00", ns2block(step))
        self.assertSequenceEqual(step[:4], ciphertext[16:])

    def test_random(self):
        """Random data with various sizes
        """
        key = urandom(KEYSIZE)
        iv = urandom(BLOCKSIZE)
        for size in (5, 8, 16, 120):
            pt = urandom(size)
            self.assertSequenceEqual(
                cfb_decrypt(key, cfb_encrypt(key, pt, iv), iv),
                pt,
            )


class CTRTest(TestCase):
    def test_gcl(self):
        """Test vectors from libgcl3
        """
        sbox = "id-Gost28147-89-TestParamSet"
        key = hexdec(b"0475f6e05038fbfad2c7c390edb3ca3d1547124291ae1e8a2f79cd9ed2bcefbd")
        plaintext = bytes(bytearray((
            0x07, 0x06, 0x05, 0x04, 0x03, 0x02, 0x01, 0x00,
            0x0f, 0x0e, 0x0d, 0x0c, 0x0b, 0x0a, 0x09, 0x08,
            0x17, 0x16, 0x15, 0x14, 0x13, 0x12, 0x11, 0x10,
            0x1f, 0x1e, 0x1d, 0x1c, 0x1b, 0x1a, 0x19, 0x18,
            0x27, 0x26, 0x25, 0x24, 0x23, 0x22, 0x21, 0x20,
            0x2f, 0x2e, 0x2d, 0x2c, 0x2b, 0x2a, 0x29, 0x28,
            0x37, 0x36, 0x35, 0x34, 0x33, 0x32, 0x31, 0x30,
            0x3f, 0x3e, 0x3d, 0x3c, 0x3b, 0x3a, 0x39, 0x38,
            0x47, 0x46, 0x45, 0x44, 0x43, 0x42, 0x41, 0x40,
            0x4f, 0x4e, 0x4d, 0x4c, 0x4b, 0x4a, 0x49, 0x48,
            0x57, 0x56, 0x55, 0x54, 0x53, 0x52, 0x51, 0x50,
            0x5f, 0x5e, 0x5d, 0x5c, 0x5b, 0x5a, 0x59, 0x58,
            0x67, 0x66, 0x65, 0x64, 0x63, 0x62, 0x61, 0x60,
            0x6f, 0x6e, 0x6d, 0x6c, 0x6b, 0x6a, 0x69, 0x68,
            0x77, 0x76, 0x75, 0x74, 0x73, 0x72, 0x71, 0x70,
            0x7f, 0x7e, 0x7d, 0x7c, 0x7b, 0x7a, 0x79, 0x78,
            0x87, 0x86, 0x85, 0x84, 0x83, 0x82, 0x81, 0x80,
            0x8f, 0x8e, 0x8d, 0x8c, 0x8b, 0x8a, 0x89, 0x88,
            0x97, 0x96, 0x95, 0x94, 0x93, 0x92, 0x91, 0x90,
            0x9f, 0x9e, 0x9d, 0x9c, 0x9b, 0x9a, 0x99, 0x98,
            0xa7, 0xa6, 0xa5, 0xa4, 0xa3, 0xa2, 0xa1, 0xa0,
            0xaf, 0xae, 0xad, 0xac, 0xab, 0xaa, 0xa9, 0xa8,
            0xb7, 0xb6, 0xb5, 0xb4, 0xb3, 0xb2, 0xb1, 0xb0,
            0xbf, 0xbe, 0xbd, 0xbc, 0xbb, 0xba, 0xb9, 0xb8,
            0xc7, 0xc6, 0xc5, 0xc4, 0xc3, 0xc2, 0xc1, 0xc0,
            0xcf, 0xce, 0xcd, 0xcc, 0xcb, 0xca, 0xc9, 0xc8,
            0xd7, 0xd6, 0xd5, 0xd4, 0xd3, 0xd2, 0xd1, 0xd0,
            0xdf, 0xde, 0xdd, 0xdc, 0xdb, 0xda, 0xd9, 0xd8,
            0xe7, 0xe6, 0xe5, 0xe4, 0xe3, 0xe2, 0xe1, 0xe0,
            0xef, 0xee, 0xed, 0xec, 0xeb, 0xea, 0xe9, 0xe8,
            0xf7, 0xf6, 0xf5, 0xf4, 0xf3, 0xf2, 0xf1, 0xf0,
            0xff, 0xfe, 0xfd, 0xfc, 0xfb,
        )))
        ciphertext = bytes(bytearray((
            0x4a, 0x5e, 0x37, 0x6c, 0xa1, 0x12, 0xd3, 0x55,
            0x09, 0x13, 0x1a, 0x21, 0xac, 0xfb, 0xb2, 0x1e,
            0x8c, 0x24, 0x9b, 0x57, 0x20, 0x68, 0x46, 0xd5,
            0x23, 0x2a, 0x26, 0x35, 0x12, 0x56, 0x5c, 0x69,
            0x2a, 0x2f, 0xd1, 0xab, 0xbd, 0x45, 0xdc, 0x3a,
            0x1a, 0xa4, 0x57, 0x64, 0xd5, 0xe4, 0x69, 0x6d,
            0xb4, 0x8b, 0xf1, 0x54, 0x78, 0x3b, 0x10, 0x8f,
            0x7a, 0x4b, 0x32, 0xe0, 0xe8, 0x4c, 0xbf, 0x03,
            0x24, 0x37, 0x95, 0x6a, 0x55, 0xa8, 0xce, 0x6f,
            0x95, 0x62, 0x12, 0xf6, 0x79, 0xe6, 0xf0, 0x1b,
            0x86, 0xef, 0x36, 0x36, 0x05, 0xd8, 0x6f, 0x10,
            0xa1, 0x41, 0x05, 0x07, 0xf8, 0xfa, 0xa4, 0x0b,
            0x17, 0x2c, 0x71, 0xbc, 0x8b, 0xcb, 0xcf, 0x3d,
            0x74, 0x18, 0x32, 0x0b, 0x1c, 0xd2, 0x9e, 0x75,
            0xba, 0x3e, 0x61, 0xe1, 0x61, 0x96, 0xd0, 0xee,
            0x8f, 0xf2, 0x9a, 0x5e, 0xb7, 0x7a, 0x15, 0xaa,
            0x4e, 0x1e, 0x77, 0x7c, 0x99, 0xe1, 0x41, 0x13,
            0xf4, 0x60, 0x39, 0x46, 0x4c, 0x35, 0xde, 0x95,
            0xcc, 0x4f, 0xd5, 0xaf, 0xd1, 0x4d, 0x84, 0x1a,
            0x45, 0xc7, 0x2a, 0xf2, 0x2c, 0xc0, 0xb7, 0x94,
            0xa3, 0x08, 0xb9, 0x12, 0x96, 0xb5, 0x97, 0x99,
            0x3a, 0xb7, 0x0c, 0x14, 0x56, 0xb9, 0xcb, 0x49,
            0x44, 0xa9, 0x93, 0xa9, 0xfb, 0x19, 0x10, 0x8c,
            0x6a, 0x68, 0xe8, 0x7b, 0x06, 0x57, 0xf0, 0xef,
            0x88, 0x44, 0xa6, 0xd2, 0x98, 0xbe, 0xd4, 0x07,
            0x41, 0x37, 0x45, 0xa6, 0x71, 0x36, 0x76, 0x69,
            0x4b, 0x75, 0x15, 0x33, 0x90, 0x29, 0x6e, 0x33,
            0xcb, 0x96, 0x39, 0x78, 0x19, 0x2e, 0x96, 0xf3,
            0x49, 0x4c, 0x89, 0x3d, 0xa1, 0x86, 0x82, 0x00,
            0xce, 0xbd, 0x54, 0x29, 0x65, 0x00, 0x1d, 0x16,
            0x13, 0xc3, 0xfe, 0x1f, 0x8c, 0x55, 0x63, 0x09,
            0x1f, 0xcd, 0xd4, 0x28, 0xca,
        )))
        iv = b"\x02\x01\x01\x01\x01\x01\x01\x01"
        encrypted = cnt(key, plaintext, iv=iv, sbox=sbox)
        self.assertSequenceEqual(encrypted, ciphertext)
        decrypted = cnt(key, encrypted, iv=iv, sbox=sbox)
        self.assertSequenceEqual(decrypted, plaintext)

    def test_gcl2(self):
        """Test vectors 2 from libgcl3
        """
        sbox = "id-Gost28147-89-TestParamSet"
        key = hexdec(b"fc7ad2886f455b50d29008fa622b57d5c65b3c637202025799cadf0768519e8a")
        plaintext = bytes(bytearray((
            0x07, 0x06, 0x05, 0x04, 0x03, 0x02, 0x01, 0x00,
            0x0f, 0x0e, 0x0d, 0x0c, 0x0b, 0x0a, 0x09, 0x08,
            0x17, 0x16, 0x15, 0x14, 0x13, 0x12, 0x11, 0x10,
            0x1f, 0x1e, 0x1d, 0x1c, 0x1b, 0x1a, 0x19, 0x18,
            0x27, 0x26, 0x25, 0x24, 0x23, 0x22, 0x21, 0x20,
            0x2f, 0x2e, 0x2d, 0x2c, 0x2b, 0x2a, 0x29, 0x28,
            0xff, 0xfe, 0xfd, 0xfc, 0xfb,
        )))
        ciphertext = bytes(bytearray((
            0xd0, 0xbe, 0x60, 0x1a, 0x2c, 0xf1, 0x90, 0x26,
            0x9b, 0x7b, 0x23, 0xb4, 0xd2, 0xcc, 0xe1, 0x15,
            0xf6, 0x05, 0x57, 0x28, 0x88, 0x75, 0xeb, 0x1e,
            0xd3, 0x62, 0xdc, 0xda, 0x9b, 0x62, 0xee, 0x9a,
            0x57, 0x87, 0x8a, 0xf1, 0x82, 0x37, 0x9c, 0x7f,
            0x13, 0xcc, 0x55, 0x38, 0xb5, 0x63, 0x32, 0xc5,
            0x23, 0xa4, 0xcb, 0x7d, 0x51,
        )))
        iv = BLOCKSIZE * b"\x00"
        encrypted = cnt(key, plaintext, iv=iv, sbox=sbox)
        self.assertSequenceEqual(encrypted, ciphertext)
        decrypted = cnt(key, encrypted, iv=iv, sbox=sbox)
        self.assertSequenceEqual(decrypted, plaintext)


class CBCTest(TestCase):
    def test_pad_requirement(self):
        key = KEYSIZE * b"x"
        for s in (b"", b"foo", b"foobarbaz"):
            with self.assertRaises(ValueError):
                cbc_encrypt(key, s, pad=False)
            with self.assertRaises(ValueError):
                cbc_decrypt(key, s, pad=False)

    def test_passes(self):
        iv = urandom(BLOCKSIZE)
        key = KEYSIZE * b"x"
        for pt in (b"foo", b"foobarba", b"foobarbaz", 16 * b"x"):
            ct = cbc_encrypt(key, pt, iv)
            dt = cbc_decrypt(key, ct)
            self.assertSequenceEqual(pt, dt)

    def test_iv_existence_check(self):
        key = KEYSIZE * b"x"
        with self.assertRaises(ValueError):
            cbc_decrypt(key, BLOCKSIZE * b"x")
        iv = urandom(BLOCKSIZE)
        cbc_decrypt(key, cbc_encrypt(key, BLOCKSIZE * b"x", iv))

    def test_meshing(self):
        pt = urandom(MESH_MAX_DATA * 3)
        key = urandom(KEYSIZE)
        ct = cbc_encrypt(key, pt)
        dt = cbc_decrypt(key, ct)
        self.assertSequenceEqual(pt, dt)


class CFBMeshingTest(TestCase):
    def setUp(self):
        self.key = urandom(KEYSIZE)
        self.iv = urandom(BLOCKSIZE)

    def test_single(self):
        pt = b"\x00"
        ct = cfb_encrypt(self.key, pt, mesh=True)
        dec = cfb_decrypt(self.key, ct, mesh=True)
        self.assertSequenceEqual(pt, dec)

    def test_short(self):
        pt = urandom(MESH_MAX_DATA - 1)
        ct = cfb_encrypt(self.key, pt, mesh=True)
        dec = cfb_decrypt(self.key, ct, mesh=True)
        dec_plain = cfb_decrypt(self.key, ct)
        self.assertSequenceEqual(pt, dec)
        self.assertSequenceEqual(pt, dec_plain)

    def test_short_iv(self):
        pt = urandom(MESH_MAX_DATA - 1)
        ct = cfb_encrypt(self.key, pt, iv=self.iv, mesh=True)
        dec = cfb_decrypt(self.key, ct, iv=self.iv, mesh=True)
        dec_plain = cfb_decrypt(self.key, ct, iv=self.iv)
        self.assertSequenceEqual(pt, dec)
        self.assertSequenceEqual(pt, dec_plain)

    def test_longer_iv(self):
        pt = urandom(MESH_MAX_DATA * 3)
        ct = cfb_encrypt(self.key, pt, iv=self.iv, mesh=True)
        dec = cfb_decrypt(self.key, ct, iv=self.iv, mesh=True)
        dec_plain = cfb_decrypt(self.key, ct, iv=self.iv)
        self.assertSequenceEqual(pt, dec)
        self.assertNotEqual(pt, dec_plain)
