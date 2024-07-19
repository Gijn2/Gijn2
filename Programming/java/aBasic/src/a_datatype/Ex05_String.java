package a_datatype;

public class Ex05_String {

	public static void main(String[] args) {
		/*
		복습.데이터타입
		1. 기본형(primitive)
			- 논리형: boolean
			- 문자형: char
			- 정수형: int/long
			- 실수형: double
		
		2. 참조형(reference): 클래스 / 배열
		-> new 키워드를 통해 메모리를 확보해야함(객체생성)
		[ex] 이름이 홍길동
			char a = '홍길동'; -> 오류
			char a = "홍길동"; -> 오류
			
			해결법: 변수 a,b,c -> '홍' '길' '동'
			
		[cf] 문자 1개 => char
			 문자열(0개이상) => string(클래스)
			
		사용처: 회원가입, 로그인 등
			
		 */
		
		
		//참조변수선언
		String name;
		
		//메모리 확보(값지정) - 객체생성
		name = new String("홍씨");
		
		String irum = new String("홍씨");
		
		if(name == irum) {
			System.out.println("동일이름");
		}else {
			System.out.println("다른이름");
		}
		
		// 다른이름이 뜨는 이유: 변수 이름이 다르므로 다르게 인지
		// **문자열 비교는 equals 함수를 이용해야만함
		if(name.equals(irum)) {
			System.out.println("동일이름2");
		}else {
			System.out.println("다른이름2");
		}
		
		
		
		
		
		
		
		
		
		
		
		
		
	}

}
