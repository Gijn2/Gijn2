package a_datatype;

// 한 줄 주석

/*
 * 	여러줄
 * 	주석
 */

/**
 * 여러줄 주석 , 설명문 주석
 */

/*
  	변수 명 규칙(명명규칙)
   			- 문자 + 숫자 + _ + ($) 달러는 가능하나 쓰지않을 예정
 			- BUT 첫 글자로 숫자는 안된다.
 			- 길이 제한 없음.
 			- 대소문자 구별 엄격함 중요
 
 			- 명명 권장사항
 				- package - folder / 패키지명은 전부 다 소문자
 				- 클래스명은 첫글자만 대문자 + 영단어의 첫글자는 대문자
 					ex) 귀여운 개를 목욕시키는 클래스 생성하려한다 -> CuteDogBath
 														-> 낙타 표기법 (camel case)
 				- 함수/변수명 첫글자는 소문자 + 영단어의 첫글자 대문자
 				ex) catBathAndFeed
 				
 				- 자바가 인식하는 단어를 변수명으로 사용할 수없다. -> 키워드는 안된다
 				
 */

public class Ex01_변수명 {

	public static void main(String[] args) { 
		
		// 변수선언 
		char chName;
		int i;
		int int1; 
		double abcd;
		boolean a;
		
		
		
		
		
		// 값 저장
		chName = '김'; // 문자형 ''
		i = 100;
		int1 = 1;
		abcd = 3.6;
		a = true;
				// true or false만 가능
		
		// 출력
		System.out.println(chName);
		System.out.println(i);
		System.out.println(abcd);
		System.out.println(a);



	}

}

/*
 	변수: 메모리상에 어떤 값을 저장하는 공간
 	
 	자료형 (data Type)
 	1. 기본형
 			논리형 (T/F): boolean
 			문자형		: char		*문자 하나만 가능
 			정수형		: int / long (그 외에는 잘 안씀, short/byte 등)
 			실수형		: double	 (float:4B)

 	2. 참조형		
 		- 배열/클래스
 	3.
 	
 	[참고]
 		1 bit -> 0 or 1
 		8 bit = 1 byte
 		
 		1024B = 1KB
 		1024KB
 		1024MB
 		1024GB
 		1024TB
 		......... 등드으으등등
 		
 		boolean - 1byte
 		 char - 2byte
 		 int - 4byte
 		 double - 8 byte
 		 
 	[참고] int : 4B
 		0 bit : 부호(0+ 1-)
 		31bit : 숫자표현
 		
 		-2(31) ~ +2(31)
 		-> max 21억
 		21억 이상은 int(4B)가 아닌 long(8B)을 사용해 표현
 		
 		
 		
 	- 메모리에 공간을 확보하는 것
		char xxxxxxx;(명명규칙) -> char chName;
		
		
*/

