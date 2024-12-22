package z_test;
import java.awt.Frame;


// is-a 방식

/**
 * 자바의 상속관계는 단일상속이 원칙: 부모 클래스가 1개만 들어올 수 있따.
 * 따로 부모를 잡지않으면 default 로 최상위 클래스인 object 가 잡힌다
 */

public class Test2 extends Frame{
	public Test2() {
	
		super("나의 두번쨰 창");
		//상속받아서 따로 Frame을 설정해주지않는다.
		setBounds(300,400,500,600);
		setVisible(true);
	}
	public static void main(String[] args) {
		Test2 t = new Test2();	
	}
	
}
