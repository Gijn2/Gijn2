package e_tabpane;

import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;

import javax.swing.JButton;
import javax.swing.JPanel;

import e_tabpane.model.ModelB;

public class PanelB extends JPanel{
	JButton btn;
	
	MyScreen screen;
	
	ModelB model;
	
	public PanelB(MyScreen screen) {
		this.screen = screen;
		//모델 B 설정
		try {
			model = new ModelB();
		} catch (Exception e) {
			
			e.printStackTrace();
		}
		
		addLayout(); 
		eventproc();
		setBackground(new Color(250,150,0));
						// int r, int g, int b -> 3원색 red green blue
		
	}
	void addLayout() {
		btn = new JButton("통통");
		
		add(btn);
	}
	void eventproc(){
		
		btn.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
			// ㅁㅏ이 스크린에 어레이 리스트 결과에 추가만 하면 그 뒤로 패널에 목록으로 출력은 된다.
				ArrayList temp = new ArrayList();
				temp.add(btn.getText());
				temp.add(1000);
				
				screen.result.add(temp);
				screen.addResult();
				
			}
		});
		
	}
}
