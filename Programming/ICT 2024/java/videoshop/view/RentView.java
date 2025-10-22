package  videoshop.view;

import java.awt.BorderLayout;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.util.ArrayList;

import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.border.TitledBorder;
import javax.swing.table.AbstractTableModel;

import videoshop.model.RentDao;

import videoshop.model.dao.RentModel;
import videoshop.view.VideoView.ButtonEventHandler;



public class RentView extends JPanel 
{
	JTextField tfRentTel, tfRentCustName, tfRentVideoNum;
	JButton bRent;

	JTextField tfReturnVideoNum,tfReturnCustTel;
	JButton bReturn;

	JTable tableRecentList;

	RentTableModel rentTM;

	RentDao model;

	//==============================================
	//	 생성자 함수
	public RentView(){
		addLayout();	//화면구성
		eventProc();	//DB연결
		connectDB();
		showNoReturn();
	}

	// DB 연결
	void connectDB(){
		try {
			model = new RentModel();
		} catch (Exception e) {
			System.out.println("Connect DB 실패: ");
			e.printStackTrace();
		}
	}

	// 이벤트 등록
	public void eventProc(){

		ButtonEventHandler hdlr = new ButtonEventHandler();
		bRent.addActionListener(hdlr);
		bReturn.addActionListener(hdlr);
		//전화번호에서 엔터칠때


	}// end event


	/*	객체 생성 및 화면 구성   */
	void addLayout(){
		tfRentCustName = new JTextField(15);
		tfRentTel = new JTextField(15);
		tfRentVideoNum = new JTextField(15);
		bRent = new JButton("대 여");

		tfReturnVideoNum = new JTextField(15);
		tfReturnCustTel = new JTextField(15);
		bReturn = new JButton("반 납");


		// TM은 테이블 안의 관리모델이므로 미리 만들어 놓고 안에 넣어야한다.
		rentTM = new RentTableModel();
		tableRecentList = new JTable(rentTM);

		// 화면구성 *************************************

		// 화면 북쪽
		JPanel pNorth = new JPanel();

		// 화면 북 서 
		JPanel pNorth_west = new JPanel();
		pNorth_west.setBorder(new TitledBorder("반 납"));
		pNorth_west.setLayout(new GridLayout(3,2));
		pNorth_west.add(new JLabel("비디오 번호"));
		pNorth_west.add(tfReturnVideoNum);
		pNorth_west.add(new JLabel("고객 번호"));
		pNorth_west.add(tfReturnCustTel);		
		pNorth_west.add(bReturn);


		// 화면 북 동
		JPanel pNorth_east = new JPanel();
		pNorth_east.setBorder(new TitledBorder("대 여"));
		pNorth_east.setLayout(new GridLayout(4,2));
		pNorth_east.add(new JLabel("비디오 번호"));
		pNorth_east.add(tfRentVideoNum);
		pNorth_east.add(new JLabel("고객 성함"));
		pNorth_east.add(tfRentCustName);
		pNorth_east.add(new JLabel("고객 번호"));
		pNorth_east.add(tfRentTel);
		pNorth_east.add(bRent);


		pNorth.setLayout(new GridLayout(1,2));
		pNorth.add(pNorth_east);
		pNorth.add(pNorth_west);

		// 화면 중간
		JPanel pCenter = new JPanel();
		pCenter.setLayout(new BorderLayout());
		pCenter.add(new JScrollPane(tableRecentList), BorderLayout.CENTER );

		// 전체화면
		setLayout(new BorderLayout());
		add(pNorth, BorderLayout.NORTH);
		add(pCenter, BorderLayout.CENTER);

	}

	class RentTableModel extends AbstractTableModel { 

		ArrayList data = new ArrayList();
		String [] columnNames = {"비디오번호","제목","고객명","전화번호","반납예정일","반납여부"};

		public int getColumnCount() { 
			return columnNames.length; 
		} 

		public int getRowCount() { 
			return data.size(); 
		} 

		public Object getValueAt(int row, int col) { 
			ArrayList temp = (ArrayList)data.get( row );
			return temp.get( col ); 
		}

		public String getColumnName(int col){
			return columnNames[col];
		}
	}

	// 미납목록보기
	//	public void showNoReturn() {
	//		try {
	//			ArrayList data = model.selectNoReturn();
	//			rentTM.data = data;
	//			tableRecentList.setModel(rentTM);
	//			rentTM.fireTableDataChanged();
	//		}catch(Exception ex) {
	//			System.out.println("미납목록보기실패: ");
	//			ex.printStackTrace();
	//		}
	//	}


	class ButtonEventHandler implements ActionListener{
		public void actionPerformed(ActionEvent ev){
			Object o = ev.getSource();
			if(o==bRent){  
				String tel = tfRentTel.getText();
				int vNum = Integer.parseInt( tfRentVideoNum.getText());
				try {
					model.RentVideo(tel, vNum);
					showNoReturn();
				} catch (Exception e) {
					System.err.println("대여 이벤트 실패");
					e.printStackTrace();
				}					// 비디오 대여
			}
			else if(o==bReturn){  
				try {
					String tel = tfReturnCustTel.getText();
					int vNum = Integer.parseInt(tfReturnVideoNum.getText());
					model.ReturnVideo(tel,vNum);
					showNoReturn();

				} catch (Exception e) {
					System.err.println("반납 이벤트 실패");
					e.printStackTrace();
				} 

			}


			// ????
			//			else if(o==bReturn){  
			//				try {
			//					model.ReturnVideo(Integer.parseInt(tfReturnVideoNum.getText()));
			//				} catch (Exception e) {
			//					System.err.println("반납 이벤트 실패");
			//					e.printStackTrace();
			//				} 
			//
			//			}

		}

	}
	void showNoReturn(){

		try {
			rentTM.data = model.selectNoReturn();
			tableRecentList.setModel(rentTM);
			rentTM.fireTableDataChanged();
		} catch (Exception e) {
			e.printStackTrace();
		}


	}
}

