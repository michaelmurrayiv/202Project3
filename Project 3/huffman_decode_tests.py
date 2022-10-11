import unittest
import filecmp
from huffman import *
import subprocess


class TestList(unittest.TestCase):
    def test_01a_test_file1_parse_header(self):
        """test the parse_header function"""
        f = open('file1_compressed_soln.txt', 'rb')
        header = f.readline()
        f.close()
        expected = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3,
                    0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 3, 2, 1, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0]
        self.compare_freq_counts(parse_header(header), expected)

    def test_01_test_file1_decode(self):
        """test the decode function using file1.txt"""
        huffman_decode("file1_compressed_soln.txt", "file1_decoded.txt")
        err = subprocess.call("FC /b file1.txt file1_decoded.txt", shell=True)
        self.assertEqual(err, 0)

    def compare_freq_counts(self, freq, exp):
        for i in range(256):
            stu = 'Frequency for ASCII ' + str(i) + ': ' + str(freq[i])
            ins = 'Frequency for ASCII ' + str(i) + ': ' + str(exp[i])
            self.assertEqual(stu, ins)

    def test_02_decode(self):
        """test the decode function on WAP.txt"""
        huffman_decode("file_WAP_out_compressed.txt", "decode_file.txt")
        err = subprocess.call("FC /b file_WAP.txt decode_file.txt", shell=True)
        self.assertEqual(err, 0)

    def test_03_decode(self):
        """test the decode function on declaration.txt"""
        huffman_decode("declaration_compressed_soln.txt", "declaration_decode.txt")
        err = subprocess.call("FC /b declaration.txt declaration_decode.txt", shell=True)
        self.assertEqual(err, 0)

    def test_04_decode(self):
        """test teh decode function on multiline.txt"""
        huffman_decode("multiline_compressed_soln.txt", "multiline_decode.txt")
        err = subprocess.call("FC /b multiline.txt multiline_decode.txt", shell=True)
        self.assertEqual(err, 0)

    def test_05_decode(self):
        """test the decode function on a one-letter file"""
        huffman_decode("one_letter_out_compressed.txt", "one_letter_decode.txt")
        err = subprocess.call("FC /b one_letter.txt one_letter_decode.txt", shell = True)
        self.assertEqual(err, 0)

    def test_06_decode(self):
        """test the decode function on an empty file"""
        huffman_decode("empty_file.txt", "empty_decode.txt")
        err = subprocess.call("FC /b empty_file.txt empty_decode.txt", shell = True)
        self.assertEqual(err, 0)


if __name__ == '__main__':
    unittest.main()
