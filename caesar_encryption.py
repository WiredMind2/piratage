def crypt(mot,cle,encrypt=True):
    alphabet = list("abcdefghijklmnopqrstuvwxyz -.!?/éèà()")

    out = []
    for i,c in enumerate(mot):
            cle_index = alphabet.index(cle[i%len(cle)].lower())
            mot_index = alphabet.index(c.lower())
            if encrypt:
                    index_out = mot_index - cle_index
            else:
                    index_out = mot_index + cle_index
            out.append(alphabet[index_out%len(alphabet)])
    return ''.join(out)

alphabet = list("abcdefghijklmnopqrstuvwxyz -.!?/éèà()")

def crypt2(mot,cle,encrypt=True):
    return ''.join([alphabet[(alphabet.index(c.lower()) + alphabet.index(cle[i%len(cle)].lower()) * -1 if encrypt else 1)%len(alphabet)] for i,c in enumerate(mot)])


mot = input("Text: ")
cle = input("Cle: ")
encrypted = crypt(mot,cle)
print("Encrypted:",encrypted)
decrypted = crypt(encrypted,cle,False)
print("Decrypted:",decrypted)
