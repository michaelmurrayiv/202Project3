import unittest
import filecmp
import subprocess
from ordered_list import *
from huffman import *


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


    """test cases that didn't work in the first submission"""
    def test_09_empty_file(self):
        huffman_encode("empty_file.txt", "empty_out.txt")
        err = subprocess.call("FC empty_out.txt empty_soln.txt", shell=True)
        self.assertEqual(err, 0)

    def test_10_single_character(self):
        huffman_decode("single_out.txt", "single_char_decoded.txt")
        err = subprocess.call("FC single_in.txt single_char_decoded.txt", shell=True)
        self.assertEqual(err, 0)

    def test_09_textfile(self):
        huffman_encode("empty_file.txt", "empty_out.txt")
        err = subprocess.call("FC empty_out.txt empty_soln.txt", shell=True)
        self.assertEqual(err, 0)


if __name__ == '__main__':
    unittest.main()
