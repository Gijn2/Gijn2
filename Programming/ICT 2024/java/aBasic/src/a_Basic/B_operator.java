package a_Basic;

import java.util.Scanner;		// 스캐너 사용할 때, 이거 꼭 선언해주기

public class B_operator {
	public static void main(String[] args) {

		// Chapter 1.증감연산자
		int a = 5; int b = 7;

		System.out.println(" A + 1 = " + (a+1) + ", B + 1 = " + (b+1)); // 6,8
		a = a + 1;
		b = b - 1; 
		System.out.println(a + "," + b);

		++a;
		--b;
		System.out.println(a+","+b);

		a++;
		b--;
		System.out.println(a+","+b);

		/* ***********************************
	 		증가연산자 ++   감소연산자 --
			앞뒤 둘 다 붙힐 수 있다.
			BUT 앞 뒤의 경우가 다르다.

			앞의 경우, ++을 먼저 하고서 값을 인출
			뒤의 경우, 기존값을 먼저 출력하고 ++ 진행
		 */

		int c = 10;
		int result = ++c;
		System.out.println(result);

		int d = 10;
		int result1 = d++;
		System.out.println(result1); // 기존값 10을 먼저 출력하고 지금 11이 된 상태

		d = d + 2; 				// 확인을 위한 +2
		System.out.println(d); // d++은 기존 d를 출력하고 +1을 해준다.

		int x = 5, y = 9;

		System.out.println("x'= " + ++x + ", y'= " + --y); // x6 y8
		System.out.println("x'= " + x++ + ", y'= " + y--); // x6 y8
		System.out.println("x''= " + x + ", y''= " + y); 	 // x7 y7

		if(x == 7) {
			x = x - 1;
			System.out.println("x=x-1 적용");
		}else {
			System.out.println("hi");  // 위에서 순서대로 진행되나봄. 계산할때마다 출력이 안되네
		}



		// Chapter 2. 부정
		/* 결과를 반대로 하는 연산자
			- 일반논리 : !
			- 이진논리 : ~
		*/

		// 일반논리 NOT
		boolean resulT = 3 < 4;
		System.out.println(resulT);  	// true
		System.out.println(!resulT);	// false
		
		//이진논리 NOT 	** 버려도된다.
		int ac = 15;			 	 		//  int = 4byte
		System.out.println(ac);   	 	//  0000000 0000000 0000000 0000011
		System.out.println(~ac);  	 	//  1111111 1111111 1111111 1111100



		// Chapter 3. 산술연산자
		// 산술연산자 + - / * %(나머지) 
		
		int ab = 3;
		
		if(ab%2 != 0) {					// 해석: a/2의 나머지 값이 0이 아니다.
			System.out.println("홀");
		}else {
			System.out.println("짝");
		}
		
		// Chapter 4. Shift
		// shift 연산자는 각각 비트의 값을 이동하는 연산자 ** 솔직히 쓸 일 없다고 하심
		// ex. 0010
		// 		ㄴ 오른쪽으로 쉬프트 = 0001, 왼쪽으로 쉬프트 0100

		int a1 = 4;			// 0100
		int b1 = a1 << 2;		// 1000, 오른쪽 쉬프트
		int c1 = a1 >> 1;		// 0010, 왼쪽  쉬프트
		
		System.out.println(a1+", "+b1+", "+c1);
		
		int d1 = a1 >>> 1;
		System.out.println(d1); // 옮긴 친구 무조건 양수 만들기?



		// Chapter 5. 비교연산자
		// >  >=  ==  <=  <  !=(같지않다)

		System.out.println("국어점수");			  //print(내부는 문장은 무조건 따옴표)
		Scanner input = new Scanner(System.in);		// 스캐너 오류? 대소문자 구문 철저히
		int ad = input.nextInt();					// int -> nextInt / Spring -> nextLine / float -> nextDouble

		System.out.println("수학점수");
		Scanner input1 = new Scanner(System.in);	// input 변수가 중복되지 않도록
		int bd = input1.nextInt();					// input1로 실수했을시, 잊지않고 변환

		System.out.println("영어점수");
		Scanner input2 = new Scanner(System.in);
		int cd = input2.nextInt();

		System.out.println("총점 = "+ (ad+bd+cd)); 	// 괄호 잊지 말기. 아니면 숫자 연속으로 표현함
		System.out.println("평균 = "+((ad+bd+cd)/3 ) );	

		// 정수가 아닌 소수점을 원한다면 double형 으로 바꾸고 진행
		int ave = ((ad + bd + cd)/3);

		if(ave >= 90) {
			System.out.println("A");			
		}else if(ave >= 70){
			System.out.println("B");
		}else if(ave >= 50) {
			System.out.println("C");
		}else {
			System.out.println("F");
		}



		// Chapter 6. 논리연산자
		/* 	정말 많이 쓰임 - 중요함

			논리연산자
			1. 일반논리
			표시: &&(and), ||(or)

		 	2.	이진논리
		 	표시: &		|		^

			A  	B		A&&B		A||B
			0(F)   0		0			 0
			0  	1		0			 1
			1  	0		0			 1
			1(T)	1		1			 1

			입력신호가 하나라도 들어오면 or
			입력신호가 모두 들어오면 and
		*/

		int ae = 75;
		char be = 'A';

		if(ae >= 80||be == 'A') {
			System.out.println("우등");
		}else {
			System.out.println("ㄲㅂ");
		}

		if(ae >= 80&&be == 'A') {
			System.out.println("우등");
		}else {
			System.out.println("ㄲㅂ");
		}




		// Chapter 7. 메인 함수(main function)
		int aa = 15;
		int ba = 10;
		
		int and = aa & ba;			
		/*  00001111
			00001010
			---------
			00001010	
			ㄴ and 이므로 두 수가 1인 것들만 걸러짐 다르면 0처리
		*/
		System.out.println(and);
		
		int or = aa | ba;
		/*	00001111
			00001010
			---------
			00001111
		
			답은 15
		*/
		System.out.println(or);
		
		int xor = aa^ba;
		System.out.println(xor); // xor : 두 신호가 다른경우에만 결과 발생
		
		/*  00001111
			00001010
			---------
			00000101
		
			답은 5
		*/



		// Chapter 8. short_Circuit_Logic
		// 일반논리연산자 대신 이진논리연산자를 사용한다면?
		
		int an =3;
		if(an>3 & ++an>3) {					
			System.out.println("조건 만족");
		} else {
			System.out.println("ㅈㄱ ㅂㅁㅈ");
		}	
		System.out.println(an); 				
		// 이진논리연산자를 사용하면 a값이 ++a 처리가 된다. -> a>3을 처리하고 ++a>3 처리
		
		if(an>1 | ++an>3) {
			System.out.println("조건 만족2");
		}
		System.out.println(an);
		/*
	 		숏서킷로직
	 		- 일반논리에서만 발생
	 		- 원리: 앞 조건에 의해 결과가 정해지면 뒤에 조건을 실행하지 않는다.
	 		- 자바에서만 이 개념을 가지고 있따

	 		일반논리 연산자
	 		
	 		
	 		if(a>3 && ++a>3) {					   // 조건입력 시, 먼저 입력된 조건 먼저 따지며 이미 결론을 내린다.
			System.out.println("조건 만족");		//먼저 주어진 조건에 부합하면 결과가 바로 도출되게하는 것이 숏서킷로직
			} else {
				System.out.println("ㅈㄱ ㅂㅁㅈ");
			}
		
				System.out.println(a); 				// 자바만 3이라고 결론이 난다. 다른 언어들은 결과값 4
										 			//	a, ++a 순서바꾸면 4로 출력								
		*/



		// Chapter 9. 삼항
		/*	항을 세 곳을 줘서 삼항
			1.조건 ?	2.참인 경우, 실행문:~	3.거짓인 경우, 실행문:~
		*/
		
		int s = 1;
		String results = (s > 8) ? "합격" : "불합격";
		System.out.println(results);
		
		//s의 값이 ()조건에 따라 ? 이후의 값 중 하나가 저장 a:b {a=T,b=F}
		Scanner in = new Scanner(System.in);
		System.out.println("점수 입력");
		
		int sc = in.nextInt();
		
		String results1 = (sc > 80)?"합":"불합";
		System.out.println(results1);
		
		// 두 수를 입력받아 a,b에 저장/ 두 수 중 더 큰 수를 출력
		/**
		Scanner in  = new Scanner(System.in);
		System.out.println("숫자1 입력");
		
		int n1 = in.nextInt();
		
		Scanner in1  = new Scanner(System.in);
		System.out.println("숫자2 입력");
		
		int n2 = in1.nextInt();
		
		int max = (n1>n2)?n1:n2;
		System.out.println("더 큰수 "+max);
		*/



		// Chapter 10. 대입
		int a2 = 10;
		int b2 = 7;
		
		// a=a+b;				// 덮어짐
		a2%=b2;					// 간략화, 사칙연산 모두 가능 ( +,-,/,*,% -> +=, -=, *=, /=, %=)
		System.out.println(a2);
		
		a2+=b2;						
		System.out.println(a2);
			
		a2-=b2;						
		System.out.println(a2);
			
		a2*=b2;						
		System.out.println(a2);
			
		a2/=b2;						
		System.out.println(a2);
		// +.17 -.3 /.1 *.70 %.3



		// Chapter 11. 문자열클래스
		/*
			자바에서 문자열을 처리하는 클래스
			- String, StringBuffer, StringBuilder
			- String 특권
				ㄴ new ~ 생략가능
				ㄴ + 연산가능 = 계속 문자를 연결가능
			- StringBuffer
			- StringBuilder
		 	  	ㄴ Buffer와 거의 동일하지만 접근속도에 따른 구별이 있다.
		 	  ex. '가'와 '나'가 동시에 접근하려하면 먼저 접근한 '가' 외의 '나'는 접근불가
		 	  #OSI7계층
		 	  
		 	  String과 그 외의 차이점
		 	  메모리로 접근해버려
		 	  ex. String의 경우, '1'을 저장할 때, 1번 메모리공간에 '1'을 저장. 후에
		 	  		'1+1은?'로 내용을 추가할 경우, 1번 메모리 공간을 비우고 2번 메모리 공간에 '1+1은?'저장
		 	  
		 	  글자(내용)의 변화가 심화면 StringBuffer/Builder
		 	  글자(내용)의 변화가 적으면 String
		 	  	ㄴString을 계속 쓰면 생기는 새로운 메모리 공간 외에 안쓰는공간은 자동수거된다.(쓰레기컬렉터가 이씀)
		 	  	ㄴ 쓰레기(Garbage): 사용중이지 않은 메모리공간을 칭하는 말 
			(중요!) 가비지컬렉터 & 가비지
		*/

		/**
			String a = "홍길동";
			System.out.println(a);
			
			String a1 = "홍길동2";
			
			StringBuilder b = new StringBuilder("김길동");
			System.out.println(b);
			
			// StringBuilder b2 = "김길동2";
			// 에러나옴. 유일하게 String만 생략이가능. Builder,Buffer는 앞에 new String~(""); 쳐줘야댐.

			
			String a2 = "홍길동3";
			a2 += "힘내"; // s3 = s3 + "힘내" 			// String 특권
			
			b.append("힘내");							// String 외의 문자 연결방법
		*/



		// Chapter 12. StringBufferSpeedMain
		/* 	String과 StringBuffer의 속도차이를 알아보기위한 예시
			결론: 자주 반복하는 부분은 StringBuffer 자주 반복 안하면 String이 좋다
		*/

		long startTime = 0L;
		long elapsedTime = 0L;

		//1. String으로 문자열 만들기의 속도 측정
		String str1 = ""; 
		startTime = System.currentTimeMillis(); 
		for(int i=0; i<50000; i++){
			str1 += "H"; 
		}
		elapsedTime = System.currentTimeMillis() - startTime;
		System.out.println("String 문자열만들기:" + elapsedTime);

		//2. StringBuffer로 문자열 만들기의 속도 측정
		StringBuffer sb = new StringBuffer(); 
		startTime = System.currentTimeMillis(); 
		for(int i=0; i<50000; i++){
			sb.append("H"); 
		}
		elapsedTime = System.currentTimeMillis() - startTime; 
		System.out.println("StringBuffer 문자열만들기:" + elapsedTime);
		


		// TEST
		/*
		학생점수를 입력받아 100만점 중 80~90사이라면 '평균', 
		1. 학생점수 변수 선언
		2. scanner
		3. 점수입력 문장출력
		4. 입력값을 학생점수 변수에 저장
		5. 입력값이 80보다 크고 90보다 작다면 '평균 출력'
		*/
		
		System.out.println("점수입력");

		Scanner inpuT = new Scanner(System.in);
		int score = inpuT.nextInt();
		
		if(score>100 || score <0) {
			System.out.println("잘못입력된 점수");
		}else if(score>80 & score<90) {
			System.out.println("평균");
		}else {
			System.out.println("평균아님");
		}
		
		/*
		String a = "점수";
		score>=80 & score<=90 ? a=="평균":a=="비평균" ;  
		*** 에러코드 = if else 문으로 바꿔라
		
		왜 이렇게는 안되는 걸까?
		
		-----------------------------------------------------------------
		[참고]
		파일을 읽기위해 컴파일이 필요
		java 버츄얼 머신
		
		코딩 실행시, f11만 누르면 디버깅모드가된다(오류잡는 용도)		
		*/


		// TEST 2: 문자하나를 입력받아서 그 문자가 대문자인지 소문자인지

		System.out.println("알파벳을 입력하세요");
		Scanner input12 = new Scanner(System.in);
		String b23 = input12.nextLine();
		int v = (int)b23.charAt(0);

		if(65 <= v && v <= 90) {
			System.out.println("대문자입니다.");
		} else {
			System.out.println("소문자입니다.");
		}
		
		/**
		 -> if구절을 char을 이용해 단어구문으로도 표현가능
		 char ch = str.charAt(0);
		 ...입력하세요..
		 if('A'<=ch & ch<='z'){
		 
		 } 로도 가능하다. 
		*/

		
		// TEST 3: 해당년도가 윤년인지 평년인지
		/**
		System.out.println("년도를 입력하세요");
		Scanner input2 = new Scanner(System.in);
		int c = input2.nextInt();
		int d = 0; // 일단 /4 윤년인 애들 집합
		if(c%4==0) {
			d = c;
		}else {
			System.out.println("평년");
		}
		if(d%100!=0) {
			System.out.println("윤년");
		}else if(d%400==0){
			System.out.println("윤년");
		}else {
			System.out.println("평년");
		}
		// 가능은 할 듯, 코드가 너무 길어진다
		*/
	
		System.out.println("연도를 입력하소");
		Scanner input3 = new Scanner(System.in);
		int e = input3.nextInt();
		
		if(e%4==0||(e%4==0 && e%400==0)) {
			System.out.println("윤년");
		}

	}
}
