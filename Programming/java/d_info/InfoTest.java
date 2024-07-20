package d_info;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
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

	// 데이터베이스 연동변수 선언
	InfoModel model;

	//객체 생성
	InfoTest(){
		super("나의 정보");


		ta = new JTextArea();

		tfName = new JTextField(15);
		tfId = new JTextField();
		tfTel = new JTextField();
		tfSex = new JTextField();
		tfAge = new JTextField();
		tfHome = new JTextField();

		bAdd = new JButton("Add");
		bShow = new JButton("Modify");
		bSearch = new JButton("Search");	
		bDelete = new JButton("Delete");
		bCancel = new JButton("Clear");
		bExit = new JButton("Exit");

		lName = new JLabel("Name");

		//데이터베이스 연동 객체 생성
		//
		try {
			model = new InfoModelImpl();
			ta.setText("드라이버 로딩 성공");
		}catch(Exception ex) {
			ta.setText("실패: "+ex.getMessage());
		}
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
		pWest.add(new JLabel("Home",SwingConstants.CENTER));
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

				try {
					//1. 사용자 입력값 얻어오기
					String name = tfName.getText();
					String id = tfId.getText();
					String tel = tfTel.getText();
					String sex = tfSex.getText();
					int age = Integer.parseInt(tfAge.getText());
					String home = tfHome.getText();

					//2. 여러 입력값들을 VO객체로 지정
					//InfoVO vo = new InfoVO(name,id,tel~~~~)
					InfoVO vo = new InfoVO();
					vo.setName(name);
					vo.setAge(age);
					vo.setHome(home);
					vo.setId(id);
					vo.setSex(sex);
					vo.setTel(tel);

					// 연결확인
					model.insertData(vo);
					clearTexts();


					ta.append("연결성공");
				} catch (Exception ex) {
					ta.append("연결실패"+ex.getMessage());
				}
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

		//전화번호에서 엔터칠떄
		tfTel.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e) {
				String tel = tfTel.getText();
				try {
					InfoVO vo = model.searchByTel(tel);
					// 각각 화면 텍스트필드에 지정(출력)
					tfName.setText(vo.getName());
					tfId.setText(vo.getId());
					tfHome.setText(vo.getHome());
					tfSex.setText(vo.getSex());
					tfAge.setText(String.valueOf(vo.getAge()));

				}catch(Exception ex){
					ta.setText("전화번호 검색실패:" + ex.getMessage());
				}
			}
		});

		// search 버튼이 눌리면
		bSearch.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e) {

				searchAll();

			}
		});


		//		bSearch.addActionListener(new ActionListener(){
		//			public void actionPerformed(ActionEvent e) {
		//
		//				try {
		//					ArrayList<InfoVO> list = model.searchAll();
		//					ta.setText("=========검색결과 ============== \n\n");
		//
		//					for(int i=0; i<list.size();i++) {
		//						InfoVO temp = (InfoVO)list.get(i);
		//						ta.append(temp.toString()+"\n\n");
		//					}
		//
		//				}catch(Exception ex){
		//					System.out.println("실패: "+ex.getMessage());
		//				}
		//			}
		//		});

		// delete 버튼이 눌리면
		bDelete.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e) {

				String tel = tfTel.getText();
				try {
					model.deleteData(tel);
				} catch (Exception e1) {
					e1.printStackTrace();
					ta.append("연결실패: "+ e1.getMessage());
				}
				clearTexts();
				searchAll();
			}	
		});

		bShow.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e) {
				try {
					//1. 사용자 입력값 얻어오기
					String name = tfName.getText();
					String id = tfId.getText();
					String tel = tfTel.getText();
					String sex = tfSex.getText();
					int age = Integer.parseInt(tfAge.getText());
					String home = tfHome.getText();

					//2. 여러 입력값들을 VO객체로 지정
					//InfoVO vo = new InfoVO(name,id,tel~~~~)
					InfoVO vo = new InfoVO();
					vo.setName(name);
					vo.setAge(age);
					vo.setHome(home);
					vo.setId(id);
					vo.setSex(sex);
					vo.setTel(tel);

					// 연결확인
					model.modifyData(vo);
					clearTexts();
					searchAll();

					ta.append("연결 성공");
				} catch (Exception ex) {
					ta.append("수정 실패"+ex.getMessage());
				}

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

		ta.setText("");

	}// end eventproc

	void searchAll() {
		try {
			ArrayList<InfoVO> list = model.searchAll();
			ta.setText("=========검색결과 ============== \n\n");

			for(int i=0; i<list.size();i++) {
				InfoVO temp = (InfoVO)list.get(i);
				ta.append(temp.toString()+"\n\n");
			}

		}catch(Exception ex){
			System.out.println("실패: "+ex.getMessage());
		}
	}
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
