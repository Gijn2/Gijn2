package e_tabpane;

import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JPanel;

import e_tabpane.model.ModelC;

public class PanelC extends JPanel{
	
	JButton btn;
	
	ModelC model;
	
	public PanelC() {
		//모델 C 설정
		try {
			model = new ModelC();
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		btn = new JButton("치킨");
		
		add(btn);
		eventproc();
		setBackground(Color.BLACK);
						// int r, int g, int b -> 3원색 red green blue
		
	}
	void eventproc(){
		
		btn.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
			
				
			}
		});
		
	}
}
