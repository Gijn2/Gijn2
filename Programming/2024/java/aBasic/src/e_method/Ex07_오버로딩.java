package e_method;

public class Ex07_오버로딩 {
	public static void main(String[] args) {
		
		System.out.println(1000);		//int
		System.out.println(3.999);		//double
		System.out.println("왕");		//char
		System.out.println("ㅎㅇ");		//string
		
		
	}
}

/* 오버로딩:(OverLoading): 
 * 
 * 여러개의 함수가 동일한 함수명을 사용. -> 원래는 error
 * 인자의 자료형과 갯수가 달라야한다.
 * 
 * 함수명은 같지만 자료형이 다른 걸 오버로딩이라한다.
 * 
 * 
 * [주의] 리턴형만 다른 것은 아님.
 * 
 * void   test(int a){}
 * double test(int z){}
 * char   test(int c){}
 * ㄴ 오버로딩이 아님. a, z, c 인자가 같은 수일 경우, 들어가야하는 곳부터 정해지지 않아서 오류 
 * 
 */
	
// 4,   2, 4     6 2  4 2  안녕자바 자바 안녕 자바		6 0		4 