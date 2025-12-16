package e_method;

public class Ex01_인자 {

	/*
	 *  함수의 구조: 리턴형 메소드 형(파라메타 변수){
	 *  
	 *  }
	 *  
	 *  - 리턴형: 값을 반환하는 값의 자료형, 		   없으면 void
	 *  - 파라메타 변수: 인자(argument)를 받는 변수, 없으면 안 써도됨
	 */



	public static void main(String[] args) {

		int a =10, b = 20;

		add(a, b);								 // 인자, 매개변수, 파라미터
	}

	static void add(int a, int b) { 		//파라미터
		int sum = a+b;
		System.out.println("합"+sum);
	}

}
