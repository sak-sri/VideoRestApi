import requests
BASE="http://127.0.0.1:5000/"

data=[{"name":"How to make soup","views":50000,"likes":5245},
{"name":"How to do yoga","views":30000,"likes":4512},
{"name":"How to make cake","views":10000,"likes":55},
{"name":"how to make milkshake","views":5000,"likes":245},
{"name":"how to make pasta","views":5000,"likes":525},
{"name":"How to make pizza","views":500000,"likes":50245}]

for i in range(len(data)):
    response=requests.put(BASE+"Video/"+str(i),data[i])
    print(response.json())

response=requests.get(BASE+"Video/2")
print(response.json())

response=requests.patch(BASE+"Video/3",{"views":330})
print(response.json())

response=requests.delete(BASE+"Video/3")
print(response)

response=requests.get(BASE+"Video/3")
print(response.json())