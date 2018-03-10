import http.client,urllib

def get_asset_info

# header = {"API-Key" : "51sbj7/IwiqrwNJ03yDTPJZJ41AWskTMXih/iwgRJV8Ihp3OLSmA302C",
#           }

conn = http.client.HTTPSConnection("api.kraken.com", port=http.client.HTTPS_PORT)
conn.request('GET', '/0/public/Ticker?pair=XBT/USD')
resp = conn.getresponse()
print(resp.status, resp.reason)
data = resp.read()
print(data)
