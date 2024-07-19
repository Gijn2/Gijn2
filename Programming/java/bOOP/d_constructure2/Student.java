package d_constructure2;

public class Student {


	private String name;
	public int kor, eng, math;
	private int total;
	private double avg;

	//default constructor
	Student(){
//		this.name = "이름없음";
//		this.kor = 50;
//		this.eng = 50;
//		this.math = 50;


		System.out.println("기본생성자");
	}
	
	// constructor 사용
	Student(String name, int kor, int eng, int math){
		this.name = name;
		this.kor = kor;
		this.eng = eng;
		this.math = math;
		System.out.println("인자생성자");
	}
	
	
	int calTotal() {
		total = eng + math + kor;
		return total;
	}

	double calAvg() {
		avg = (double)total/3;
		return avg;
	}

	// setter 과 getter 설정 후 생성된 함수
	// 마우스 우클릭 후 생성
	
	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public void setKor(int kor) {
		this.kor = kor;
	}

	public void setEng(int eng) {
		this.eng = eng;
	}

	public void setMath(int math) {
		this.math = math;
	}
	
	
	
}
