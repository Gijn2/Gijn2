package a_basic;

	// main 함수를 가져오지 않음.

public class Student {

	/*
	 서로 다른 데이터 타입을 가진 class
	
	 class 안의 변수, 
	 		멤버변수(): 서로 다른 데이터 타입
	 		멤버함수(): 맴버변수를 처리하는 역할
	 */


	String name;
	int kor, eng, math;
	int total;
	double avg;

	//서로다른 데이터 타입(멤버 변수들)을 묶어주는 class

	int calTotal() {
		total = eng + math + kor;

		return total;
	}

	double calAvg() {
		avg = (double)total/3;
		return avg;

	}

}
