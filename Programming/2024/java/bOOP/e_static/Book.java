
package e_static;

/* static
 * - 각 객체들끼리 공유하고 싶을떄 사용 *****
 * - 메모리에 단 1개 생성
 * - 객체 생성보다 먼저 static 영역에 메모리 생성
 * 		ㄴ static 이 붙은 경우, 클래스명으로 접근해 부른다. *****
 * 
 * 
 *  ** 메모리를 하나만 먹으면서 정보를 공유하고 싶을 때, static 사용
 */

/* Static 을 붙힐경우,
 * 스택영역에서 저장한 변수들이 힙영역에 각자 저장 힙 영역 안에 있는 Static 영역에 count 를 가리킨다? 
 */

public class Book {
	private static	int count; //멤버변수는 자동으로 초기화가 된다. (int count = 0;)
	
	static {
		System.out.println("단 한번만 실행");
	} // 무조건 단, 1번 초기화 시키고 싶을 때 사용
	
	public Book(){
		count++;
		System.out.println("책 한권 생성");
	}
	
	// private 변수에 static 이 걸려 있어 return 을 사용할 떄, get 함수에도 static 을 걸어준다.
	static public int getCount() {
		return count;
	}
	
	
	
	
}
