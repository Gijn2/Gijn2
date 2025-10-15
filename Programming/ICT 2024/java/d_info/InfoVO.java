package d_info;


//VO,DTO: value object, data transfer object
//DAO:
public class InfoVO {
	// 멤버 변수
	// 원래 VO들은 private 걸어줘야함
	String name;
	String id;
	String tel;
	String sex;
	int age;
	String home;
	
	//1. 생성자로 지정
	// 자동으로 인자없는 기본함수가 안 만들어지므로 수동으로 만들어주자
	
	//기본 생성자
	public InfoVO() {}
	
	//인자 생성자
	public InfoVO(String name, String id, String tel, String sex, int age, String home) {
		super();
		this.name = name;
		this.id = id;
		this.tel = tel;
		this.sex = sex;
		this.age = age;
		this.home = home;
	}
	
	//2. getter setter 지정
	
	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}

	public String getTel() {
		return tel;
	}

	public void setTel(String tel) {
		this.tel = tel;
	}

	public String getSex() {
		return sex;
	}

	public void setSex(String sex) {
		this.sex = sex;
	}

	public int getAge() {
		return age;
	}

	public void setAge(int age) {
		this.age = age;
	}

	public String getHome() {
		return home;
	}

	public void setHome(String home) {
		this.home = home;
	}
	
	// 
	@Override
	public String toString() {
		return "InfoVO [name=" + name + ", id=" + id + ", tel=" + tel + ", sex=" + sex + ", age=" + age + ", home="
				+ home + "]";
	}
	
	
}
