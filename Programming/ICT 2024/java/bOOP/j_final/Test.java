package j_final;
/* - abstract: 추상보다 미완성으로 보는게 편하다
 * final ~ : 변경불가
 * 
 * 'final field	: 상수 취급
 * 'final method: overriding 금지 
 * 'final class	: 부모클래스 불가
 */
final class Parents{
	final String field = "부모님";
	final public void jib() {
		System.out.println("부모님이 만드신");
	}
}

//class Child extends Parents{
//	public Child() {
//		// field = "내꺼"; 						// final 변수는 가져올 수 없다. final 이 붙은 거에는 절대 에러가 떠버린다.
//	}
//	
//	//	public void jib() {
//	//		System.out.println("모든 걸 탕진");
//	//	}										// final method 는 overriding 이 안됨.
//}												// final class 는 부모 클래스가 될 수 없다. -> abstract 도 붙힐 수 없다

public class Test {
	public static void main(String[] args) {
//		Parents p = new Child();
//		System.out.println(p.field);
//		p.jib();
	}
}
