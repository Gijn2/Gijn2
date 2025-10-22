import json
f = open('./data/temp.json','r',encoding='utf-8')
data = f.read()
print(data,end='')
print('-'*100)
print(type(data))

result = json.loads(data) # data의 요소들을 객체로 올리는 작업
'''
print(items)
print(type(items))
'''
for key,item in result.items():
    print(key,'>',item)
    print(item['Job'])

f.close()