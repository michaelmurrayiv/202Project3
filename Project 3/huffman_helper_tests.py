import unittest
import filecmp
import subprocess
from ordered_list import *
from huffman import *

"""contains all my test cases used while testing the huffman encode and decode functions"""


class TestList(unittest.TestCase):
    def test_cnt_freq(self):
        """test the cnt_freq function for huffman encoding. """
        freqlist = cnt_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0]
        self.assertListEqual(freqlist[97:104], anslist)
        freqlist = cnt_freq("empty_file.txt")
        expected = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0]
        self.assertListEqual(freqlist, expected)

    def test_lt_and_eq(self):
        """tests the lt and eq definitions for a Huffman Node"""
        anslist = [2, 4, 8, 16, 0, 2, 0]
        ascii = 97
        lst = OrderedList()
        for freq in anslist:
            node = HuffmanNode(chr(ascii), freq)
            lst.add(node)
            ascii += 1
        self.assertEqual(lst.index(HuffmanNode('e', 0)), 0)
        self.assertEqual(lst.index(HuffmanNode('d', 16)), 6)
        self.assertEqual(lst.index(HuffmanNode('a', 2)), 2)
        self.assertFalse(HuffmanNode('a', 2) is None)

    def test_create_huff_tree(self):
        """tests the create_huff_tree function that turns an ordered list of HuffNodes into the final tree"""
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree.freq, 32)
        self.assertEqual(hufftree.char, 97)
        left = hufftree.left
        self.assertEqual(left.freq, 16)
        self.assertEqual(left.char, 97)
        right = hufftree.right
        self.assertEqual(right.freq, 16)
        self.assertEqual(right.char, 100)
        freqlist = cnt_freq("empty_file.txt")
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree, None)
        freqlist = cnt_freq("file4.txt")
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree.freq, 1)
        self.assertEqual(hufftree.char, 103)

    def test_create_header(self):
        """tests that the create_header function properly formats the headers for the compressed files"""
        freqlist = cnt_freq("file2.txt")
        self.assertEqual(create_header(freqlist), "97 2 98 4 99 8 100 16 102 2")

    def test_create_code(self):
        """tests that the create_code function creates the correct binary sequences for each character"""
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        self.assertEqual(codes[ord('d')], '1')
        self.assertEqual(codes[ord('a')], '0000')
        self.assertEqual(codes[ord('f')], '0001')

    def test_01_textfile(self):
        """tests the huffman_encode function when inputting file1.txt"""
        huffman_encode("file1.txt", "file1_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("FC /b file1_out.txt file1_soln.txt", shell=True)
        self.assertEqual(err, 0)
        err = subprocess.call("FC /b file1_out_compressed.txt file1_compressed_soln.txt", shell=True)
        self.assertEqual(err, 0)

    def test_02_textfile(self):
        """tests the huffman_encode function when inputting declaration.txt"""
        huffman_encode("declaration.txt", "declaration_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("FC /b declaration_out.txt declaration_soln.txt", shell=True)
        self.assertEqual(err, 0)
        err = subprocess.call("FC /b declaration_out_compressed.txt declaration_compressed_soln.txt", shell=True)
        self.assertEqual(err, 0)

    def test_03_textfile(self):
        """tests the huffman_encode function when inputting multiline.txt"""
        huffman_encode("multiline.txt", "multiline_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("FC /b multiline_out.txt multiline_soln.txt", shell=True)
        self.assertEqual(err, 0)
        err = subprocess.call("FC /b multiline_out_compressed.txt multiline_compressed_soln.txt", shell=True)
        self.assertEqual(err, 0)

    def test_04_textfile(self):
        """tests the huffman_encode function when inputting empty_file.txt"""
        huffman_encode("empty_file.txt", "empty_out.txt.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("FC /b empty_out.txt empty_soln.txt", shell=True)
        self.assertEqual(err, 0)

    def test_01a_test_file1_parse_header(self):
        """test the parse_header function"""
        f = open('file1_compressed_soln.txt', 'rb')
        header = f.readline()
        f.close()
        expected = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 3, 2, 1, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
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
        err = subprocess.call("FC /b one_letter.txt one_letter_decode.txt", shell=True)
        self.assertEqual(err, 0)

    def test_06_decode(self):
        """test the decode function on an empty file"""
        huffman_decode("empty_file.txt", "empty_decode.txt")
        err = subprocess.call("FC /b empty_file.txt empty_decode.txt", shell=True)
        self.assertEqual(err, 0)


if __name__ == '__main__':
    unittest.main()
