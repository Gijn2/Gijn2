package i_inherit;

public class Test {
	public static void main(String[] args) {
		
//		Um u = new Um();
//		u.gene();
//		u.job();
		
		Ddal d = new Ddal();
		d.gene();
		d.study();
		d.job();
		// 부모자식 상속관계를 지으면 자식 클래스는 부모 클래스를 다 사용할 수 있다.
		// ㄴ 위 코딩 돌리면 부모 클래스의 생성자 함수까지 같이 나온다.
		
		//casting
		//원래 기본형끼리만 가능하지만 상속관계의 경우 관계 내의 형변환이 가능
		
		Um u = new Um();
		Ddal d1 = (Ddal)u;
		
		Ddal d2 = new Ddal();
		Um u1 = (Um)d2;
		
		
		
	}
}