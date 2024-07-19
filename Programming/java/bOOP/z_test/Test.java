package z_test;
import java.awt.*;

public class Test {
	
	//has-a 방식
	
	Frame f;

	public Test() {
		f = new Frame("나의 첫 화면");

		f.setBounds(100, 200, 300, 100);
		f.setVisible(true);
	}

	public static void main(String[] args) {

		Test t = new Test();

	}
}
