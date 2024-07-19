package e_method;

public class Ex06_main인자 {

	/* method 명:main
	 * return 형:void = 리턴값 x
	 * 
	 * 매개변수	   :String
	 */
	public static void main(String[] args) {
	
		for(int i=0; i<args.length; i++){
			System.out.println(args[i]);
		}
		
	}
	/* 위의 메인 함수가 없을 경우,
	 * javac Ex06_main인자.java
	 * 
	 * java Ex06_main인자 // 뒤에 문자열을 넣을 수 있다. -> 이건 뒤의 args가 받는다.
	 */
}
