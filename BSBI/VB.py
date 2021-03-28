
def encode(n):
    bytess = []
    while True:
        bytess.insert(0, n % 128)
        if n < 128:
            break
        n //= 128
    bytess[-1] += 128
    return bytess


def decode(bytess):
    nums = []
    n = 0
    for idx in range(len(bytess)):
        if bytess[idx] < 128:
            n = 128 * n + bytess[idx]
        else:
            n = 128 * n + (bytess[idx] - 128)
            nums = n
            n = 0
    return nums


def intervals(in_docIDs):
    intervalss = []
    docIDs = list(in_docIDs)
    if type(docIDs[0]) == str:
        docIDs = list(map(int, docIDs))
    head = docIDs[0]
    if head > 0:
        intervalss.append(head)
    for doc_idx in range(len(docIDs) - 1):
        diff = docIDs[doc_idx + 1] - docIDs[doc_idx]
        intervalss.append(diff)
    return intervalss


def compress(source_path, destination_path, compress_fn=lambda x: [int(y) for y in x.split()]):
    source_file = open(source_path, "r")
    destination_file = open(destination_path, "wb")
    line = source_file.readline()
    output = b""
    while line:
        split_line = compress_fn(line)
        try:
            for token in split_line:
                encoded = encode(token)
                for byte in encoded:
                    output += (byte).to_bytes(1, "little")
            # print("Output:", output)
        except Exception as e:
            print(e, "in token: ", token)

        destination_file.write(output)
        output = b""
        line = source_file.readline()

    source_file.close()
    destination_file.close()


def decompress(source_path, destination_path, decompress_fn=lambda x: x):
    source_file = open(source_path, "rb")
    destination_file = open(destination_path, "w")
    byte = source_file.read(1)
    bytestream = []
    while byte:
        num = int.from_bytes(byte, "little")
        while not num & 128:
            bytestream.append(num)
            byte = source_file.read(1)
            num = int.from_bytes(byte, "little")
        bytestream.append(num)
        number = decode(bytestream)
        result = decompress_fn(number)
        # print("Decoded:", result)
        destination_file.write(str(result) + " ")
        bytestream = []
        byte = source_file.read(1)

    source_file.close()
    destination_file.close()

def compress_fn(line):
    result = [ord(c) for c in line]
    return result


def decompress_fn(ascii_num):
    return chr(ascii_num)


if __name__ == "__main__":
    source_path = "merged_blocks.dat"
    destination_path = "compressed.dat"
    decompressed_path = "decompressed.txt"

    compress(source_path, destination_path, compress_fn)
    decompress(destination_path, decompressed_path, decompress_fn)

