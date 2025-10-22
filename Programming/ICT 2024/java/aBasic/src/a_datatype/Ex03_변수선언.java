package a_datatype;

public class Ex03_변수선언 {
	//class 생성할 때, 박스 체크를 안 했을 경우, main을 입력하고 ctrl+스페이스바 - 엔터(메인 메소드)
	public static void main(String[] args) {

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
		int a = 10, b = 20;
		System.out.println("A=" + a + "B=" + b + "입니다.");
		int temp = a; 											// 임시변수 temp를 지정해서 저장해야한다
		a = b;													// 컴퓨터는 반드시 중간처리가 있어야댐
		b = temp;
		System.out.println(a*b+5);
		
		

	}
}
