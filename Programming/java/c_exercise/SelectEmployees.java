package c_exercise;

import java.sql.*;

public class SelectEmployees {
	
	public static void main(String[] args) {
		//0. 필요한 변수
		String driver = "com.mysql.cj.jdbc.Driver";
		String url = "jdbc:mysql://localhost:3306/advanced";
		String user = "scott";
		String pw = "tiger";
		
		Connection con = null;
		PreparedStatement ps = null;
		ResultSet rset = null;
		
		try {	
			//1. 드라이버를 메모리 로딩
			Class.forName(driver);
			System.out.println("드라이버 연결");
			
			//2.  연결객체 언덩오기
			con = DriverManager.getConnection(url, user, pw);
			System.out.println("디비연결성공");

			// 사용자입력값을 받는다고 가정

			String searchName = "Jonathon";
			
			//3. SQL 문장 만들기 ** 제일 많이 건드리는 부분
			String sql = " SELECT concat(e.FIRST_NAME,' ', e.LAST_NAME) as ename "
			    + ", hire_date "
			    + " FROM employees e "
			    + " WHERE DEPARTMENT_ID IN("
			    + " 		SELECT DEPARTMENT_ID"
			    + "			FROM employees"
			    + "			WHERE FIRST_name = ?"
			    + "			) AND first_name <> 'Timothy'";
			
			//4. SQL 전송 객체 얻어오기
			/*
			 * Statement: 완성된 SQL을 전송할때
			 * PreparedStatement: 미완성된 SQL을 전송할떄
			 * CallableStatement: PL - SQL(function/procedure) 호출할 떄
			 */
			ps = con.prepareStatement(sql);
			ps.setString(1, searchName);
			
			// 물음표가 있으나 없으나 prepareStatement를 써도된다.
			
			//5. 전송
			/* -int 	  executeUpdate()  : 3번이 insert update, delete, ddl
			 * -ResultSet executeQuery()	: 3번이 select
			 */
			rset = ps.executeQuery();
			while(rset.next()) {
				System.out.print(rset.getString("ename")+", ");
				System.out.println(rset.getString("hire_date"));

				
				
			// 미완성은 안의 내용을 sql로 넣어서 가져가면 오류가 떠버린다.
			}
		}catch (Exception ex) {
			System.out.println("실패:" +  ex.getMessage());

		}finally {
			try {
			//6. 닫기
			rset.close();
			ps.close();
			con.close();
			System.out.println("Goodbye");
			}catch(Exception ex){
				
			}
			
		}
	}
}