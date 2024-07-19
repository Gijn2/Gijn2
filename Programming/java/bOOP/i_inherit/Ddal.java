package i_inherit;
	
	//상속관계: '자식 클래스' extends '부모 클래스'

public class Ddal extends Um{
	public void gene() {
		System.out.println("자식은 자식이다");
	}

	public void study() {
		System.out.println("학생이다");
	}

	//생성자 함수
	public Ddal() {
		System.out.println("자식 클래스 생성");
	}
}
