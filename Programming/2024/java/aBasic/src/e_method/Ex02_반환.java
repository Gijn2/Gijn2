package e_method;

public class Ex02_반환 {
	public static void main(String[] args) {
		
		// 'return'으로 가져올 변수 설정
		int sum = add();
		
		// 출력
		System.out.println("합 "+ sum);
		
	}
	static int add() {			// return 할 변수의 자료형을 기입(int, char...)
		//데이터
		int a =10, b= 20;
		int sum = a+b;
		// return: 제어권을 반환
		return sum;				// 여기서 프로그램을 반환. 딱 1개의 데이터만 가져갈 수 있음 
								// 이후에 함수에 작성하는 거는 오류 - 뒷 부분은 갈 일이 없음
	}
}
