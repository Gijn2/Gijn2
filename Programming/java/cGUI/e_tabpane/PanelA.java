package e_tabpane;

import java.awt.BorderLayout;
import java.awt.Color;
import java.util.ArrayList;

import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.table.AbstractTableModel;

import e_tabpane.model.ModelA;

public class PanelA extends JPanel{
	
	MyTableModel tm;
	JTable table;
	
	ModelA model;
	
	public PanelA() {
		//모델 A 설정
		try {
			model = new ModelA();
		} catch (Exception e) {
			System.out.println("모델 실패:");
			e.printStackTrace();
		}
		
		tm = new MyTableModel();
		table = new JTable(tm);
		
		setLayout(new BorderLayout());
		add(new JScrollPane(table), BorderLayout.CENTER);
		
		setBackground(Color.GREEN); // Green 은 상속된 함수의 것, 이 값들은 static 이다.
		
	}
	class MyTableModel extends AbstractTableModel{

		ArrayList data = new ArrayList();
		String [] columnNames = {"메뉴", "가격"};

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

}
