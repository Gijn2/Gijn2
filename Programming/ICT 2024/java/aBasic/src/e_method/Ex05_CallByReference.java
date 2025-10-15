package e_method;

/*
 * call by ref
 * 	- 메소드의 인자가 참조형인 경우,
 *  - 단, String은 특이 케이스이므로 예외
 *  	주소가 복사되어 원본에 영향을 준다.
 */

public class Ex05_CallByReference {
	public static void main(String[] args) {

		StringBuffer a = new StringBuffer("안녕");
		StringBuffer b = new StringBuffer("ㅎㅇ");
		add(a, b);
		
		// a의 값에 영향을 줌
		System.out.println(a+","+b);

	}// 메인함수에 a 라는 주소에 "안녕"이라는 문자 저장 
	static void add(StringBuffer a, StringBuffer b) {
		a.append(b);
		System.out.println(a+","+b);
		
	}
}