"""
     1) 클래스 기초

     ` __init__ 함수 : 객체 초기화 함수( 생성자 역할 )
     ` self : 객체 자신을 가리킨다.

     [JAVA인 경우]
    class Sample {
        String data = "데이터";
        String name;
        Sample(String name){
            this.name;
        }
    }
    Samle s = new Sample("홍길동");
"""

class Sample :
    data = 'data'


    def __init__(self,name): #생성자 함수 만들기: name이라는 이름을 받아서 멤버변수 선언
        self.name = name
        print('__init__ 호출')

    def __del__(self):       # 소멸자 함수가 존재한다.
        print('__del__ 호출')

s = Sample('홍길동')   # 홍길동 저장
print(s.data)
print(s.name)


print(dir(s))         # 내부적으로 가지고있는 함수들을 출력해준다.
del s                 # 객체를 지울 때 쓰는 표현
"""
print(s.name)         # NameError: name 's' is not defined
"""
print('='*100)







"""
    2) 
    인스턴스 함수 :  'self'인 인스턴스를 인자로 받고 인스턴스 변수와 같이 하나의 인스턴스에만 한정된 데이터를 생성, 변경, 참조
    클래스   함수 :  'cls'인 클래스를 인자로 받고 모든 인스턴스가 공유하는 클래스 변수와 같은 데이터를 생성, 변경 또는 참조
     
    - 클래스 함수는 클래스명 접근
 
"""
class Book:
    cnt = 0
    def __init__(self,title):
        self.title = title
        self.cnt += 1
    def output(self):
       print('제목: ',self.title)
       print("총 개수: ",self.cnt)
    # Book class 안의 cnt 를 다른영역에 띄워서 공유하고싶다. -> JAVA라면 static 적용
    # python은 ...

    @classmethod
    def output2(cls):
        cls.cnt += 1
        print('2. 총 개수:',cls.cnt)

b1 = Book('행복이란')
b2 = Book('행복')
b3 = Book('먹고살자')

b1.output()
b2.output()
b3.output()
print('1>','-'*30)

b1.output2()
b2.output2()
b3.output2()
print('2>','-'*30)

print('='*100)
'''
     3) 클래스 상속
        - 파이션은 method overriding은 있지만 method overloading 개념은 없다
        - 파이션은 다중상속이 가능
        - 부모 클래스가 2개 이상인 경우 먼저 기술한 부모클래스에서 먼저 우선 해당 멤버를 찾음
'''

class Animal:
    def move(self):
        print('동물은 움직입니다.')

class Wolf(Animal): # python 에서 부모 자식 상속관계 : Animal 클래스 부모로 지정한 Wolf class
    def move(self): # Overriding
        print('늑대는 4발로 달린다.')

class Human(Animal): 
    def move(self):
        print('인간은 2발로 걸어요.')
        
# JAVA와의 차이점: python은 다중 상속이 가능하다.
class WolfHuman(Wolf,Human):
    def move(self):
        super().move()  # 먼저 입력한 상속함수의 것을 불러온다. ex. Wolf 이면 print 4~ / Human 이면 print 2~
        print('늑대인간은 2발로 달려요')

w = WolfHuman()
w.move()

