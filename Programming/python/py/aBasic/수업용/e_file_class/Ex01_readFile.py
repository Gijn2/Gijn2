"""
Stream : 데이터가 지나가는 가상의 통로
Stream을 열면 반드시 닫아줘야한다.
@ 파일 읽고 쓰기
    - 파일을 읽고 쓰기 전에 파일을 열어야 한다
    - fileObj = open ( filename, mode )
            mode 첫번째 글자 - 작업 표시
            r(read)   : 파일 읽기
            w(write)  : 파일 쓰기 ( 파일이 없으면 생성하고 파일이 있으면 덮어쓴다 )
            x(write)  : 파일 쓰기 ( 파일이 없을 때만 생성하고 쓴다 )
            a(append) : 파일 추가 ( 파일이 있으면 파일의 끝에서부터 추가하여 쓴다 )

            mode 두번째 글자 - 파일 타입
            t : 텍스트(text) 타입 ( 기본값 )
            b : 이진(binary) 타입 (ex. 이미지 등의 파일)
            두번째 글자가 없으면 텍스트 타입이다.

            encoding='utf-8' : 한글

    - 파일을 열고 사용 후에는 반드시 닫아야 한다
"""

#  파일 열기 1번 표현
"""
try:    # 파일을 찾고싶은 데 예외가 발생해서 try/catch로 씌워주어 확인
    f = open('./data/data.txt','r',encoding='utf-8') #Stream open , 'r' 부분을 기술하지 않을 경우 default = t,
except FileNotFoundError as e:
    print('파일을 못 찾음 : ',e) # 오류
else:
    #pass      #빈 공간 표현
    while True:
        line = f.readline() # 반복문으로 - true: 한 줄 씩 읽기
        if not line:        # 라인이 없다면 : false + not = true -> break
            break
        print(line,end='')  # 자체로 개행이 있어서 ,end=~ 로 없애기.
    f.close()               # 문제가 없으면 파일을 닫게 끔
finally:
    print('종료')
"""
#  파일 열기 2번 표현
"""
# 자동으로 파일 닫기 - with 이용
with open('./data/data.txt', 'r', encoding='utf-8') as f:
    while True:
        line = f.readline()  # 반복문으로 - true: 한 줄 씩 읽기
        if not line:         # 라인이 없다면 : false + not = true -> break
            break
        print(line, end='')
"""
#  파일 열기 3번 표현
filename = './data/data.txt'                            # filename 에 파일경로 지정
try:
    with open(filename,'rt',encoding='utf-8') as f:     # filename 을 open하고 f라는 별칭 부여
        content = f.read()                              # f 를 읽고 그 내용을 content에 저장
        print('=' * 100)
        print(content,end='')                           # content 출력 및 자동개행 방지
        print('='*100)
        words = content.split()                         # content의 내용 split
        print(words)
        print('=' * 100)
        num = len(words)                                # content의 단어 수 세기
except Exception as e:
    print('예외 발생',e)
else:
    print('파일명 :',filename,', 총 단어 수:',num)