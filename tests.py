from PaddingOracle import PaddingOracle, PaddingOracleError

KEY = "DEADBEEFPOTATATO"
server = PaddingOracle(KEY)
encrypted_message = server.encrypt("ham", "burr", "I like cats")
ret_code = server.decrypt("ham", "burr", encrypted_message)
if ret_code is not PaddingOracle.DecryptBehavior.VALID_VALIDATION:
    raise PaddingOracleError("Should be valid validation")
ret_code = server.decrypt("ham", "urr", encrypted_message)
if ret_code is not PaddingOracle.DecryptBehavior.INVALID_VALIDATION:
    raise PaddingOracleError("Should be invalid validation")
