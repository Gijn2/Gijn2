package c_control;

import java.util.Scanner;

public class Ex01_if_주민번호 {
	public static void main(String[] args) {

		/*
	 자료형
	 1.기본형
	 - boolean char int double

	 2.참조형
	 - 클래스 			/ 배열
	 	ㄴ String(*)
	 	ㄴ 특이 케이스
		 */

		String id =  "111111-1234567";
		//String id = new String("");

		// 자바스크립 = 프로그램언어는 0부터 카운트/ 데이터베이스쪽은 1부터 카운트
		id.charAt(7);
		char num = id.charAt(7);

		if(num=='1' || num=='3'|| num=='9') {	// 실수형이랑 문자형 구분 안하면 다르게 인식한다.
			System.out.println("남자");
		}else if(num=='0' || num=='2'|| num=='4'){
			System.out.println("여자");
		}else if(num=='5'||num=='7') {
			System.out.println("남 외국인");
		}else if(num=='6'||num=='8') {
			System.out.println("여 외국인");
		}
		
		char num1 = id.charAt(1);
		char num2 = id.charAt(2);
		System.out.println("당신이 태어난 년도는"+num1+num2);
		
		
		System.out.println("문자입력");
		Scanner input = new Scanner(System.in);
		String str = input.next();
		char ch = str.charAt(0);		//String -> char 형변환 안됨. 둘이 자료형이 다름
		
		
		
		
		
	}
}