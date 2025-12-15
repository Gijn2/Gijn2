package a_datatype;

import java.util.Scanner;

// 한 줄 주석

/*
 * 	여러줄
 * 	주석
 */

/**
 * 여러줄 주석 (설명문)
 */

// 주석 한번에 만들기 드래그 후 ctrl+/
//코드 줄맞춤 -> ctrl+a >> ctrl+i

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

public class Ex01_데이터타입 {
	//class 생성할 때, 박스 체크를 안 했을 경우, main을 입력하고 ctrl+스페이스바 - 엔터(메인 메소드 생성)
	public static void main(String[] args) { 
		
		//Chpater1. 변수명
		// 변수선언 
		char chName;
		int i;
		double abcd;
		boolean a;
		
		// 값 저장
		chName = '김'; // 문자형 ''
		i = 100;
		abcd = 3.6;
		a = true;
				// true or false만 가능
		
		// 출력
		System.out.println(chName);
		System.out.println(i);
		System.out.println(abcd);
		System.out.println(a);



		/* Chapter2. 형변환

			기본형
			1. 변수의 자료형과 값이 일치
			2. 크기가 큰 자료형에 작은 값 넣기 (자동형변환)
			3. 크기가 작은 자료형에 큰 값을 넣을 경우,
				ㄴ 에러발생 -> 형변환 필요(= casting)
		*/ 

		int su;
		su = '문';
		System.out.println(su);

		double d;
		d = 1000;
		System.out.println(d);
		
		int su2;
		su2 = 1;					// 1.2를 int에 넣으면 공간은 4b인데 넣는거는 8b

		float f;
		f = 1.2F;					// 4B 변수에 8B 값을 넣고자 하는 상황에 F를 넣어 해결

		System.out.println(f);

		long big;
		big = 1000000000000L;		//long형은 기본적으로 int이므로 큰 수 뒤에 L을 붙혀준다
		System.out.println(big);

		int z;
		z = (int)1.6;
		System.out.println(z);		// 괄호를 사용하여 캐스팅을 해준다

		char b;
		b = 'b';					// 문자형 안에 ''는 한 단어만 "" 두개이상의 단어
		


		// Chapter 3. 변수 선언
		// (1) 변수 선언 + 값 대입
		int kor; 		// 정수형 변수 선언
		kor = 30;		// 값 저장 ** 설명과 코딩값이 자동으로 나올 수 있게 연습.

		// (2) 초기화: 변수선언 시, 값을 대입
		int eng = 30;		// 변수 입력 전에 초기값을 먼저 설정
		// (3) 변수가 여러개일 경우,
		int math = 30, java = 50;

		if(kor == java) {
			System.out.println("점수 동일");
		}else {
			System.out.println("점수 다름"); 
		} // 이 상태로 재생할 경우, 변수 값을 비교해 문자 출력
		/* [참고]
		 swap: 두 변수의 값을 바꾼다.

		 */
		int az = 10, bz = 20;
		System.out.println("A=" + a + "B=" + b + "입니다.");
		int temp = az; 											// 임시변수 temp를 지정해서 저장해야한다
		az = bz;												// 컴퓨터는 반드시 중간처리가 있어야댐
		bz = temp;
		System.out.println(az*bz+5);


		//Chapter 4. char
	char ch = 'A'; // 2 byte
	
	int id = 'A';   // 4 byte
	
	 System.out.println("문자는"+ id);
	// '문자는65'로 찍힌다 -> 고로 캐스팅처리
	 System.out.println((char)id);
	
	/**
	 1. 자바 언어 이전의 문자체제는 아스키코드 (ascii-code) 자바는 unicode
	 [asci-code] -- 1byte(2^8개 문자표현가능)
	 	영어 숫자 특수기호 등만 표현
	 
	 'A' = 0100(대문자) 0001(1번 = A) => 2^6 + 2^0 = 65 **위에 65가 찍힌 이유
	 'E' = 0100 0101 = 2^6 + 2^2 +2^0 = 69
	 
	 'a' = 0110(소문자) 0001(첫 영단어) => 이진법 계산은.. 64 32 1 = 97 
	 'b' = 0110 0010 => (생략)64 32 2 = 98
	 
	 [uni-code] -- 2Byte(2^16만큼의 문자표현)
	 asci-code에 더불어 일본어, 한국어 등 일부 다른 외국어들도 포함
	 - 표현 '/u0000'
	 
	 2. cmd 자바
	 */


	 /*	Chapter 5. String(참조형)
		
		데이터타입(자료형)
		1. 기본형(primitive)
			- 논리형: boolean
			- 문자형: char
			- 정수형: int/long
			- 실수형: double
		
		2. 참조형(reference): 클래스 / 배열
		-> new 키워드를 통해 메모리를 확보해야함(객체생성)
		[ex] 이름이 홍길동
			char a = '홍길동'; -> 오류
			char a = "홍길동"; -> 오류
			
			해결법: 변수 a,b,c -> '홍' '길' '동'
			
		[cf] 문자 1개 => char
			 문자열(0개이상) => string(클래스)
			
		사용처: 회원가입, 로그인 등
	*/
		
	String name;
	
	//메모리 확보(값지정) - 객체생성
	name = new String("홍씨");
		
	String irum = new String("홍씨");
	
	if(name == irum) {
		System.out.println("동일이름");
	}else {
		System.out.println("다른이름"); 			// 다른이름이 뜨는 이유: 변수 이름이 다르므로 다르게 인지
	}
	
	if(name.equals(irum)) {						  // **문자열 비교는 equals 함수를 이용해야만함
		System.out.println("동일이름2");
	}else {
		System.out.println("다른이름2");
	}
	
	/** Chapter 5-1. String Plus (중요)
		String class는 참조형이 맞다
		하지만 유일하게 new를 안써도 되게끔 만듬

		- 기본적인 참조형 작성법 -
		String hong = new String("홍길동");
		String gil = new String("홍길동");
	*/
	
	String hong = "홍길동";
	String gil  = "홍길동";
			
	if(hong.equals(gil)) {
		System.out.println("같은 상자");
	}else {
		System.out.println("다른 상자");
	}



	// Chapter 6. Scanner
	/*
		콘솔에 출력
			system.out
				' print()
				' println()
				' printf()
				
		콘솔에 입력
			system.in
		 	
		-> Scanner 이용	
		
		class 생성 시, Package 하단에 아래 문구를 입력하여 도구르 가져옴.
		import java.utill            
		import java.lang.*;

		문자열 입력시: next()/ nextLine() -> 두 명령어 차이점 ==> 과제
		정수형 입력시: nextInt
		실수형 입력시: nextDouble()
	
	*/
		
	System.out.println("첫번쨰 수를 입력하세요");
	Scanner input = new Scanner(System.in);
	int first = input.nextInt();
		
	System.out.println("두번쨰 수를 입력하세요");
	Scanner input1 = new Scanner(System.in);
	int second = input1.nextInt();
		
	int add = first + second;
	System.out.println("두 수의 합은 " + add);
	}

}