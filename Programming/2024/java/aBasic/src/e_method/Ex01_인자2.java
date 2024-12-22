package e_method;

public class Ex01_인자2 {
	public static void main(String[] args) {

		int a = 10, b = 20;
		method(a, b);						// method 함수로 이동
		// method 실행 후 이동
		System.out.println(a+" "+b);		// 10 20

	}
	// 메인 String 밖에 함수 생성해야해요
	static void method(int a, int b) {		// method 함수 실행 **함수 내 가상의 데이터 a, b
		a += b;
		System.out.println(a+" "+b);		// 30 20, 8번째 줄로 이동
	}										// 함수 실행 이후 가상 데이터 a, b 사라짐.
}
