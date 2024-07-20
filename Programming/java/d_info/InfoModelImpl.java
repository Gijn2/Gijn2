package d_info;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;

public class InfoModelImpl implements InfoModel{

	//0. DB에 필요한 변수
	String driver = "com.mysql.cj.jdbc.Driver";
	String url = "jdbc:mysql://localhost:3306/basic";
	String user = "scott";
	String pw = "tiger";

	//기본 생성자?
	//1. 드라이버를 메모리 로딩
	public InfoModelImpl() throws Exception{
		Class.forName(driver);
		System.out.println("InfoModelImpl - 연결");
	}

	/* 함수명: 
	 * 인자값: null
	 * 리턴값: null
	 * 역할: 회원가입하는 입력 값을 받아서 데이터베이스에 저장
	 */

	@Override
	public void insertData(InfoVO vo) throws Exception {
		// 연결 객체 얻어오기
		Connection con = null;
		try {
			con = DriverManager.getConnection(url, user, pw);
			//SQL 문장
			String sql =  " INSERT INTO "
					+ " info_tab(name, tel, jumin, gender, age, home) "
					+ " VALUES(?,?,?,?,?,?) 						  ";
			// 전송 객체 얻어오기
			PreparedStatement ps = con.prepareStatement(sql);

			// ? 값 지정 
			ps.setString(1, vo.getName());
			ps.setString(2, vo.getTel());
			ps.setString(3, vo.getId());
			ps.setString(4, vo.getSex());
			ps.setInt	(5, vo.getAge());
			ps.setString(6, vo.getHome());

			// 전송
			ps.executeUpdate();
		}finally {
			// 닫기
			con.close();
		}
	}

	public InfoVO searchByTel(String tel) throws Exception{
		InfoVO vo = new InfoVO();
		Connection con  = null;
		PreparedStatement ps = null;
		ResultSet rs = null;

		try {
			con = DriverManager.getConnection(url, user, pw);

			String sql = "Select * From info_tab where tel=? ";

			ps = con.prepareStatement(sql);
			ps.setNString(1, tel);

			rs = ps.executeQuery();
			if(rs.next()) {
				vo.setName(rs.getString("Name"));
				vo.setTel(rs.getString("Tel"));
				vo.setSex(rs.getString("Gender"));
				vo.setAge(rs.getInt("age"));
				vo.setHome(rs.getString("home"));
				vo.setId(rs.getString("jumin"));
			}

		}finally {
			con.close();
		}
		return vo;	
	}
	
	
	// ***********************
	public ArrayList<InfoVO> searchAll() throws Exception{
		ArrayList<InfoVO> list = new ArrayList<InfoVO>();

		Connection con  = null;
		PreparedStatement ps = null;
		ResultSet rs = null;

		try {
			con = DriverManager.getConnection(url, user, pw);

			String sql = "Select * From info_tab";

			ps = con.prepareStatement(sql);

			rs = ps.executeQuery();
			while(rs.next()) {
				InfoVO vo = new InfoVO();  

				vo.setName(rs.getString("Name"));
				vo.setTel(rs.getString("Tel"));
				vo.setSex(rs.getString("Gender"));
				vo.setAge(rs.getInt("age"));
				vo.setHome(rs.getString("home"));
				vo.setId(rs.getString("jumin"));

				list.add(vo);
			}
		}finally {
			con.close();
		}
		return list;	
	}


	public void deleteData(String tel) throws Exception{
		// 연결객체 가져오기
		Connection con  = null;
		PreparedStatement ps = null;
		int rs = 0;

		try {
			con = DriverManager.getConnection(url, user, pw);

			String sql = "Delete From info_tab where tel = ?";

			ps = con.prepareStatement(sql);
			ps.setString(1,tel);
			
			rs = ps.executeUpdate();
			
		}finally {
			ps.close();
			con.close();
		}
	}

	public void modifyData(InfoVO vo) throws Exception {
		
		Connection con = null;
		
		try {
			con = DriverManager.getConnection(url, user, pw);
			
			//SQL 문장	
			String sql = "Update info_tab "
					+" Set name=?, jumin=?, gender=?, age=?, home=? "
					+" Where tel =?";
			
			PreparedStatement ps = con.prepareStatement(sql);

			// ? 값 지정 
			ps.setString(1, vo.getName());
			ps.setString(2, vo.getId());
			ps.setString(3, vo.getSex());
			ps.setInt	(4, vo.getAge());
			ps.setString(5, vo.getHome());
			ps.setString(6, vo.getTel());

			// 전송
			ps.executeUpdate();
		}finally {
			// 닫기
			con.close();
		}
	}

	
	
	
	
}


