package f_singleton;

public class ScreenA {
	DBConnect con;
	public ScreenA() {

		con = DBConnect.getInstance();
		// con = new DBConnect(); 
		/* static 사용 이전
		 * 위의 그대로 ABC에 사용 시, static 함수로 안가고 기본 생성자 함수로 이동되어 "디비연동"도 출력됨.  
		 * ㄴ 출력값: "디비 연동""화면작업A""디비연동"...
		 */	
	}

	public void use() {
		System.out.println("화면작업A");

	}
}
