package b_operator;

public class Ex02_non {
	public static void main(String[] args) {

		/* 결과를 반대로 하는 연산자
	 - 일반논리 : !
	 - 이진논리 : ~
		 */


		// 일반논리 NOT
		boolean result = 3 < 4;
		System.out.println(result);  // true
		System.out.println(!result); // false


		//이진논리 NOT 	** 버려도된다.
		int a = 15;			 	 //  int = 4byte
		System.out.println(a);   	 //  0000000 0000000 0000000 0000011
		System.out.println(~a);  	 //  1111111 1111111 1111111 1111100

		






	}


}
