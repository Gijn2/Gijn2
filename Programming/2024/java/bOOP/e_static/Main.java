package e_static;

public class Main {
	// main 함수에 static 을 넣어두는 이유: 자바 버츄얼 머신(jvm)이 클래스명으로 main 이라는 이름만 찾으면 실행이 가능하기때문
	
	public static void main(String[] args) {

//		Book b1 = new Book();
//		System.out.println("책 갯수: "+b1.count);
//		
//		Book b2 = new Book();
//		System.out.println("책 갯수: "+b2.count);
//		
//		Book b3 = new Book();
//		System.out.println("책 갯수: "+b3.count);
		
		// static 쓴 이후 ---
		Book b1 = new Book();
		System.out.println("책 갯수: "+Book.getCount());
		
//		Book b2 = new Book();
//		System.out.println("책 갯수: "+Book.getCount());
//				
//		Book b3 = new Book();
//		System.out.println("책 갯수: "+Book.getCount());

	}
}
