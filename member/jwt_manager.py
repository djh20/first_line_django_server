import jwt

SECRET_KEY = "SE7540"
ALGORITHM = "HS256"

def encode_jason_to_jwt(data) :
    jwt_token = jwt.encode(data,SECRET_KEY, ALGORITHM)
    return jwt_token.decode("utf-8") 

def decode_jwt_to_dic(data) :
    dic = jwt.decode(data,SECRET_KEY, ALGORITHM)
    return dic