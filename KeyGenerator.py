import os
import Math
import string
import random
import PrimeNumber

#Files Path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#Key Generator
def generateKeys(keySize = 1024, log = False):
    # Generates an RSA key pair: a public key (n, e) and a private key (n, d).
    # Uses two large random prime numbers (p and q), where keySize defines their bit length.
    # If log is True, progress messages will be printed during generation.

    #1
    if log: print("Generating N")
    
    p, q = 0, 0

    while p == q:
        p = PrimeNumber.generateLargePrime(keySize)
        q = PrimeNumber.generateLargePrime(keySize)

    n = p * q

    #2
    if log: print("Generating E")

    pq = (p - 1) * (q - 1)
    e = random.randint(2 ** (keySize - 1), 2 ** (keySize))

    while Math.gcd(e, pq) != 1:
        e = random.randint(2 ** (keySize - 1), 2 ** (keySize))

    #3
    if log: print("Generating D")

    d = Math.findModInverse(e, pq)

    publicKey = (n, e)
    privateKey = (n, d)

    return publicKey, privateKey

def writeKeysToFile(keySize, publicKey, privateKey, fileName):
    # Saves the public and private keys to two separate text files in CSV format.
    # The filenames are based on the given fileName parameter.

    public_path = os.path.join(BASE_DIR, f"{fileName}_public.key")
    private_path = os.path.join(BASE_DIR, f"{fileName}_private.key")

    with open(public_path, 'w') as publicFile:
        publicFile.write(f"{keySize},{publicKey[0]},{publicKey[1]}")

    with open(private_path, 'w') as privateFile:
        privateFile.write(f"{keySize},{privateKey[0]},{privateKey[1]}")

    publicFile.close()
    privateFile.close()

#Encryption & Decryption
symbols = " " + string.punctuation + string.digits + string.ascii_letters
# The set of allowed characters in messages.
block_size = 16
# block_size defines how many characters are grouped into each encryption block.

def blockToString(blocks):
    # Converts the input string into a list of numeric blocks based on each character's index in the symbols list.
    # These blocks are used for RSA encryption.

    output = ""

    for block in blocks:
        while block:
            index = block % len(symbols)
            block = block // len(symbols)
            output += symbols[index]
        
    return output
    
def stringToBlock(plainText):
    # Converts a list of numeric blocks back into a readable text string using the symbols list.
    # Used to restore the decrypted message to its original form.

    output = []

    while plainText:
        block_number = 0
        block_string = None

        if len(plainText) >= block_size:
            block_string = plainText[0:block_size]
            plainText = plainText[block_size:]
        else:
            block_string = plainText
            plainText = ""

        for i in range(len(block_string)):
            index = symbols.find(block_string[i])
            block_number += (index * (len(symbols) ** i))
        
        output.append(block_number)

    return output

def encrypt(plainText, publickey, outputFile):
    # Encrypts the input plain text using the public key.
    # The text is first converted to numeric blocks, then each block is encrypted using RSA.
    # The resulting ciphertext blocks are saved to the output file as comma-separated values.

    plainBlocks = stringToBlock(plainText)
    cipherBlocks = []

    for block in plainBlocks:
        C = pow(block, publickey[1], publickey[0])
        cipherBlocks.append(str(C))

    output_path = os.path.join(BASE_DIR, outputFile)
    with open(output_path, 'w') as file:
        file.write(",".join(cipherBlocks))

def decrypt(encrypted_file, privatekey):
    # Decrypts the encrypted message using the private key.
    # Reads encrypted blocks from the input file, decrypts each block using RSA,
    # and reconstructs the original message from the decrypted blocks.

    encrypted_path = os.path.join(BASE_DIR, encrypted_file)
    with open(encrypted_path, 'r') as file:
        cipherBlocks = file.read()

    cipherBlocks = cipherBlocks.split(",")

    plainBlocks = []

    for block in cipherBlocks:
        M = pow(int(block), privatekey[1], privatekey[0])
        plainBlocks.append(M)

    return blockToString(plainBlocks)

def readKeysFromFile(fileName):
    # Reads the public and private RSA keys from their respective files using the given base file name.
    # Assumes the files were written using the writeKeysToFile function.

    public_path = os.path.join(BASE_DIR, f"{fileName}_public.key")
    private_path = os.path.join(BASE_DIR, f"{fileName}_private.key")

    with open(public_path, 'r') as publicFile:
        publicKey = publicFile.read()

    with open(private_path, 'r') as privateFile:
        privateKey = privateFile.read()

    publicKey = publicKey.split(",")
    publicKey = (int(publicKey[1]), int(publicKey[2]))

    privateKey = privateKey.split(",")
    privateKey = (int(privateKey[1]), int(privateKey[2]))
    
    return publicKey, privateKey

#BODY
if __name__ == "__main__":
    generateKey = input("Do you want Generate key or Encrypt/decrypt? (Enter G or E) : ").upper()

    if generateKey == "G":
        keySize = int(input("Keysize : "))
        fileName = input("Output file name : ")
        publicKey, privateKey = generateKeys(keySize, log = True)
        writeKeysToFile(keySize, publicKey, privateKey, fileName)

    elif generateKey == "E":
        op = input("Encrypt or Decrypt ? (Enter E or D) : ").upper()

        if op == "E":
            plainText = input("Your Message : ")
            keyFile = input("Key File Name : ")
            outputFile = input("Output File Name : ")
            public, private = readKeysFromFile(keyFile)
            encrypt(plainText, public, outputFile)

        elif op == "D":
            encryptedFile = input("Encrypted File Name : ")
            keyFile = input("Key File Name : ")
            public, private = readKeysFromFile(keyFile)
            print(decrypt(encryptedFile, private))