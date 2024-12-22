package f_singleton;

/*
 * 제시된 목적: DBConnect 객체가 1개 공유
 */

public class DBConnect {

	static DBConnect con;
	// default 값: static DBConnect con = null;
	//메모리에 먼저 getInstance함수가 올라가는 것을 막기위해 'con' 변수에도 static 을 붙혀준다
	public DBConnect() {
	// 생성자 함수 생성: *** void 없어야 생성자 함수 = return 으로 출력할 값이 없어야한다.
		System.out.println("디비 연동");
	}
	
	static public DBConnect getInstance() {
	//Instance 는 객체이므로 구별하기 편하게 이름저장
		if(con == null) {
			con = new DBConnect();
		}
		return con ;
	}
	// 맨 처음 한번만 객체를 생성하기 위한 코딩
	
}
