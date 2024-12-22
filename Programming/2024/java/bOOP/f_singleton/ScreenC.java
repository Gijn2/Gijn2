package f_singleton;

public class ScreenC {
	DBConnect con;
	public ScreenC() {
		//con = new DBConnect();
		con = DBConnect.getInstance();
	}
	
	public void use() {
		System.out.println("화면작업C");
	}
}
