# 개발자가 만드는 함수와 구별하기 위해 __ __로 앞 뒤 처리를해서 만듬
"""
    매직 메소드

(1) Binary Operators
        Operator	Method
        +	    object.__add__(self, other)
        -	    object.__sub__(self, other)
        *	    object.__mul__(self, other)
        //	    object.__floordiv__(self, other)
        /	    object.__div__(self, other)
        %	    object.__mod__(self, other)
        **	    object.__pow__(self, other[, modulo])
        >>	    object.__lshift__(self, other)
        <<	    object.__rshift__(self, other)
        &	    object.__and__(self, other)
        ^	    object.__xor__(self, other)
        |	    object.__or__(self, other)  
        
(2) Comparison Operators
        Operator	Method
        <	    object.__lt__(self, other)
        <=	    object.__le__(self, other)
        ==	    object.__eq__(self, other)
        !=	    object.__ne__(self, other)
        >=	    object.__ge__(self, other)
        >	    object.__gt__(self, other)
                
(3) Extended Assignments
        Operator	Method
        +=	    object.__iadd__(self, other)
        -=	    object.__isub__(self, other)
        *=	    object.__imul__(self, other)
        /=	    object.__idiv__(self, other)
        //=	    object.__ifloordiv__(self, other)
        %=	    object.__imod__(self, other)
        **=	    object.__ipow__(self, other[, modulo])
        <<=	    object.__ilshift__(self, other)
        >>=	    object.__irshift__(self, other)
        &=	    object.__iand__(self, other)
        ^=	    object.__ixor__(self, other)
        |=	    object.__ior__(self, other)
          
(4) Unary Operators
        Operator	Method
        -	        object.__neg__(self)
        +	        object.__pos__(self)
        abs()	    object.__abs__(self)
        ~	        object.__invert__(self)
        complex()	object.__complex__(self)
        int()	    object.__int__(self)
        long()	    object.__long__(self)
        float()	    object.__float__(self)
        oct()	    object.__oct__(self)        
        hex()	    object.__hex__(self)
"""

class Sample:
    def __init__(self,name,age): #__init__ 생성자MagicMethod
        self.name = name
        self.age = age
    def __str__(self):           # toString MagicMethod
        return '이름:{0}, 나이:{1} \n'.format(self.name,self.age)
    def __add__(self, other):    # 덧셈 Method
        self.age += other
    def __gt__(self, other):     # 비교연산 Method
        if self.age > other:
            return "어른이에요."
        else:
            return "아가에요"
    def __bool__(self):
        return self.name == '홍길동'
s = Sample(name='홍길자',age=22)

print(s) #toString 이 아닌 sample 객체라는 의미의 메세지 출력
s+10
print(s) # 당연히 객체 + int 형은 오류지만, __add__ method 추가 이후에 융통성있어짐.

print(s>20) # sample 과 비교연산자를 연결해주기 위해 __gt__ method 추가 (greater than)

if s:   # 홍길동 내용이 아닌 s 내의 값이 존재하면 true를 반환함.
    print('홍길동 본인')
else:
    print('나 홍길동 아니다')
