package b_operator;

public class Ex08_short_Circuit_Logic {
	public static void main(String[] args) {

		// 일반논리연산자 대신 이진논리연산자를 사용한다면?
		
		int a =3;
			if(a>3 & ++a>3) {					
				System.out.println("조건 만족");
			} else {
				System.out.println("ㅈㄱ ㅂㅁㅈ");
			}
			
			System.out.println(a); 				
		// 이진논리연산자를 사용하면 a값이 ++a 처리가 된다. -> a>3을 처리하고 ++a>3 처리
		
		if(a>1 | ++a>3) {
			System.out.println("조건 만족2");
		}
		System.out.println(a);				


		/*
	 		숏서킷로직
	 		- 일반논리에서만 발생
	 		- 원리: 앞 조건에 의해 결과가 정해지면 뒤에 조건을 실행하지 않는다.
	 		- 자바에서만 이 개념을 가지고 있따

	 		일반논리 연산자
	 		
	 		
	 		if(a>3 && ++a>3) {					// 조건입력 시, 먼저 입력된 조건 먼저 따지며 이미 결론을 내린다.
			System.out.println("조건 만족");		//먼저 주어진 조건에 부합하면 결과가 바로 도출되게하는 것이 숏서킷로직
			} else {
				System.out.println("ㅈㄱ ㅂㅁㅈ");
			}
		
				System.out.println(a); 			// 자바만 3이라고 결론이 난다. 다른 언어들은 결과값 4
										 		//	a, ++a 순서바꾸면 4로 출력
										
		*/

	}
}
