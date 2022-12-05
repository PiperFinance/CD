import requests
import base64




def decode_https_uri(uri: str):
    res = requests.get(uri)
    uri = res.json().get("image")
    res = requests.get(uri)
    uri = ("data:" + 
       res.headers['Content-Type'] + ";" +
       "base64," + base64.b64encode(res.content).decode("utf-8"))
    return uri

print(decode_https_uri("https://vivid.mypinata.cloud/ipfs/QmdJXNoTTzSkfdusFqidpYuDqDF6p7AMi7iZkmZpxPAByW/4813"))
