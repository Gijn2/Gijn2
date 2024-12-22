package a_sample;

import java.awt.*;
import javax.swing.*;

class MyFrame1 extends JFrame{
	//멤버변수 선언
	JButton b1;
	JButton b2;
	
	JLabel l1;

	JCheckBox box1;
	JCheckBox box2;
	
	JList list;
	
	JComboBox combo;
	
	JRadioButton radio1;
	JRadioButton radio2;
	
	JTextField tf;
	JTextArea ta;
	
	//객체생성
	MyFrame1(){
		String[] data = {"1","2","3","4","5"};
		
		b1 = new JButton("ok");
		b2 = new JButton("cancel");
		
		l1 = new JLabel("HEllo World");

		box1 = new JCheckBox("male");
		box2 = new JCheckBox("female");
		
		list = new JList(data);
		
		combo = new JComboBox(data);
		
		radio1 = new JRadioButton("boy");
		radio2 = new JRadioButton("girl");
		ButtonGroup bg = new ButtonGroup();
		bg.add(box1);
		bg.add(box2);
		ButtonGroup bg1 = new ButtonGroup();
		bg1.add(radio1);
		bg1.add(radio2);
		
		tf = new JTextField("문구입력: ",10);
		ta = new JTextArea(10,60);
		
	}
	void addLayout() {
		//              FlowLayout - 윗줄 상단 중앙 배치(컴포넌트 크기 유지)
		//setLayout(new FlowLayout());
		
		//            GridLayout - 주어진 행과열에 맞춰 배치(컴포넌트 크기 유지x) 
		//setLayout(new GridLayout(5,5));
		//            BorderLayout - 중앙 동 서 남 북 5개 배치
		
		setLayout(new BorderLayout());
		add(b1,BorderLayout.WEST);
		add(b2,BorderLayout.EAST);
		
		add(l1,BorderLayout.NORTH);
		
		JPanel p = new JPanel();
		p.setLayout(new GridLayout(2, 1));
		p.add(radio1);
		p.add(radio2);
		add(p,BorderLayout.SOUTH);
		add(box2,BorderLayout.CENTER);
		

//		add(b1);
//		add(b2);
//		
//		add(l1);
//		
//		add(box1);
//		add(box2);
//		
//		add(list);
//		
//		add(combo);
//		
//		add(radio1);
//		add(radio2);
//		
//		add(tf);
//		add(ta);
		
		setBounds(600,600,600,600);
		setVisible(true);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}
}

public class Test2 {
	public static void main(String[] args) {
		MyFrame1 my = new MyFrame1();
		my.addLayout();
	}
}
