package i_inherit3;
// 추상 메소드를 가진 클래스는 추상적인 클래스가 되어야한다.
/*
 * 이를 통해 overriding 을 필수로 만들어 상속관계의 함수가 문제가 생길 경우, 바로 에러문구가 나온다.
 */

public abstract class Item {
	
	protected String num;
	protected String title;
	
	public Item(){
		System.out.println("부모 기본생성자");
	}
	
	public Item(String num, String title){
		this.num = num;
		this.title = title;
		System.out.println("부모 인자생성자");
	}
	
//	public void output() { } -> 빈칸으로 출력
	abstract public void output(); // abstract: 함수가 구현되지 않은 미완성(추상적) 함수
	
}
