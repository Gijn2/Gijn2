package d_cal;

import java.awt.*;
import javax.swing.*;


public class Calculator {
	
	// 1. 멤버변수 선언
	
	JFrame f;
	
	JTextField tf;
	
	JButton num0;
	JButton num1;
	JButton num2;
	JButton num3;
	JButton num4;
	JButton num5;
	JButton num6;
	JButton num7;
	JButton num8;
	JButton num9;
	
	JButton bPlu;
	JButton bMin;
	JButton bBox;
	JButton bSqu;
	JButton bEqu;
	
	// 2. 객체 생성
	Calculator(){
	
		f = new JFrame();
		
		tf = new JTextField("");
		
		num0 = new JButton("0");
		num1 = new JButton("1");
		num2 = new JButton("2");
		num3 = new JButton("3");
		num4 = new JButton("4");
		num5 = new JButton("5");
		num6 = new JButton("6");
		num7 = new JButton("7");
		num8 = new JButton("8");
		num9 = new JButton("9");
		
		bPlu = new JButton("+");
		bMin = new JButton("-");
		bBox = new JButton("*");
		bSqu = new JButton("/");
		bEqu = new JButton("=");
		
	}
	
	//3. 화면 붙이기 및 화면 보이기
	void addLayout() {
		f.setLayout(new BorderLayout());
		
		f.add(tf,BorderLayout.NORTH);
		tf.setPreferredSize(new Dimension(60,60));
		
		JPanel pCenter = new JPanel();
		
		pCenter.setLayout(new GridLayout(5, 3));
		
		pCenter.add(num1);
		pCenter.add(num2);
		pCenter.add(num3);
		pCenter.add(num4);
		pCenter.add(num5);
		pCenter.add(num6);
		pCenter.add(num7);
		pCenter.add(num8);
		pCenter.add(num9);
		pCenter.add(bPlu);
		pCenter.add(num0);
		pCenter.add(bEqu);
		pCenter.add(bMin);
		pCenter.add(bBox);
		pCenter.add(bSqu);
		
		f.add(pCenter,BorderLayout.CENTER);
		f.setBounds(500, 600, 700, 700);
		f.setVisible(true);
	}
	

	

	//--------------------------------------------------------

	//4. 이벤트처리
	void eventproc() {
		
	}
	
	public static void main(String[] args) {
		Calculator c = new Calculator();
		c.addLayout();
		c.eventproc();
	}
}
