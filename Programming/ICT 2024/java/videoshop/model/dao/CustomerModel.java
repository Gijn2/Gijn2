package videoshop.model.dao;

import java.security.DrbgParameters.NextBytes;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;

import com.mysql.cj.protocol.Resultset;

import videoshop.model.CustomerDao;
import videoshop.model.vo.Customer;

public class CustomerModel implements CustomerDao{
	// 0.세팅
	String driver = "com.mysql.cj.jdbc.Driver";
	String url = "jdbc:mysql://LocalHost:3306/basic";
	String user = "scott";
	String pass = "tiger";

	public CustomerModel() throws Exception{
		// 1. 드라이버로딩		
		Class.forName(driver);
	}
	
	// ******* 입력함수
	public void insertCustomer(Customer vo) throws Exception{

		// 2. Connection 연결객체 얻어오기
		Connection con = null;
		try {
			con = DriverManager.getConnection(url, user, pass);
			// 3. sql 문장 만들기
			String sql =  " INSERT INTO "
					+ " Customer(custName, custTel1, custTel2, custAddr, custEmail) "
					+ " VALUES(?,?,?,?,?) 						  					";

			// 4. sql 전송객체 (PreparedStatement)	
			PreparedStatement ps = con.prepareStatement(sql);

			ps.setString(1, vo.getCustName());
			ps.setString(2, vo.getCustTel1());
			ps.setString(3, vo.getCustTel2());
			ps.setString(4, vo.getCustAddr());
			ps.setString(5, vo.getCustEmail());

			// 5. sql 전송
			ps.executeUpdate();
		}finally {
			// 6. 닫기 
			con.close();
		}
	}
	
	
	
	
	
	// ********* 검색 리스트 
		public ArrayList<Customer> searchAll() throws Exception{
			ArrayList<Customer> list = new ArrayList<Customer>();

			Connection con = null;
			
			try {
				con = DriverManager.getConnection(url, user, pass);
				
				String sql =  "Select custAddr, custEmail, custName, custTel1, custTel2"
							+ " From Customer ";

				PreparedStatement ps = con.prepareStatement(sql);

				ResultSet rs = ps.executeQuery();
				while(rs.next()) {
					Customer cu = new Customer();  
					
					cu.setCustAddr(rs.getString(1));
					cu.setCustEmail(rs.getString(2));
					cu.setCustName(rs.getString(3));
					cu.setCustTel1(rs.getString(4));
					cu.setCustTel2(rs.getString(5));
					list.add(cu);
				}
			}finally {
				con.close();
			}
			return list;	
		}
	// ************** 번호로 검색 함수
	public Customer selectByTel(String tel) throws Exception{
		Customer vo = new Customer();
		try{
			Connection con = DriverManager.getConnection(url, user, pass);

			String sql = " Select * "
					+ 	 " From Customer "
					+ 	 " Where custTel1 = ? ";

			PreparedStatement ps = con.prepareStatement(sql);		
			ps.setString(1, tel);

			ResultSet rs = ps.executeQuery();
			if(rs.next()) {
				vo.setCustName(rs.getString(1));
				vo.setCustTel1(rs.getString(2));
				vo.setCustTel2(rs.getString(3));
				vo.setCustAddr(rs.getString(4));
				vo.setCustEmail(rs.getString(5));
			}
		}catch(Exception ex) {
			System.out.println("전번 검색 함수 실패: "+ex.getMessage());
		}
		return vo;	
	}

	// ************** 이름으로 검색 함수
		public Customer selectByName(String name) throws Exception{
			Customer vo = new Customer();
			try{
				Connection con = DriverManager.getConnection(url, user, pass);

				String sql = " Select * "
						+ 	 " From Customer "
						+ 	 " Where custName = ? ";

				PreparedStatement ps = con.prepareStatement(sql);		
				ps.setString(1, name);

				ResultSet rs = ps.executeQuery();
				if(rs.next()) {
					vo.setCustName(rs.getString(1));
					vo.setCustTel1(rs.getString(2));
					vo.setCustTel2(rs.getString(3));
					vo.setCustAddr(rs.getString(4));
					vo.setCustEmail(rs.getString(5));
				}
			}catch(Exception ex) {
				System.out.println("이름검색 함수 실패: "+ex.getMessage());
			}
			return vo;	
		}
		
	// *********** 수정 함수
	public int updateCustomer(Customer vo) throws Exception{

		int result = 0;
		Connection con = null;
		try {
			con = DriverManager.getConnection(url, user, pass);
			String sql =  " Update Customer "
						+ " Set custName = ?, custTel2 = ?, custAddr = ?, custEmail = ? "
						+ " Where custTel1 = ?";

			PreparedStatement ps = con.prepareStatement(sql);

			ps.setString(1, vo.getCustName());
			ps.setString(5, vo.getCustTel1());
			ps.setString(2, vo.getCustTel2());
			ps.setString(3, vo.getCustAddr());
			ps.setString(4, vo.getCustEmail());

			result = ps.executeUpdate();
		}finally {
			con.close();
		}
		return result;
	}
}
