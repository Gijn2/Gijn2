package e_method;

public class Ex04_참고_맴버변수 {
	/* 멤버 변수: class안의 변수
	 * 멤버 함수: class안의 함수
	 */
	
	//맴버 변수 선언
	static int a =10,b =20;
	static int sum = 0;
	
	public static void main(String[] args) {

	add();
	System.out.println(sum);
	
	
}
static void add() {
	sum = a+b;
}
}
