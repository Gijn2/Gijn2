package a_sample;

import java.awt.*;
import javax.swing.*;

//  도구 수입
class MyFrame2 extends JFrame{
	
}
public class InfoTest2 extends JFrame{

	// 멤버변수 선언
	JTextArea ta;
	JTextField tfName, tfId, tfTel, tfSex, tfAge, tfHome;
	JButton	  bAdd, bShow,bSearch, bDelete, bCancel, bExit;
	JLabel lName, lId, lTel, lSex, lAge, lHome, img;
	
	//객체 생성
	InfoTest2(){
		super("나의 정보");	
		
		ta = new JTextArea();
		
		tfName = new JTextField("Name",15);
		tfId = new JTextField("Name");
		tfTel = new JTextField("Name");
		tfSex = new JTextField("Name");
		tfAge = new JTextField("Name");
		tfHome = new JTextField("Name");
		
		bAdd = new JButton("Add", new ImageIcon("src\\image\\1.png"));
		bShow = new JButton("Show");
		
		bSearch = new JButton("Search", new ImageIcon("src\\image\\3.png"));	
		bDelete = new JButton("Delete", new ImageIcon("src\\image\\4.png"));
		bCancel = new JButton("Cancel", new ImageIcon("src\\image\\1.png"));
		bExit = new JButton("Exit");
		
		lName = new JLabel("Name");
	}

	//화면 붙이기 및 출력
	void addLayout() {

		setLayout(new BorderLayout());

		add(ta,BorderLayout.CENTER);

		JPanel pWest = new JPanel();
		
		pWest.setLayout(new GridLayout(6, 2, 10, 0));
		
		pWest.add(new JLabel("Name",JLabel.CENTER));
		pWest.add(tfName);
		pWest.add(new JLabel("ID",SwingConstants.CENTER));
		pWest.add(tfId);
		pWest.add(new JLabel("Tel",SwingConstants.CENTER));
		pWest.add(tfTel);
		pWest.add(new JLabel("Sex",SwingConstants.CENTER));
		pWest.add(tfSex);
		pWest.add(new JLabel("Age",SwingConstants.CENTER));
		pWest.add(tfAge);
		pWest.add(new JLabel("HOme",SwingConstants.CENTER));
		pWest.add(tfHome);
		
		add(pWest,BorderLayout.WEST);

		JPanel pSouth = new JPanel();
		pSouth.setLayout(new GridLayout());
		pSouth.add(bAdd);
		pSouth.add(bShow);
		pSouth.add(bSearch);
		pSouth.add(bDelete);
		pSouth.add(bCancel);
		pSouth.add(bExit);
		add(pSouth,BorderLayout.SOUTH);

		setBounds(700,700,700,500);
		setVisible(true);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}	

	public static void main(String[] args) {
		InfoTest2 test = new InfoTest2();
		test.addLayout();
		
	}
}
