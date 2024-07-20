package b_prep_emp;

import java.sql.*;

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
			int sabun = 4321;
			String sname = "그루트2";
			String job = "개발";
			int sal = 10000;
			int mgr = 7788;
			int deptno = 30;
			
			//3. SQL 문장 만들기 ** 제일 많이 건드리는 부분
			String sql = "INSERT   "
					+ " INTO emp(empno, ename, job, sal, mgr, deptno) "
					+ " VALUES(?,?,?,?,?,?)";			
			
			//4. SQL 전송 객체 얻어오기
			/*
			 * Statement: 완성된 SQL을 전송할때
			 * PreparedStatement: 미완성된 SQL을 전송할떄
			 * CallableStatement: PL - SQL(function/procedure) 호출할 떄
			 */
			PreparedStatement ps = con.prepareStatement(sql);
			ps.setInt(1, sabun);
			ps.setString(2, sname);
			ps.setString(3, job);
			ps.setInt(4, sal);
			ps.setInt(5, mgr);
			ps.setInt(6, deptno);
			
			
			
			
			//5. 전송
			/* -int 	  executeUpdate()  : 3번이 insert update, delete, ddl
			 * -ResultSet executeQuery()	: 3번이 select
			 */
			
			
			ps.executeUpdate(); 		// 미완성은 안의 내용을 sql로 넣어서 가져가면 오류가 떠버린다.
			System.out.println("전송");
			
			
			
			//6. 닫기
			ps.close();
			con.close();
			System.out.println("Goodbye");
						
			
			
		}catch (Exception ex) {
			System.out.println("실패:" +  ex.getMessage());


		}
	}
}