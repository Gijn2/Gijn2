package videoshop.model.dao;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.Vector;

import videoshop.model.RentDao;


public class RentModel implements RentDao{
	// 드라이버 세팅
	String driver = "com.mysql.cj.jdbc.Driver";
	String url = "jdbc:mysql://LocalHost:3306/basic";
	String user = "scott";
	String pass = "tiger";

	Connection con;

	public RentModel() throws Exception{
		// 1. 드라이버로딩
		Class.forName(driver);
		System.out.println("RentModel - 연결");	
	}
	
	// ******* RENT VIDEO *******
	public void RentVideo(String tel, int vNum) throws Exception{
		/* 전화번호 입력값 얻어오기
		 * 
		 * 대여할 비디오번호 입력값 얻어오기
		 * 모델에 rentvideo호출
		 * 화면 비우기
		 * 
		 */
		try {
			con = DriverManager.getConnection(url, user, pass);;
			String sql =  " Insert Into Rent "
					+ " (custTel1 , videoNo , rentDate , returnYN ) "
					+ " VALUES (?,?,SYSDATE(),'N')";
			
			PreparedStatement ps = con.prepareStatement(sql);
			ps.setString(1, tel);
			ps.setInt(2, vNum);
			
			ps.executeUpdate();
		}finally {
			con.close();
		}
	}
	
	
	// ******* RETURN VIDEO *******
	public void ReturnVideo(String tel,int vNum) throws Exception {
		System.out.println(tel);
		System.out.println(vNum);
		try {
			con = DriverManager.getConnection(url, user, pass);;
			String sql =  " Update Rent "
						+ " set returnDate = SYSDATE() , returnYN = 'Y' "
						+ " WHERE custTel1 = ? and videoNo = ? ";
			
			PreparedStatement ps = con.prepareStatement(sql);
			ps.setString(1, tel);
			ps.setInt(2, vNum);
			
			ps.executeUpdate();
		}finally {
			con.close();
		}
	}
	
	// ##@
	public ArrayList selectNoReturn()throws Exception {


		String [] column = {"videoName", "director"};

		ArrayList data = new ArrayList();
		
		Connection con = DriverManager.getConnection(url, user, pass);

		String sql = " SELECT r.videoNo as '비디오번호', v.videoName as '비디오 이름', c.custName as '고객명', c.custTel1  as '고객번호', adddate( r.returndate, 3) as '반납예정일' , r.returnYN as '미납여부' "
				+ 	 " FROM customer c inner join rent r "
				+ 	 " on c.custTel1 = r.custTel1 "
				+ 	 " join video v "
				+ 	 " on r.videoNo = v.videoNo "
				+ 	 " WHERE r.returndate is null " ;
		PreparedStatement ps = con.prepareStatement(sql);

		ResultSet rs = ps.executeQuery();
		while(rs.next()) {
			ArrayList temp = new ArrayList();
			temp.add(rs.getInt(1));
			temp.add(rs.getString(2));
			temp.add(rs.getString(3));
			temp.add(rs.getString(4));
			temp.add(rs.getDate(5));
			temp.add(rs.getString(6));
			data.add(temp);
		}
		return data;
		
		}
	
	
	
	
	
}
