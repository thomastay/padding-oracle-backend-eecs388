from padding_oracle import PaddingOracle

KEY = "DEADBEEFPOTATATO"
server = PaddingOracle(KEY)
encrypted_message = server.encrypt("ham", "burr", "I like cats")
print(encrypted_message)
ret_code = server.decrypt("ham", "burr", encrypted_message)
print(ret_code)
