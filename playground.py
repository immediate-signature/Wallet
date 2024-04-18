import json
import script
import server

obj = script.filter_utxo(101)

print(type(obj))
print(obj)
print(obj[1])

jack = json.loads(obj)[1]

print(jack["txid"])