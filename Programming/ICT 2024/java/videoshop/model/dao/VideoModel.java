package videoshop.model.dao;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;

import videoshop.model.VideoDao;
import videoshop.model.vo.Video;

public class VideoModel implements VideoDao{
	// 0. 드라이버 세팅
	String driver = "com.mysql.cj.jdbc.Driver";
	String url = "jdbc:mysql://LocalHost:3306/basic";
	String user = "scott";
	String pass = "tiger";
	public VideoModel() throws Exception{

		// 1. 드라이버로딩
		Class.forName(driver);
		System.out.println("VideoModel - 연결");
	}

	// ******** INSERT *********
	public void insertVideo(Video vo, int count) throws Exception{
		try {
			// 2. Connection 연결객체 얻어오기
			Connection con = null;

			con = DriverManager.getConnection(url, user, pass);
			// 3. sql 문장 만들기
			String sql =  " INSERT INTO Video "
					+ " ( videoName, genre, director, actor, exp ) "
					+ " VALUES (?,?,?,?,?) ";
			// 4. sql 전송객체 (PreparedStatement)	
			PreparedStatement ps = con.prepareStatement(sql);
			ps.setString(1, vo.getVideoName());
			ps.setString(2, vo.getGenre());
			ps.setString(3, vo.getDirector());
			ps.setString(4, vo.getActor());
			ps.setString(5, vo.getExp());
			// 5. sql 전송
			ps.executeUpdate();
			// 6. 닫기	
			con.close();
		}catch(Exception ex) {
			System.out.println("insert 실패: "+ex.getMessage());
		}
	}

	// ******** UPDATE *********
	public void modifyVideo(Video vo) throws Exception{
		Connection con;
		try {
			con = DriverManager.getConnection(url, user, pass);

			String sql =  " Update Video "
					+ " Set videoName = ? , genre = ? , director = ? , actor = ? , exp = ? "
					+ " Where videoNo = ? ";

			PreparedStatement ps = con.prepareStatement(sql);
			ps.setString(1, vo.getVideoName());
			ps.setString(2, vo.getGenre());
			ps.setString(3, vo.getDirector());
			ps.setString(4, vo.getActor());
			ps.setString(5, vo.getExp());		
			ps.setInt(6, vo.getVideoNo());
			
			ps.executeUpdate();
			
			con.close();
			
		}catch(Exception ex) {
			System.out.println("수정 실패: "+ex.getMessage());
		}
	}
	
	public void deleteVideo(Video vo){
			Connection con;
			try {
				con = DriverManager.getConnection(url, user, pass);

				String sql =  " Delete From Video "
							+ " Where videoNo = ? ";

				PreparedStatement ps = con.prepareStatement(sql);
				ps.setInt(1, vo.getVideoNo());
				
				ps.executeUpdate();
				
				con.close();
				
			}catch(Exception ex) {
				System.out.println("삭제 실패: "+ex.getMessage());
			}
		}
	
	
	// ******** ARRAY LIST *********
	public ArrayList selectVideos(int idx, String keyword) throws Exception{

		String [] column = {"videoName", "director"};

		ArrayList data = new ArrayList();
		//연결객체 얻어오기
		Connection con = DriverManager.getConnection(url, user, pass);

		String sql = " SELECT videoNo, videoName, genre, director, actor "
				+ 	 " FROM VIDEO "
				+ 	 " WHERE " + column[idx] + " LIKE '%" + keyword + "%' ; " ;
		PreparedStatement ps = con.prepareStatement(sql);

		ResultSet rs = ps.executeQuery();
		while(rs.next()) {
			ArrayList temp = new ArrayList();
			temp.add(rs.getInt("videoNo"));
			temp.add(rs.getString("videoName"));
			temp.add(rs.getString("genre"));
			temp.add(rs.getString("director"));
			temp.add(rs.getString("actor"));
			data.add(temp);
		}
		return data;
	}

	// ******** SEARCH BY PK(PRIMARY KEY) *********
	public Video searchByPk(int videoNum) {
		Video v = new Video();
		Connection con;
		try {
			con = DriverManager.getConnection(url, user, pass);

			String sql = " SELECT videoNo, videoName, genre, director, actor, exp"
					+ 	 " FROM VIDEO "
					+ 	 " WHERE videoNo =" + videoNum ;
			PreparedStatement ps = con.prepareStatement(sql);

			ResultSet rs = ps.executeQuery();
			if(rs.next()) {
				v.setVideoNo(rs.getInt("videoNo"));
				v.setVideoName(rs.getString("videoName"));
				v.setGenre(rs.getString("genre"));
				v.setDirector(rs.getString("director"));
				v.setActor(rs.getString("actor"));
				v.setExp(rs.getString("exp"));
			}
		}catch(Exception ex) {
			System.out.println("searchByPk 실패: "+ ex.getMessage());
		}
		return v;
	}
	
	

}

