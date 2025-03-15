import bcrypt


def gen_salt():
    return bcrypt.gensalt()


def encrypt(password, salt):
    password = password.encode("utf-8")
    return bcrypt.hashpw(password, salt)


def check_pass(password, salt, hashedPass):
    password = encrypt(password, salt)
    if password == hashedPass:
        return True
    else:
        return False
