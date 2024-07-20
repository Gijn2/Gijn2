package a_sample;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Calendar;

import javax.swing.*;
//  도구 수입
class MyFrame extends JFrame{
	
}
public class InfoTest extends JFrame{

	// 멤버변수 선언
	JTextArea ta;
	JTextField tfName, tfId, tfTel, tfSex, tfAge, tfHome;
	JButton	  bAdd, bShow,bSearch, bDelete, bCancel, bExit;
	JLabel lName, lId, lTel, lSex, lAge, lHome;

	//객체 생성
	InfoTest(){
		super("나의 정보");
		
		
		ta = new JTextArea();

		tfName = new JTextField("Name",15);
		tfId = new JTextField("ID");
		tfTel = new JTextField("Tel");
		tfSex = new JTextField("Sex");
		tfAge = new JTextField("Age");
		tfHome = new JTextField("Home");
		
		bAdd = new JButton("Add");
		bShow = new JButton("Show");
		bSearch = new JButton("Search");	
		bDelete = new JButton("Delete");
		bCancel = new JButton("Cancel");
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

	
	void eventproc() {
		bExit.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e) {
				System.exit(0);
			}
			
		});//exit이 눌렸을 떄
		//종료버튼이 눌리면
		bCancel.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e) {
				clearTexts();
			}
		});//cancel 이 눌렸을 떄
		
		bAdd.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e) {
				JOptionPane.showMessageDialog(null, "입력합니다.");
			}
		});//add 가 눌렸을 떄
		
		//주민번호 ID에서 엔터쳤을 떄
		tfId.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e) {
				
				String id = tfId.getText();
				
				JOptionPane.showMessageDialog(null, "님 주민번호는 " + id + " 다.");
				
				// 성별
				char num = (id).charAt(7);
				
				switch(num) {
				case '9':
				case '3':
				case '1': tfSex.setText("남자");	break;
				
				case'2':
				case'0':
				case'4': tfSex.setText("여자");	break;
				
				default:System.out.println("한국인");
				}
				
				// 지역
				char area = id.charAt(8);

				switch(area) {
				case '0': tfHome.setText("서울");
					break;
				case '1': tfHome.setText("인천");
					break;
				case '2': tfHome.setText("경기");
					break;
				default: tfHome.setText("한국"); 
				}
				
				//나이
				Calendar c 	= Calendar.getInstance();			// 이미 있는 데이터를 불러오기.
				int year 	= c.get(Calendar.YEAR);
				
				String old_str = id.substring(0,2);
				int old = Integer.parseInt(old_str);
				
				char gend = id.charAt(7);
				int  cent = 0;
				int  age  = 0;
				
				switch(gend) {
				case'9':
				case'0':
				case'1': 
				case'2': cent = 1900;break;
				case'3': 
				case'4': cent = 2000;break;
				}
				
				age = year-(cent+old)+1;
				tfAge.setText(Integer.toString(age));
				
				
			}
		});
		
		
		
	}// end eventproc
	
	void clearTexts() {
		//종료버튼이 눌리면
		tfName.setText("");
		tfId.setText("");	
		tfTel.setText("");	
		tfSex.setText("");	
		tfAge.setText("");
		tfHome.setText("");	
				
	}// end eventproc
	
	
	public static void main(String[] args) {
		InfoTest test = new InfoTest();
		test.addLayout();
		test.eventproc();
	}
}

/*
 * ActionEvent : 자주 사용하는 이벤트 묶음
 * 
 * - 버튼 클릭시
 * 	 (메뉴 리스트에서 클릭할 수 있는거는 메뉴아이템)
 * - 메뉴아이템을 클릭시
 * - 리스트 더블클릭 시
 * - 텍스트필드에서 엔터를 쳤을 떄
 * 
 *  
 *  
 */ 
