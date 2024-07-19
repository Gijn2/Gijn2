package f_singleton;

public class ScreenB {
	DBConnect con;
	public ScreenB() {
		//con = new DBConnect();
		con = DBConnect.getInstance();
	}
	
	public void use() {
		System.out.println("화면작업B");
	}
}
