package	 videoshop.view;

import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;
import javax.swing.*;
import javax.swing.border.*;
import javax.swing.table.AbstractTableModel; 
import javax.swing.text.TabExpander;

import mysql_e_jfreechart.MyFrame;
import videoshop.model.VideoDao;
import videoshop.model.dao.VideoModel;
import videoshop.model.vo.Video;


public class VideoView extends JPanel 
{	
	//	member field
	JTextField	tfVideoNum, tfVideoTitle, tfVideoDirector, tfVideoActor;
	JComboBox	comVideoJanre;
	JTextArea	taVideoContent;

	JCheckBox	cbMultiInsert;
	JTextField	tfInsertCount;

	JButton		bVideoInsert, bVideoModify, bVideoDelete;

	JComboBox	comVideoSearch;
	JTextField	tfVideoSearch;
	JTable		tableVideo;

	VideoTableModel tbModelVideo;

	// 모델변수
	VideoDao model;
	
	// 차트 변수
	JFrame frame;
	
	public void frameView() {
		Frame frame = new JFrame();	
	}

	//##############################################
	//	constructor method
	public VideoView(){
		addLayout(); 	// 화면설계
		initStyle();
		eventProc();
		connectDB();	// DB연결
	}

	public void connectDB(){	// DB연결
		try {
			model = new VideoModel();
		} catch (Exception e) {
			System.out.println("모델 불러오기 실패");
			e.printStackTrace();
		}
	}

	public void eventProc(){

		// ************** 다중입고 체크박스에 이벤트 발생하면
		cbMultiInsert.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				/*if(cbMultiInsert.isSelected()){
					tfInsertCount.setEditable(true);
				}else {
					tfInsertCount.setEditable(false);
				}*/
				tfInsertCount.setEditable(cbMultiInsert.isSelected());

			}
		});// 다중입고 이벤트 끝

		// *********** 버튼이벤트 발생
		ButtonEventHandler hdlr = new ButtonEventHandler();
		bVideoDelete.addActionListener(hdlr);
		bVideoInsert.addActionListener(hdlr);
		bVideoModify.addActionListener(hdlr);
		tfVideoSearch.addActionListener(hdlr);
		
		// JTable 에 클릭했을때
		tableVideo.addMouseListener(new MouseAdapter() {
			
			@Override
			public void mouseClicked(MouseEvent e) {
				int row = tableVideo.getSelectedRow();
				int col = 0;
				int videoNum = (int)tableVideo.getValueAt(row, col);
				// System.out.println("선택 비디오 번호:"+ videoNum);
				
				try {
				Video v = model.searchByPk(videoNum);
				tfVideoNum.setText(String.valueOf(v.getVideoNo()));
				tfVideoActor.setText((v.getActor()));
				tfVideoDirector.setText((v.getDirector()));
				tfVideoTitle.setText((v.getVideoName()));
				comVideoJanre.setSelectedItem(v.getGenre());
				taVideoContent.setText(v.getExp());
				
				// JOptionPane.showMessageDialog(null, );
				}catch(Exception ex) {
					System.err.println("실패: "+ex.getMessage());
				}
			}
		});
	}// 이벤트 끝

	// 버튼 이벤트 핸들러 만들기
	class ButtonEventHandler implements ActionListener{
		public void actionPerformed(ActionEvent ev){
			Object o = ev.getSource();

			if(o==bVideoInsert){  
				registVideo();					// 비디오 등록
			}
			else if(o==bVideoModify){  
				modifyVideo();					// 비디오 정보 수정
			}
			else if(o==bVideoDelete){  
				deleteVideo();					// 비디오 정보 삭제
			}
			else if(o==tfVideoSearch){
				searchVideo();					// 비디오 검색
			}
		}
	}

	// 입고 클릭시  - 비디오 정보 등록
	public void registVideo(){
		JOptionPane.showMessageDialog(null, "입고");
		// 1 화면에 사용자 입력값 얻어오기
		String genre = (String)comVideoJanre.getSelectedItem();

		// 2 얻어온 입력값들을 Video 멤버 지정 
		Video v = new Video();
		v.setGenre((String)comVideoJanre.getSelectedItem());
		v.setVideoName(tfVideoTitle.getText());
		v.setActor(tfVideoActor.getText());
		v.setDirector(tfVideoDirector.getText());
		v.setExp(taVideoContent.getText());
		try {
			model.insertVideo(v, Integer.parseInt(tfInsertCount.getText()));
			clearTexts();
		} catch(Exception ex) {
			System.out.println("입고실패: "+ ex.getMessage());
		}

		//		int count = Integer.parseInt(tfInsertCount.getText());
		//		try {
		//			model.insertVideo(v, count);
		//			//화면 지우기
		//			clearTexts();
		//		} catch (Exception e) {
		//			System.out.println("count 실패");
		//			e.printStackTrace();
		//		}
		//		
	}
	
	public void initStyle(){   // 입력하지 못하게 만듬.
		tfVideoNum.setEditable(false);
		tfInsertCount.setEditable(false);		
		// tfInsertCount.setEditable(false); : 편집이 안됨 = 사용자는 변경이 안되는 부분. 읽기전용
		tfInsertCount.setHorizontalAlignment(JTextField.RIGHT);
	}
	
	// 수정 클릭시 - 비디오 정보 수정
	public void modifyVideo(){
		
		Video v = new Video();
		v.setVideoNo(Integer.parseInt(tfVideoNum.getText()));
		v.setGenre((String)comVideoJanre.getSelectedItem());
		v.setVideoName(tfVideoTitle.getText());
		v.setDirector(tfVideoDirector.getText());
		v.setActor(tfVideoActor.getText());
		v.setExp(taVideoContent.getText());
		
		System.out.println(v.getVideoNo());
		
		try {
			model.modifyVideo(v);
			clearTexts();
		} catch (Exception e) {
			taVideoContent.append("수정 실패"+e.getMessage());
		}
		
		JOptionPane.showMessageDialog(null, "수정");
	}
	
	
	// 삭제 클릭시 - 비디오 정보 삭제
	public void deleteVideo(){
		Video v = new Video();
		v.setVideoNo(Integer.parseInt(tfVideoNum.getText()));
		v.setGenre((String)comVideoJanre.getSelectedItem());
		v.setVideoName(tfVideoTitle.getText());
		v.setDirector(tfVideoDirector.getText());
		v.setActor(tfVideoActor.getText());
		v.setExp(taVideoContent.getText());
		
		System.out.println(v.getVideoNo());
		
		try {
			model.deleteVideo(v);
			clearTexts();
		} catch (Exception e) {
			taVideoContent.append("삭제 실패"+e.getMessage());
		}
		JOptionPane.showMessageDialog(null, "삭제");
	}
	
	// 비디오현황검색
	public void searchVideo(){
		JOptionPane.showMessageDialog(null, "검색");
		
		int idx = comVideoSearch.getSelectedIndex();
		String keyword = tfVideoSearch.getText();
		
		try {
			ArrayList data = model.selectVideos(idx, keyword);
			tbModelVideo.data = data;
			tableVideo.setModel(tbModelVideo);
			tbModelVideo.fireTableDataChanged();
			
		}catch(Exception ex) {
			System.out.println("검색실패");
			ex.getMessage();
		}
	}
	
	//  화면설계 메소드
	public void addLayout(){
		//멤버변수의 객체 생성
		tfVideoNum = new JTextField();
		tfVideoTitle = new JTextField();
		tfVideoDirector = new JTextField();
		tfVideoActor = new JTextField();

		String []cbJanreStr = {"멜로","액션","스릴","코미디"};
		comVideoJanre = new JComboBox(cbJanreStr);
		taVideoContent = new JTextArea();

		cbMultiInsert = new JCheckBox("다중입고");
		tfInsertCount = new JTextField("1",5);

		bVideoInsert = new JButton("입고");
		bVideoModify = new JButton("수정");
		bVideoDelete = new JButton("삭제");

		String []cbVideoSearch = {"제목","감독"};
		comVideoSearch = new JComboBox(cbVideoSearch);
		tfVideoSearch = new JTextField(15);

		tbModelVideo = new VideoTableModel();
		tableVideo = new JTable(tbModelVideo);

		// 화면 구성
		//왼쪽영역
		JPanel p_west = new JPanel();
		p_west.setLayout(new BorderLayout());
		// 왼쪽 가운데
		JPanel p_west_center = new JPanel();	
		p_west_center.setLayout(new BorderLayout());
		// 왼쪽 가운데의 윗쪽
		JPanel p_west_center_north = new JPanel();
		p_west_center_north.setLayout(new GridLayout(5,2));
		p_west_center_north.add(new JLabel("비디오번호"));
		p_west_center_north.add(tfVideoNum);
		p_west_center_north.add(new JLabel("장르"));
		p_west_center_north.add(comVideoJanre);
		p_west_center_north.add(new JLabel("제목"));
		p_west_center_north.add(tfVideoTitle);
		p_west_center_north.add(new JLabel("감독"));
		p_west_center_north.add(tfVideoDirector);
		p_west_center_north.add(new JLabel("배우"));
		p_west_center_north.add(tfVideoActor);

		// 왼쪽 가운데의 가운데
		JPanel p_west_center_center = new JPanel();
		p_west_center_center.setLayout(new BorderLayout());
		// BorderLayout은 영역 설정도 해야함
		p_west_center_center.add(new JLabel("설명"),BorderLayout.WEST);
		p_west_center_center.add(taVideoContent,BorderLayout.CENTER);

		// 왼쪽 화면에 붙이기
		p_west_center.add(p_west_center_north,BorderLayout.NORTH);
		p_west_center.add(p_west_center_center,BorderLayout.CENTER);
		p_west_center.setBorder(new TitledBorder("비디오 정보입력"));

		// 왼쪽 아래
		JPanel p_west_south = new JPanel();		
		p_west_south.setLayout(new GridLayout(2,1));

		JPanel p_west_south_1 = new JPanel();
		p_west_south_1.setLayout(new FlowLayout());
		p_west_south_1.add(cbMultiInsert);
		p_west_south_1.add(tfInsertCount);
		p_west_south_1.add(new JLabel("개"));
		p_west_south_1.setBorder(new TitledBorder("다중입력시 선택하시오"));
		// 입력 수정 삭제 버튼 붙이기
		JPanel p_west_south_2 = new JPanel();
		p_west_south_2.setLayout(new GridLayout(1,3));
		p_west_south_2.add(bVideoInsert);
		p_west_south_2.add(bVideoModify);
		p_west_south_2.add(bVideoDelete);

		p_west_south.add(p_west_south_1);
		p_west_south.add(p_west_south_2);

		p_west.add(p_west_center,BorderLayout.CENTER);
		p_west.add(p_west_south, BorderLayout.SOUTH);   // 왼쪽부분완성

		//---------------------------------------------------------------------
		// 화면구성 - 오른쪽영역
		JPanel p_east = new JPanel();
		p_east.setLayout(new BorderLayout());

		JPanel p_east_north = new JPanel();
		p_east_north.add(comVideoSearch);
		p_east_north.add(tfVideoSearch);
		p_east_north.setBorder(new TitledBorder("비디오 검색"));

		p_east.add(p_east_north,BorderLayout.NORTH);
		p_east.add(new JScrollPane(tableVideo),BorderLayout.CENTER);
		// 테이블을 붙일때에는 반드시 JScrollPane() 이렇게 해야함 


		// 전체 화면에 왼쪽 오른쪽 붙이기
		setLayout(new GridLayout(1,2));

		add(p_west);
		add(p_east);
	}

	//화면에 테이블 붙이는 메소드 
	class VideoTableModel extends AbstractTableModel { 

		ArrayList data = new ArrayList();
		String [] columnNames = {"비디오번호","제목","장르","감독","배우"};

		//=============================================================
		// 1. 기본적인 TabelModel  만들기
		// 아래 세 함수는 TabelModel 인터페이스의 추상함수인데
		// AbstractTabelModel에서 구현되지 않았기에...
		// 반드시 사용자 구현 필수!!!!

		public int getColumnCount() { 
			return columnNames.length; 
		} 

		public void setText(String valueOf) {
			// TODO Auto-generated method stub
			
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
	// 정리 함수
	void clearTexts() {
		tfInsertCount.setText("");
		tfVideoActor.setText("");
		tfVideoDirector.setText("");
		tfVideoNum.setText("");
		tfVideoSearch.setText("");
		tfVideoTitle.setText("");
		taVideoContent.setText("");
		
	}
}


