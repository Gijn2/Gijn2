package e_tabpane.model;

public class DBDriver {
	
	static DBDriver dbd = null;
	
	private DBDriver () throws Exception{
	
		Class.forName("com.mysql.cj.jdbc.Driver");
		System.out.println("드라이버 로딩");
	
	}
	
	static public DBDriver getInstance() {
		if(dbd==null) {
			try {
				dbd = new DBDriver();
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		return dbd;
	}
}
