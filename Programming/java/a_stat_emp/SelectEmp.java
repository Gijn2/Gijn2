package a_stat_emp;

import java.sql.*;

public class SelectEmp {
	public static void main(String[] args) {
		//0. 필요 변수
		String driver = "com.mysql.cj.jdbc.Driver";
		String url = "jdbc:mysql://localhost/basic";
		String user = "scott";
		String pw = "tiger";
		
		try {
			//1. 드라이버 로딩
			Class.forName(driver);
			System.out.println("드라이버 연결");
			
			//2. 연결 객체 얻어오기
			Connection con = DriverManager.getConnection(url, user, pw);
			
			//3. sql문
			String sql = "SELECT ename, job, sal FROM emp";
			
			//4. sql 전송객체 얻어오기
			Statement stmt = con.createStatement();		
			
			//5. 전송
			ResultSet rset = stmt.executeQuery(sql);
			while(rset.next()) {
				System.out.print(rset.getString("ENAME")+", ");
				System.out.print(rset.getString("JOB")+", ");
				System.out.println(rset.getInt("SAL"));
			}
			System.out.println("전송");
			
			//6.닫기
			rset.close();
			stmt.close();
			con.close();
			
		}catch(Exception ex){
			System.out.println("실패: "+ ex.getMessage());
		}
	}
}
