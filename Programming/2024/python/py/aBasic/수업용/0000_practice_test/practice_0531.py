total_score = 0
with open('./txt/sample.txt','r',encoding='utf-8') as f:
    read_data = f.read()
    list_data = [int(data) for data in read_data.split()]

    with open('./txt/result.txt','wt',encoding='utf-8') as w:
        for i in range(len(list_data)):
            total_score += list_data[i]
            w.write(str(total_score))
            w.write('\n')
        w.write('총 점은{}, 평균은{}'.format(str(total_score),str(total_score / len(list_data))))

with open('./txt/dream.txt', 'wt', encoding='utf-8') as w:
    w.write("""나는 새로운 곳을 여행하는 꿈이 있습니다
새로운 사람들을 만나고
새로운 음식을 접하며
새로운 경험을 즐깁니다
새로운 느낌은 항상 나를 설레게 합니다 """)

with open('./txt/dream.txt', 'rt', encoding='utf-8') as r:
    re = r.read()
    result = re.split('\n')
    for idx,val in enumerate(result):
        print('{}--{}'.format(idx,val))


with open('./txt/dream.txt', 'rt', encoding='utf-8') as r:
    re = r.read()
    list_letter = [ x for x in re if x.strip()]
    total_words = re.split()
    total_lines = re.split('\n')
    print(f'총 글자 수는 : {len(list_letter)}, 총 단어의 수 : {len(total_words)}, 총 줄의 수 : {len(total_lines)}')