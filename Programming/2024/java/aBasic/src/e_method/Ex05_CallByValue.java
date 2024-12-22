package e_method;

/* 인자의 자료형이 기본형인 경우
 * call by value
 */
public class Ex05_CallByValue {
	public static void main(String[] args) {
		int a = 10,b = 20;
		add(a,b); //기본형을 보낼 경우, call by value
		System.out.println(a+","+b);
	}
	static void add(int a,int b) {
		a+=b;
		System.out.println(a+","+b);
	
	
	}
}
