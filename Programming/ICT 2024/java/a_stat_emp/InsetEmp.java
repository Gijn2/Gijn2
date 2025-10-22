package a_stat_emp;
/*
 * 자바랑 데이터베이스 연결
 * 자바와 데이터베이스를 연결해주는 드라이버 연결
 * 준비물: 자바, 데이터베이스, 드라이버
 * connection -> 자바 코딩 잘하기(sql문 도구 사용)
 */
import java.sql.*;
import java.sql.DriverManager;

public class InsetEmp {
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
			int sabun = 5665;
			String sname = "그룯트";
			String job = "개발";
			
			//3. sql 문장 만들기 ** 제일 많이 건드리는 부분
//			String sql = "INSERT   "
//					+ " INTO emp(empno, ename, job) "
//					+ " VALUES(1238, '한기진', '디자인')";
			
			//** 2번의 사용자입력값을 가져오는 방법.
			String sql = "INSERT   "
					+ " INTO emp(empno, ename, job) "
					+ " VALUES("+sabun+", '"+sname+"', '"+job+"')";
			System.out.println(sql);
			
			
			//4. sql 전송 객체 얻어오기
			/*
			 * Statement: 완성된 sql을 전송할때
			 * PreparedStatement: 미완성된 sql을 전송할떄
			 * - ? 없어도 사용가능.
			 * CallableStatement: pl- sql(function/procedure) 호출할 떄
			 */
			
			Statement stmt = con.createStatement();			
			
			
			
			//5. 전송
			/* -int 	  executeUpdate()   : 3번이 insert update, delete, ddl
			 * -ResultSet executeQuery()	: 3번이 select
			 * 
			 * 이유: 리턴값이 다름.
			 */
			stmt.executeUpdate(sql);
			System.out.println("전송");
			
			//6. 닫기
			stmt.close();
			con.close();
			System.out.println("Goodbye");
						
			
			
		}catch (Exception ex) {
			System.out.println("실패:" +  ex.getMessage());


		}
	}
}