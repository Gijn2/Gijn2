package c_exercise;

import java.sql.*;

public class SelectEmp {
	
	public static void main(String[] args) {
		//0. 필요한 변수
		String driver = "com.mysql.cj.jdbc.Driver";
		String url = "jdbc:mysql://localhost:3306/basic";
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

			
			//3. SQL 문장 만들기 ** 제일 많이 건드리는 부분
			String sql = 
			    " SELECT e.ename, e.job, e.sal, d.dname "
			  + " from emp e join dept d "
			  + " on e.deptno = d.deptno "
			  + " ORDER BY e.sal ASC ";
			
			//4. SQL 전송 객체 얻어오기
			/*
			 * Statement: 완성된 SQL을 전송할때
			 * PreparedStatement: 미완성된 SQL을 전송할떄
			 * CallableStatement: PL - SQL(function/procedure) 호출할 떄
			 */
			ps = con.prepareStatement(sql);
			// 물음표가 있으나 없으나 prepareStatement를 써도된다.
			
			
			//5. 전송
			/* -int 	  executeUpdate()  : 3번이 insert update, delete, ddl
			 * -ResultSet executeQuery()	: 3번이 select
			 */
			rset = ps.executeQuery();
			while(rset.next()) {
				System.out.print(rset.getString("ENAME")+", ");
				System.out.print(rset.getString("JOB")+", ");
				System.out.print(rset.getInt("SAL")+", ");
				System.out.println(rset.getString("DNAME"));
			// 미완성은 안의 내용을 sql로 넣어서 가져가면 오류가 떠버린다.
			}
			System.out.println("전송 ");
			
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