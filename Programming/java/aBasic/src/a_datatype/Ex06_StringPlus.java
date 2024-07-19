package a_datatype;

public class Ex06_StringPlus {

	public static void main(String[] args) {
		
		/** ************ 중요 ***************
		 String class는 참조형이 맞다
		 하지만 유일하게 new를 안써도 되게끔 만듬
		 */
		
		/*
		 ****** 기본적인 참조형 작성법 *************
		String hong = new String("홍길동");
		String gil = new String("홍길동");
		*/
		
		
		String hong = "홍길동";
		String gil = "홍길동";
		
		
		
		if(hong.equals(gil)) {
			System.out.println("같은 상자");
		}else {
			System.out.println("다른 상자");
			
			
		}

	}

}
