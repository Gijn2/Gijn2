package e_method;

public class Ex05_CallByString {
	public static void main(String[] args) {

		String a = new String("안녕");
		String b = new String("ㅎㅇ");
		add(a, b);
		
		// a의 값에 영향을 줌
		System.out.println(a+","+b);		//안녕, ㅎㅇ

	}
	static void add(String a, String b) {
		a+=(b);
		System.out.println(a+","+b);		//안녕ㅎㅇ,ㅎㅇ
		
	/* 참조형은 주소가 넘어가서 원본에 영향을 미친다.
	 * String 은 특별 클래스라서 참조형이지만 'CallByReference'를 따르지않는다.
	 * 
	 * 'String'은 값이 조금만 변경되어도 메모리를 새로 생성.
	 * 함수 내의 string a 의 '' 
	 * 
	 * 	a = 안녕 ㅎㅇ, b = ㅎㅇ // 안녕 ㅎㅇ 라는 새로운 메모리를 잡는다. 
	 *  
	 */
	
	
	
	
	}
}
