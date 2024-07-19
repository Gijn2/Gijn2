package d_constructure2;

public class Main {

	public static void main(String[] args) {
		
		Student h = new Student();
		//Student h = new Student("홍길동",100,80,70);
		System.out.println(h.getName() +"의 총점: " +h.calTotal());
		// ctrl 함수 클릭 시, Main 의 해당 함수로 이동
		System.out.println("평균"+h.calAvg());
		
		
		
		
		Student h2 = new Student("홍길동",50,50,50);
		
		System.out.println(h2.getName() +"의 총점: " +h2.calTotal());
		System.out.println("평균"+h2.calAvg());
		
		
		
		
		// 2. 값 지정
		
//		h.setName("홍길동");
//		h.setKor(100);
//		h.setEng(88);
//		h.setMath(77);
		
		//클래스 초기화
		//변수선언 + 값지정
		

		
		
	
		
		
		
		
	}

}
