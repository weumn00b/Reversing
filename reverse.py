def decrypt(inputfile, outputfile, key=0x19):
   # Open the input file in binary
    with open(inputfile, 'rb') as input:
        # Read the file content
        data = input.read()
        
    # XOR to reverse the obfuscation
    decrypted_data = bytes([byte ^ key for byte in data])
        
    # opening the output file in binary
    with open(outputfile, 'wb') as output:
        output.write(decrypted_data)

# setting input and output files
inputfile = 'logs'
outputfile = 'decrypted_logs'  

decrypt(inputfile, outputfile)
