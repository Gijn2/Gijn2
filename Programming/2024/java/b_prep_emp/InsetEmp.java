package b_prep_emp;

/*
 * 20번 부서이면서 월급이 2000 이상인 사원의 정보를삭제
 */

import java.sql.*;

public class InsetEmp {
	
	public static void main(String[] args) {
		//0. 필요한 변수
		String driver = "com.mysql.cj.jdbc.Driver";
		String url = "jdbc:mysql://175.114.130.17:3306/basic";
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
			// 7788사원이 이름을 그루트2 업무를 개발로 바꾸세요
			String sql  = "  "
						+ " Into info_tab (name, tel, sal, empno) "
						+ " values ('끝나기', '10분전', 9001, 3312)";
			
			//4. SQL 전송 객체 얻어오기
			/*
			 * Statement: 완성된 SQL을 전송할때
			 * PreparedStatement: 미완성된 SQL을 전송할떄
			 * CallableStatement: PL - SQL(function/procedure) 호출할 떄
			 */
			PreparedStatement ps = con.prepareStatement(sql);
			
			
			
			//5. 전송
			/* -int 	  executeUpdate()  : 3번이 insert update, delete, ddl
			 * -ResultSet executeQuery()	: 3번이 select
			 */			
			int a = ps.executeUpdate(); 		// 미완성은 안의 내용을 sql로 넣어서 가져가면 오류가 떠버린다.
			System.out.println(a + "행 실행");
			
						
			//6.   
			ps.close();
			con.close();
			System.out.println("Goodbye");
			
		}catch (Exception ex) {
			System.out.println("실패:" +  ex.getMessage());
		}
	}
}