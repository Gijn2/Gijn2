package b_prep_emp;

import java.sql.*;

public class SelectTestNo3 {
	
	public static void main(String[] args) {
		//0. 필요한 변수
		String driver = "com.mysql.cj.jdbc.Driver";
		String url = "jdbc:mysql://localhost:3306/advanced";
		String user = "scott";
		String pw = "tiger";
		
		try {	
			//1. 드라이버를 메모리 로딩
			Class.forName(driver);
			System.out.println("드라이버 연결");
			
			//2.  연결객체 언덩오기
			Connection con = DriverManager.getConnection(url, user, pw);
			System.out.println("디비연결성공");
			
			//3. SQL 문장 만들기 ** 제일 많이 건드리는 부분
			
			
			String sql = " SELECT employee_id, first_name"
						+ " FROM employees "
						+ " where department_id in (select department_id "
						+ "	from employees "
						+ "	where first_name like '%u%' )";
			
			//4. SQL 전송 객체 얻어오기
			PreparedStatement ps = con.prepareStatement(sql);
			
			//5. 전송
			ResultSet rset = ps.executeQuery();
			while(rset.next()) {
			System.out.print(rset.getString("EMPLOYEE_ID")+(", "));
			System.out.println(rset.getString("FIRST_NAME"));

			}
			System.out.println("데이터 전송");
			 
			//6. 닫기
			rset.close();
			ps.close();
			con.close();
			System.out.println("Goodbye");
			
		}catch (Exception ex) {
			System.out.println("실패:" +  ex.getMessage());


		}
	}
}