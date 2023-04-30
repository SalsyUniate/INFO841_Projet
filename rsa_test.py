import rsa 

(public_key, private_key) = rsa.newkeys(512)
# print("public :")
# print(public_key)
# print("private :")
# print(private_key) 

print(public_key)

test = str(public_key)[10:-1].split(", ")
print(test)


# cree une liste avec la public key en bytes pour envoi
bytes_test = [str.encode(test[0]), str.encode(test[1])]
# for i in bytes_test :
#     print(type(i))
#     print(i)

# reconversion en public key classique...
float_test = [float(str(bytes_test[0])[2:-1]), float(str(bytes_test[1])[2:-1])]
print(float_test)
new_public_key = rsa.PublicKey(float_test[0], float_test[1])
print(new_public_key)
    