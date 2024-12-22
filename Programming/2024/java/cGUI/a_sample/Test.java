package a_sample;
import java.awt.*;
/*
 * OOP 문법의 활용을 위해 GUI(화면) 만들기
 * 
 * java에서 그래픽 인터페이스만드는 방법
 * 
 * 1. AWT: 1.1
 * 
 * 2. Swing
 * 
 */
class MyScreen{
	// 1.멤버변수 선언
	Frame f;
	
	Button b;
	Button c;
	// 2.객체 생성
	MyScreen(){
		f = new Frame	("나의 창");
		b = new Button	("big button");
		c = new Button	("cancel");
	}
	
	// 3.화면 붙이기
	// 4.화면 띄우기
	void addLayout() {
		f.setLayout(new FlowLayout());
		f.add(b);
		f.add(c);
		
		
		f.setBounds(500, 600, 700, 700);
		f.setVisible(true);
	}
}

public class Test {

	public static void main(String[] args) {
		
		MyScreen my = new MyScreen();
		my.addLayout();
		
		
	}
}
