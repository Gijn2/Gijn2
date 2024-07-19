package c_control;

import java.util.Scanner;

public class Ex02_if_전화번호 {
public static void main(String[] args) {
	
	
	// 볼거면 이거 밑에 코딩보기
	/**
	
	String tel = "02-123-4567";
			
	//문자 하나만 가져오는건 charAt()
			
	int idx1 = tel.indexOf("-"); // 0부터 2앞까지 -> 위의 번호로는 02만
	System.out.println(idx1);
	//'-'찾을때, indexOf
	
	//But 서울 외에는 3자리, 031.. 032..
	
	
	System.out.println("번호를 입력하세요");
	Scanner input = new Scanner(System.in);
	String a = input.nextLine();			// 입력하는 경우가 아닐경우, 빈자리로 변수 선언.	
	int idx = a.indexOf("-");
	System.out.println(idx);
	String a1 = a.substring(0,idx);
	System.out.println(a1);
	
	if(a1.equals("02")) {						
		a="서울";	
	}else if(a1.equals("032")){
		a="인천입니다.";
	}else {
		a="한국입니다.";
	}
	
	String b = input.nextLine();
	*/
	
	
	//if문 안에서 생기는 변수는 if문 안에서만 쓸 수 있는 변수. 밖에서는 소멸
	
	System.out.println("전화번호를 입력하세요");
	Scanner input = new Scanner(System.in);	// input이라는 변수에 system.in에 적인 값 저장 
	String Num = input.nextLine();			// Num이라는 문장 변수에 input값 문자로 저장
	String b = "";
	
	int a = Num.indexOf("-");				// a라는 숫자변수에 Num변수에 첫"-"의 자리수를 숫자로 저장
	String a1 = Num.substring(0,a);			// a1이라는 문장변수에 Num변수에 0번째~a-1번째 까지를 글로 저장
	
	if(a1.equals("02")) {					//if()문의 결과가 T/F에 따라
	Num = "인천";
	}
	
	// ************************************************************
	
	String tel = "02-123-4567";
	String gu = "";
	
	char ch = tel.charAt(5);
	System.out.println(ch);
	
	/*
	 * 서울인 경우 5번째 문자의 값이 3이면 마포구
	 * 아니면 강남구
	 */
	
	if(tel.equals("03")) {
	//1단	
		System.out.println("마포구");
		if(ch=='3') {
		//2단
			gu="마포구";
		}else {
			gu="강남구";
		}
		//2단
		
	}else {
		
	}
	//1단
	
	
	
	
}
}
