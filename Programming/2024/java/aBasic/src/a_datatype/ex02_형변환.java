package a_datatype;

public class ex02_형변환 {

	public static void main(String[] args) {

		//**** 기본형
		// 변수의 자료형과 값이 일치

		int su;
		su = '문';
		System.out.println(su);

		double d;
		d = 1000;
		System.out.println(d);
		
		int su2;
		su2 = 1;
// 1.2를 int에 넣으면 공간은 4b인데 넣는거는 8b
// 주석 한번에 만들기 드래그 후 ctrl+/
		float f;
		f = 1.2F;		// 4B 변수에 8B 값을 넣고자 하는 상황에 F를 넣어 해결
System.out.println(f);

long big;
big = 1000000000000L;		//long형은 기본적으로 int이므로 큰 수 뒤에 L을 붙혀준다
System.out.println(big);




//코드 줄맞춤 -> ctrl+a >> ctrl+i



//*******기본형******
//변수의 자료형과 값이 일치
//크기가 큰 자료형에 작은 값 넣기 (자동형변환)
/* 크기가 작은 자료형에 큰 값을 넣을 경우,
	ㄴ 에러발생 -> 형변환 필요(= casting)
*/ 


int z;
z = (int)1.6;
System.out.println(z);
// 괄호를 사용하여 캐스팅을 해준다

char a;
a = 'a';
// 문자형 안에 ''는 한 단어만 "" 두개이상의 단어
// 

	}

}





