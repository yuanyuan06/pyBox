import base64
open_icon = open("ooopic_1535094442.ico","rb")
b64str = base64.b64encode(open_icon.read())
print(b64str.decode('utf-8'))