package mysql_e_jfreechart;

import java.sql.*;
import java.util.*;

public class Database {

	String URL =  "jdbc:mysql://127.0.0.1:3306/basic";
	String USER = "scott";
	String PASS = "tiger";

	public ArrayList<ArrayList> getData() {

		ArrayList<ArrayList> data = new ArrayList<ArrayList>();
		try{
			Class.forName("com.mysql.cj.jdbc.Driver");
			Connection con = DriverManager.getConnection(URL, USER , PASS);	
			
			//***************************************************************
			String sql  = "SELECT Month(hiredate), count(Month(hiredate)) AS CNT "
						+ " FROM emp"
						+ " GROUP BY Month(hiredate)";
			
			
			//***************************************************************
			
			PreparedStatement stmt = con.prepareStatement( sql );	

			ResultSet rset = stmt.executeQuery();

			
			while( rset.next() ){
				ArrayList temp = new ArrayList();
				temp.add( rset.getInt("CNT"));			//****************
				temp.add( rset.getString("Month(hiredate)"));		//****************		
				data.add(temp);
			}
			rset.close();
			stmt.close();
			con.close();
		} catch(Exception ex){
			System.out.println("에러 : " + ex.getMessage() );
		}
		return data;
	}
}
