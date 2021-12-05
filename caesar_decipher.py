word = input("Text to decipher: ")

abc = "abcdefghijklmnopqrstuvwxyz"

for rank in range(len(abc)):
    out = ""
    for i,letter in enumerate(word):
        try:
            if i+rank >= len(abc):
                out += abc[i+rank-len(abc)]
            else:
                out += abc[i+rank]
        except:
            out += letter
    print(out)
            
