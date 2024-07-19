package d_constructure;
	/*
	 * 생성자함수(constructor)
	 * 	- 클래스의 멤버값을 초기화 할 때 사용
	 * 
	 *  - 클래스가 객체화(인스턴스화)될 때, 실행되는 함수: new 사용시
	 *  
	 *  규칙
	 *  - 반드시 클래스명과 동일한 이름을 가져야한다.
	 *  	+
	 *  	리턴형이 없음(void 도 있으면 안된다.)
	 *  
	 *  - 오버로딩 가능(overloading)
	 *  	-> 매개변수의 타입과 갯수가 다른 동일한 이름의 함수
	 *  
	 *  
	 *  [참고]
	 *  1.	class A{
	 *  		int A = 10;
	 *  		1. void A(){일반함수
	 *  		   }
	 *  		2. A(){ 생성자함수
	 *  		   }
	 *  	}
	 *  
	 *  2. 기본 생성자함수: default
	 *  - 생성자함수가 한 개도 없는 경우, 자동으로 추가됨.
	 *  	ㄴ-> Student(){} 
	 *  
	 *  - 기본 생성자함수를 습관처럼 만들어 둔다.
	 *  
	 *  *********************************************************
	 *  - this: 멤버변수를 정확하게 지칭하기 위해서 사용
	 *  
	 *  - this(): 다른 생성자함수를 호출한다
	 *  	
	 *  	- this 함수의 위치는 무조건 가장 첫 줄에 있어야한다. 
	 *  
	 */

public class Student {

	/*
	 서로 다른 데이터 타입을 가진 class
	
	 class 안의 변수, 
	 		멤버변수(): 서로 다른 데이터 타입
	 		멤버함수(): 맴버변수를 처리하는 역할
	 */


	private String name;
	public int kor, eng, math;
	private int total;
	private double avg;

	Student(){
		this.name = "이름없음";
		this.kor = 50;
		this.eng = 50;
		this.math = 50;
	}
	//서로다른 데이터 타입(멤버 변수들)을 묶어주는 class
	// constructor 사용
	Student(String name, int kor, int eng, int math){
		this.name = name;
		this.kor = kor;
		this.eng = eng;
		this.math = math;
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
		// this 를 해줘야 위의 변수와 위치를 확실하게 알 수 있다.
		// 같은 이름을 줄 때, 이름과 위치를 확실하게 하기 위해 사용
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
