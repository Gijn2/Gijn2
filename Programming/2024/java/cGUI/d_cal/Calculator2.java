package d_cal;

import java.awt.*;
import javax.swing.*;
import java.awt.event.*;

public class Calculator2 {

	// 1. 멤버변수 선언

	JFrame f;

	JTextField tf;

	JButton [] b = new JButton[10];

	JButton bPlu;
	JButton bMin;
	JButton bBox;
	JButton bSqu;
	JButton bEqu;

	double prev = 0, next = 0;	//연산자 전에 1번 숫자와 2번 숫자를 저장할 변수
	char op;	 	// 선택한 연산자 저장변수

	// 2. 객체 생성
	Calculator2(){

		f = new JFrame("계산기");

		tf = new JTextField();
		bPlu = new JButton("+");
		bMin = new JButton("-");
		bBox = new JButton("*");
		bSqu = new JButton("/");
		bEqu = new JButton("=");

		for(int i =0;i < b.length; i++) {
			b[i]= new JButton(String.valueOf(i));
		}		
	}

	//3. 화면 붙이기 및 화면 보이기
	void addLayout() {
		f.setLayout(new BorderLayout());
		f.add(tf,BorderLayout.NORTH);

		JPanel pCenter = new JPanel();
		pCenter.setLayout(new GridLayout(5, 3));
		for(int i =0;i < b.length; i++) {
			pCenter.add(b[i]);
		}
		pCenter.add(bPlu);
		pCenter.add(b[0]);
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
		
		for(int i =0; i <b.length; i++) {
			int su = i;
			b[i].addActionListener(new ActionListener(){
				public void actionPerformed(ActionEvent e) {
					String str = b[su].getText();
					String prevNum = tf.getText();
					tf.setText(prevNum+str);
				}
			});
		}
		
		// +
		bPlu.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e) {
				//TF 안의 값을 얻어와서 prev 변수에 저장
				prev = Integer.parseInt(tf.getText());
				// bPlu.getText()를 op에 저장
				op = bPlu.getText().charAt(0);				
				// tf 비우기
				tf.setText(null);
			}
		});
		
		// -
		bMin.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e) {
				//TF 안의 값을 얻어와서 prev 변수에 저장
				prev = Integer.parseInt(tf.getText());
				// bPlu.getText()를 op에 저장
				op = bMin.getText().charAt(0);				
				// tf 비우기
				tf.setText(null);
			}
		});
		
		// *
		bBox.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e) {
				//TF 안의 값을 얻어와서 prev 변수에 저장
				prev = Integer.parseInt(tf.getText());
				// bPlu.getText()를 op에 저장
				op = bBox.getText().charAt(0);				
				// tf 비우기
				tf.setText(null);
			}
			
		
		});
		
		bSqu.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e) {
				//TF 안의 값을 얻어와서 prev 변수에 저장
				prev = Integer.parseInt(tf.getText());
				// bPlu.getText()를 op에 저장
				op = bSqu.getText().charAt(0);				
				// tf 비우기
				tf.setText(null);
			}
		});		
		
		// = 버튼이 눌리면 
		// tf 입력한 숫자값을 얻어와서 next변수에 저장
		bEqu.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e) {
				double result = 0;
				next = Integer.parseInt(tf.getText());
				switch(op) {
				case '+': result = prev + next; break;
				case '-': result = prev - next; break;
				case '*': result = prev * next; break;
				case '/': result = prev / next; break;
				}
				tf.setText(String.valueOf((float)result));
			}
		});
	}

	public static void main(String[] args) {
		Calculator2 c = new Calculator2();
		c.addLayout();
		c.eventproc();
	}
}
