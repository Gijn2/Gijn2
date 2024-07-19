package b_operator;

public class Ex06_논리 {

	public static void main(String[] args) {

		/* *******정말 많이 쓰임 ***** 중요함 ****************
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

		int a = 75;
		char b = 'A';

		if(a >= 80||b == 'A') {
			System.out.println("우등");
		}else {
			System.out.println("ㄲㅂ");
		}


		int c = 75;
		char d = 'A';

		if(a >= 80&&b == 'A') {
			System.out.println("우등");
		}else {
			System.out.println("ㄲㅂ");
		}

		
		
		
		
		
	}
}
