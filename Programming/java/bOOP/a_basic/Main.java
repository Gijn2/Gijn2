package a_basic;

public class Main {

	public static void main(String[] args) {
		// 1. 변수선언
		Student h;
		
		// 2. 객체생성
		h = new Student();
		
		// Student라는 클래스에 접근할래
		
		h.name = "홍길동";
		h.kor = 100;
		h.eng = 88;
		h.math = 77;
		
		// Student 클래스 안에 있는 멤버에 접근해 사용
		
		System.out.println(h.name +"의 총점: " +h.calTotal());
		
		System.out.println("평균"+h.calAvg());
		
		
	}

}
