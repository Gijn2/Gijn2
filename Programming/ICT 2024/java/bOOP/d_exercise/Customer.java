package d_exercise;

public class Customer {

	//(전화번호, 이름, 마일리지) 변수 설정

	private String tel ;
	private String name ;
	private int m ;

	//----------------------------------------------------
	public String getTel() {
		return tel;
	}

	public void setTel(String tel) {
		this.tel = tel;
	}

	//---------------------------------------------------
	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}
	//---------------------------------------------------
	public int getM() {
		return m;
	}

	public void setM(int m) {
		this.m = m;
	}
	// --------------------------------------------------
	
	//멤버함수
	public void output() {
		System.out.println(name+"님("+tel+")는"+m+"점 있습니다.");

	}
	
	// Constructor
	
	//main 2
	public Customer(String tel, String name, int m){
		this.tel = tel;
		this.name = name;
		this.m = m;
	}
	public Customer(String tel, String name){
		this.tel = tel;
		this.name = name;
	}
	
	// main 1
	public Customer() {
	
	}
	// 생성자함수를 하나라도 만들면 디폴트함수가 사라지기때문에 하나 만들어두자.

}
