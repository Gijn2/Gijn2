package c_event;

import java.awt.*;
import java.awt.event.*; // 이건 클래스가 아니라 패키지를 가져오는거라서 따로 적어줘야한다.

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JOptionPane;

class MyScreen{
	// 1.멤버변수 선언
	JFrame f;

	JButton b;
	JButton c;
	// 2.객체 생성
	MyScreen(){
		f = new JFrame	("나의 창");
		b = new JButton	("OK");
		c = new JButton	("cancel");
	}
	// 3.화면 붙이기
	// 4.화면 띄우기
	void addLayout() {
		f.setLayout(new FlowLayout());
		f.add(b);
		f.add(c);

		f.setBounds(500, 600, 700, 700);
		f.setVisible(true);
		f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}// end of addLayout()

	//*********************
	//이벤트처리
	void eventPro() {
		//이벤트핸들러 객체생성
		MyHandle handle = new MyHandle();
		
		//이벤트 컴포넌트오ㅏ 이벤트 객체를 등록
		b.addActionListener(handle);
		
	}// end eventPro()

	// 이벤트핸들러: 이벤트를 처리하는 클래스
	class MyHandle implements ActionListener {
		public void actionPerformed(ActionEvent e) {
			JOptionPane.showMessageDialog(null, "버튼 눌렸어");

		}

	}


}// end of class MyScreen()


public class Test {

	public static void main(String[] args) {

		MyScreen my = new MyScreen();
		my.addLayout();
		my.eventPro();

	}
}


