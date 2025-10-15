package e_tabpane;
import java.awt.BorderLayout;

import javax.swing.*;
//JFrame 툴 가져오기
import javax.swing.JFrame;
import javax.swing.JTabbedPane;
import java.awt.Color;
import java.util.ArrayList;


public class MyScreen extends JFrame{
	//생성자
	PanelA a;
	PanelB b;
	PanelC c;
	//패널은 서로를 간섭할 수 없지만 스크린에서는 서로를 간섭할수 있으므로 스크린에 어레이 리스트를 만들어준다,	
	ArrayList result = new ArrayList();
	
	
	public void addResult() {
		// 데이터확인
//		for(int i=0;i<3;i++) {
//			ArrayList temp = new ArrayList();
//			temp.add("메뉴"+i);
//			temp.add(1000*(i+1));
//			result.add(temp);
//		}
//		//panelA에 있는 화면 Jtable(view)/ 모델에 지정
		a.tm.data = result;
		a.tm.fireTableDataChanged();
	}
	
	public MyScreen(){

		a = new PanelA();		
		b = new PanelB(this);	// this: MyScreen 객체 주소
		c = new PanelC();

		JTabbedPane pane = new JTabbedPane();
		pane.addTab("내역",a);
		pane.addTab("주메뉴", b);
		pane.addTab("부메뉴", c);
		pane.setSelectedIndex(1);
		
		// JFrame 기본 layout : BorderLayout
		// North, South, Center, West, East
		// 기본영역: Center
		add(pane,BorderLayout.CENTER);

		
		setBounds(300, 250, 1024, 900);
		setVisible(true);
		
		addResult();
		
	}
	
	
	
	
	public static void main(String[] args) {
		
		new MyScreen();
		
		
	}
}
