'''
data/sample.json 을 읽어서 총합을 구해서 출력
'''
import json

filename = './data/sample.json'

file = open(filename,'r',encoding='utf-8')
readResult = file.read()
print(readResult)

data = json.loads(readResult)

totalPrice = 0
totalCount = 0
for key, value in data.items():
    print(key,'&',value)
    totalPrice += int(value['price'])*int(value['count'])
    totalCount += int(value['count'])

print('총 개수: ',totalCount)
print('총 가격: ',totalPrice)