package d_constructure;
/*
 * 변수선언 int a;
 * 값지정 	 a = 10;
 * 
 * 변수초기화 int a = 10;
 * ------------------------
 * 
 * 
 */
public class Main {

	public static void main(String[] args) {
		
		
		// 1. 변수선언 + 객체생성 - new 이용
		// 인자가 없는 함수
		Student h = new Student();
		
		// 2. 값 지정
		
//		h.setName("홍길동");
//		h.setKor(100);
//		h.setEng(88);
//		h.setMath(77);
		
		//클래스 초기화
		//변수선언 + 값지정
		

		//Student h = new Student("홍길동",100,80,70);
		System.out.println(h.getName() +"의 총점: " +h.calTotal());
		// ctrl 함수 클릭 시, Main 의 해당 함수로 이동
		
		System.out.println("평균"+h.calAvg());
		
		
	}

}
