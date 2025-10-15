package b_operator;

public class Ex03_산술연산 {

	public static void main(String[] args) {
		
		/* ****************************
		 산술연산자 + - / * %(나머지) 
		 - 사칙연산은 패스
		 - 나머지 연산자 	** 나중에 자주 쓸 예정
		 */
		
		int a = 3;
		
		if(a%2 != 0) {					// 해석: a/2의 나머지 값이 0이 아니다.
			System.out.println("홀");
		}else {
			System.out.println("짝");
		}
		

	}

}
