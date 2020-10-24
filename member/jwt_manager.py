import jwt

SECRET_KEY = "SE7540"
ALGORITHM = "HS256"

def encode_jason_to_jwt(data) :
    jwt_token = jwt.encode(data,SECRET_KEY, ALGORITHM)
    return jwt_token.decode("utf-8") 

def decode_jwt_to_dic(jwt_token) :
    dic = jwt.decode(jwt_token,SECRET_KEY, ALGORITHM)
    return dic

def get_authoritiy_info(cookie) :
    if 'jwt' in cookie:
        jwt_token = cookie.get('jwt')
        dic = jwt.decode(jwt_token,SECRET_KEY, ALGORITHM)
        return dic.authority
    else:
        return 0

def get_member_info(cookie) :
    print(cookie)
    if 'jwt' in cookie:
        jwt_token = cookie.get('jwt')
        dic = jwt.decode(jwt_token,SECRET_KEY, ALGORITHM)
        return dic
    else:
        return None
