package mysql_d_transection;

/******************************************************
*  @ 트랙잭션 예제
*/
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.border.*;

public class AccUI
{
	//===================================================
	// 전역변수 선언
	JFrame frame;
	JButton b_moveMoney, b_cancel;
	JTextField tf_sendAccNum, tf_recvAccNum, tf_moveMoney;

	//데이터베이서 연결 객체(모델) 변수
	AccLogic logic;
	
	//===================================================
	// 전역 변수의 객체 생성
	public AccUI(){
		frame		= new JFrame("예금 이체 프로그램");
		b_moveMoney	= new JButton("예금이체실행");
		b_cancel	= new JButton("이체취소");
		
		tf_sendAccNum	= new JTextField(20);
		tf_recvAccNum	= new JTextField(20);
		tf_moveMoney	= new JTextField(20);
		
		try {
			System.out.println("드라이버 연결성공");
			logic = new AccLogic();
		} catch (Exception ex) {
			System.out.println("드라이버 연결실패");
			ex.printStackTrace();
		}
	}

	//===================================================
	// 컴포넌트 붙이고 프레임 출력
	public void setup(){
		// 가운데 영역 ( 라벨과 텍스트필드 붙인 영역 )
		JPanel p_center1 = new JPanel();
		p_center1.setLayout( new FlowLayout(FlowLayout.RIGHT) );
		p_center1.add( new JLabel("보내는분 계좌번호") );
		p_center1.add( tf_sendAccNum );

		JPanel p_center2 = new JPanel();
		p_center2.setLayout( new FlowLayout(FlowLayout.RIGHT) );
		p_center2.add( new JLabel("받는분 계좌번호") );
		p_center2.add( tf_recvAccNum );

		JPanel p_center3 = new JPanel();
		p_center3.setLayout( new FlowLayout(FlowLayout.RIGHT) );
		p_center3.add( new JLabel("이체 금액") );
		p_center3.add( tf_moveMoney );

		JPanel p_center = new JPanel();
		p_center.setLayout( new GridLayout(3,1));
		p_center.add( p_center1 );
		p_center.add( p_center2 );
		p_center.add( p_center3 );

		// South 영역 ( 버튼 붙인 영역 )
		JPanel p_south = new JPanel();
		p_south.add( b_moveMoney );
		p_south.add( b_cancel );

		// 프레임에 붙이기
		frame.getContentPane().setLayout( new BorderLayout(20,20));
		frame.getContentPane().add("Center", p_center );
		frame.getContentPane().add("South", p_south );

		frame.pack();
		frame.setVisible( true );

		frame.setDefaultCloseOperation( JFrame.EXIT_ON_CLOSE );

	}

	// 이벤트처리 할 컴포넌트을 등록
	public void eventProc(){
		// "이체실행" 버튼이 눌렸을 때
		////////////////////////////////////////////////////////
		// 1. 화면에서 입력값 얻어오기
		// 2. Business Logic 객체 생성 ( ex. AccLogic )
		// 3. BL객체에서 계좌 이체하는 함수 호출 ( ex. moveAccount() )
		//		- 1번의 입력값을 인자로 넘김
		//		- 호출 후 넘겨받는 리턴값으로는 0이면 정상처리이고 
		//			-1이면 잘못된 경우이므로 메세지박스 출력
		b_moveMoney.addActionListener( new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				String send = tf_sendAccNum.getText();
				if(send == null) {
					send = "";
				}
				String resv = tf_recvAccNum.getText();
				int move = Integer.parseInt(tf_moveMoney.getText());
				
				int result = logic.moveAccount(send, resv, move);
				if(result == 0) {
					JOptionPane.showMessageDialog(null, "이체성공");
				}else {
					JOptionPane.showMessageDialog(null, "이체실패");
				}
				
						
			}
		} );
		
		// "이체취소" 버튼이 눌렸을 때
		b_cancel.addActionListener( new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				
			}
		} );
	}


	// 프로그램 시작
	public static void main(String[] args) 
	{
		
		AccUI  acc = new AccUI();
		acc.setup();
		acc.eventProc();
	}
}
