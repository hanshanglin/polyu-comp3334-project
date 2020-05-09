import base64

__ENCODE__CHARSET__="UTF-16"
def b64_encode(s):
    b=s.encode(__ENCODE__CHARSET__)
    e=base64.b64encode(b)
    return e.decode("ascii")

def b64_decode(s):
    b=s.encode("ascii")
    e=base64.b64decode(b)
    return e.decode(__ENCODE__CHARSET__)

if __name__=="__main__":
    assert("啥"==b64_decode(b64_encode("啥")))
