package a_stat_emp;

import java.sql.*;
import java.sql.DriverManager;

public class UpdateEmp {
	public static void main(String[] args) {
		//0. 필요한 변수
		String driver = "com.mysql.cj.jdbc.Driver";
		String url = "jdbc:mysql://localhost:3306/basic";
		String user = "scott";
		String pw = "tiger";
		
		try {	
			//1. 드라이버를 메모리 로딩
			Class.forName(driver);
			System.out.println("드라이버 연결");
			
			//2.  연결객체 언덩오기
			Connection con = DriverManager.getConnection(url, user, pw);
			System.out.println("디비연결성공");

			// 사용자입력값을 받는다고 가정
			int sabun = 7839;
			String sname = "그루트";
			String job = "개발";
			
			//3. sql 문장 만들기 ** 제일 많이 건드리는 부분
			String sql = "Update emp"
					+ " Set ename ='"+sname+"'"+ ",job='"+job+"'"
					+ " Where empno = "+sabun;
			
			//4. sql 전송 객체 얻어오기
			Statement stmt = con.createStatement();			
			
			//5. 전송
			int result = stmt.executeUpdate(sql);
			System.out.println(result + "행을 수행.");
			
			//6. 닫기
			stmt.close();
			con.close();
			
		}catch (Exception ex) {
			System.out.println("실패:" +  ex.getMessage());


		}
	}
}