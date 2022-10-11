from ordered_list import *
from huffman_bit_writer import *
from huffman_bit_reader import *


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char  # stored as an integer - the ASCII character code value
        self.freq = freq  # the frequency associated with the node
        self.left = None  # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right

    def __eq__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        return type(other) == HuffmanNode and self.freq == other.freq and self.char == other.char

    def __lt__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        if self.freq == other.freq:
            return self.char < other.char
        return self.freq < other.freq


def cnt_freq(filename):
    '''Opens a text file with a given file name (passed as a string) and counts the 
    frequency of occurrences of all the characters within that file'''
    my_file = open(filename, 'r')
    read_file = my_file.read()
    res_list = [0] * 256
    # goes through each character and accounts for it in the result list
    for char in read_file:
        index = ord(char)
        res_list[index] += 1
    my_file.close()

    return res_list


def create_huff_tree(char_freq):
    '''Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree'''

    huff_tree = OrderedList()

    # create the ordered list of all huffman nodes
    for i in range(len(char_freq)):
        if char_freq[i] != 0:
            huff_tree.add(HuffmanNode(i, char_freq[i]))

    if huff_tree.is_empty():  # deal with case when there are no entries in the list of occurrences
        return None

    # organize huffman nodes into the huffman tree using the rules
    while huff_tree.size() > 1:
        lowest = huff_tree.pop(0)
        second_lowest = huff_tree.pop(0)
        if lowest.char < second_lowest.char:  # the new node takes on the character with the smaller ASCII value
            new_node = HuffmanNode(lowest.char, lowest.freq + second_lowest.freq)
        else:
            new_node = HuffmanNode(second_lowest.char, lowest.freq + second_lowest.freq)
        new_node.left = lowest
        new_node.right = second_lowest
        huff_tree.add(new_node)

    return huff_tree.dummy.next.item


def create_code(node):
    '''Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation 
    as the index into the array, with the resulting Huffman code for that character stored at that location'''
    huff_strings = [''] * 256

    huff_tree_rec_map(node, huff_strings)  # call the recursive method that iterates through the Huffman
    # tree and adds the Huffman codes to the array
    return huff_strings


def create_header(freqs):
    '''Input is the list of frequencies. Creates and returns a header for the output file
    Example: For the frequency list associated with "aaabbbbcc, would return “97 3 98 4 99 2” '''
    result = ''
    for i in range(256):
        if freqs[i] != 0:
            if result == '':  # need to add an extra space only after the first number has been added
                result = result + str(i) + ' ' + str(freqs[i])
            else:
                result = result + ' ' + str(i) + ' ' + str(freqs[i])

    return result


def huffman_encode(in_file, out_file):
    '''Takes input file name and output file name as parameters - both files will have .txt extensions
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Also creates a second output file which adds _compressed before the .txt extension to the name of the file.
    This second file is actually compressed by writing individual 0 and 1 bits to the file using the utility methods
    provided in the huffman_bits_io module to write both the header and bits.
    Take note of special cases - empty file and file with only one unique character'''

    char_freq = cnt_freq(in_file)
    my_huff = create_huff_tree(char_freq)
    huff_codes = create_code(my_huff)



    file = open(in_file, 'r')
    read_file = file.read()
    binary_string = []

    # write the uncompressed output file
    output_file = open(out_file, 'w')
    if read_file == '': # accounts for an empty file
        output_file.close()
        file.close()
        return
    if len(create_header(char_freq).split()) == 2:  # accounts for file with one character
        output_file.close()
        file.close()
        return

    output_file.write(create_header(char_freq))
    output_file.write('\n')

    # for each character in the file, get the huffman code for it and add that code to the binary string
    for char in read_file:
        code = str(huff_codes[ord(char)])
        binary_string.append(code)
    binary_str = ''.join(binary_string)

    output_file.write(binary_str)

    # write the compressed output file
    compressed_output = out_file.replace('.txt', '_compressed.txt')
    my_compressed = HuffmanBitWriter(compressed_output)

    my_compressed.write_str(create_header(char_freq))
    my_compressed.write_str('\n')
    my_compressed.write_code(binary_str)

    my_compressed.close()
    output_file.close()
    file.close()


def huff_tree_rec_map(node, huff_strings, code=''):
    """recursive function that traverses the huffman tree and calculates the binary sequence for each character"""
    if node is None:
        return
    if node.left is None and node.right is None:
        huff_strings[node.char] = code
        return huff_strings

    huff_tree_rec_map(node.left, huff_strings, code + '0')
    huff_tree_rec_map(node.right, huff_strings, code + '1')


def huffman_decode(encoded_file, decode_file):
    """reads an encoded text file and decodes the text to the decode_file."""
    read_encode = HuffmanBitReader(encoded_file)
    header_str = read_encode.read_str()

    freq_list = parse_header(header_str)  # determine how many of each character is in the file
    my_huff = create_huff_tree(freq_list)  # create the huffman tree for the characters
    ptr = my_huff
    output_file = open(decode_file, 'w')

    total_char = 0
    for e in freq_list:
        if e !=0:
            total_char += 1

    if total_char == 1:
        for e in freq_list:
            if e != 0:
                for i in range(e):
                    output_file.write(chr(my_huff.char))
    else:
        codes = create_code(my_huff)
        length = 0

        for i in range(len(freq_list)):
            if freq_list[i] != 0:
                length += freq_list[i] * len(codes[i])

        for l in range(length):
            if read_encode.read_bit():  # if the bit is true, traverse to the right child
                ptr = ptr.right
            else:  # if the bit is false, traverse to the left node
                ptr = ptr.left
            if ptr.right is None and ptr.left is None:  # if the bit has reached a leaf, append character
                output_file.write(chr(ptr.char))
                ptr = my_huff

    read_encode.close()
    output_file.close()


def parse_header(header_string):
    """function that takes in the header string of an encoded file and returns a list of character frequencies"""
    freq_list = [0] * 256
    header_list = header_string.split()
    header_list = [e.decode('utf-8') for e in header_list]
    header_list = [int(s) for s in header_list]
    for i in range(0, len(header_list) - 1, 2):
        if i % 2 == 0:
            freq_list[header_list[i]] = header_list[i + 1]
    return freq_list

