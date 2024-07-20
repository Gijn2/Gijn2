package f_Jtable;

import java.awt.BorderLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.util.ArrayList;

import javax.swing.*;
import javax.swing.table.AbstractTableModel;

public class JTableTest {

	JFrame frame;
	JButton button;

	JTable table; 			// 화면에 출력되는 view 만 담당. 내용을 따로 만들어주어야한다.

	MyTableModel tbModel; 	// 테이블의 데이터와 컬럼관리

	public JTableTest() {

		frame = new JFrame("프레임테스트");
		button = new JButton("버튼");
		tbModel = new MyTableModel();
		table = new JTable(tbModel);




		frame.add(new JScrollPane(table), BorderLayout.CENTER );
		// 데이터의양이 많을 수 있으므로 무조건 스크롤이 있는 화면으로 넣어줘야 테이블을 띄울수 잇다.
		frame.add(button, BorderLayout.SOUTH );
		frame.setBounds(500, 500, 600, 800);
		frame.setVisible(true);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

		//버튼이 눌렸을 때.

		button.addActionListener(new ActionListener() {			
			public void actionPerformed(ActionEvent e) {
				change();


			}

			void change() {
				ArrayList data = new ArrayList();
				for(int i = 0; i<4 ;i++) {
					ArrayList temp = new ArrayList();
					for(int j = 0; j<4 ;j++) {
						temp.add( new Integer(i+j));
					}
					data.add(temp);
				}
				// 그 데이타를 테이블모델에 지정 -> 그 테이블모델을 테이블에 지정
				tbModel.data = data;
				table.setModel(tbModel);
				// 바뀐 데이터를 화면에 반영할래
				tbModel.fireTableDataChanged();
			}
		});
		
		// 테이블에서 마우스 클릭했을 때
		table.addMouseListener(new MouseAdapter() {
			public void mouseClicked(MouseEvent e) {
				int row = table.getSelectedRow();
				int col = table.getSelectedColumn();
				Integer value = (Integer)table.getValueAt(row, col);
				
				System.out.println(row+", "+col+"눌림 > "+ value);
			}
		});
	}
	// ***************************************************************************
	class MyTableModel extends AbstractTableModel{

		ArrayList data = new ArrayList();
		String [] columnNames = {"하나", "둘", "삼", "사"};

		// 구현되지않은 함수 오버라이딩
		@Override
		public int getRowCount() {

			return data.size();
		}

		@Override
		public int getColumnCount() {

			return columnNames.length;
		}

		@Override
		public Object getValueAt(int rowIndex, int columnIndex) {
			ArrayList temp = (ArrayList)data.get(rowIndex);
			return temp.get(columnIndex);
		}
		public String getColumnName(int col) {
			return columnNames[col];
		}
	}

	public static void main(String[] args) {
		new JTableTest();	
	}
}
