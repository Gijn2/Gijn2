package e_method;

public class Ex00_flow {
	static void method() {
		System.out.println("메소드-함수 실행");				// 순서2
	}
														// 16
														// 21
	public static void main(String[] args) {
		// 달디달고 달디달고 달디단 밤양갱 밤양갱이야~
		
		 
			 System.out.println("메인 시작"); 				// 순서 1
			 
			 method();									// 5라인으로 점핑
			 
			 System.out.println("메소드 중");
			 System.out.println("1");
			 
			 method();									// 5라인으로 점핑
			 System.out.println("2");
			 
			 
			 System.out.println("끝");
		
		
		
		
		

	}

}
