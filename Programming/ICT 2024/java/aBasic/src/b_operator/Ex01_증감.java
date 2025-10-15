package b_operator;

public class Ex01_증감 {
	public static void main(String[] args) {

		// *알림*      /** */를 떼주면 바로 돌릴 수 있다.


		/**
		int a = 5; int b = 7;

		System.out.println(" A + 1 = " + (a+1) + ", B + 1 = " + (b+1)); // 6,8
		a = a + 1;
		b = b - 1; 

		System.out.println(a + "," + b);

//************************************************

		++a;
		--b;
		System.out.println(a+","+b);

		a++;
		b--;
		System.out.println(a+","+b);

		 */


		/* ***********************************

	 		증가연산자 ++   감소연산자 --
			앞뒤 둘 다 붙힐 수 있다.
			BUT 앞 뒤의 경우가 다르다.

			앞의 경우, ++을 먼저 하고서 값을 인출
			뒤의 경우, 기존값을 먼저 출력하고 ++ 진행
		 */


		/**
		int c = 10;
		int result = ++c;
		System.out.println(result);

		int d = 10;
		int result1 = d++;
		System.out.println(result1); // 기존값 10을 먼저 출력하고 지금 11이 된 상태

		d = d + 2; 				// 확인을 위한 +2
		System.out.println(d); // d++은 기존 d를 출력하고 +1을 해준다.
		 */

		
		/**
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

		 */
		
		









	}
}
