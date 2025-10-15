package b_operator;

import java.util.Scanner;

public class test1 {
	public static void main(String[] args) {

		/**
		//******************연습 1***************


		System.out.println("점수입력"); 
		Scanner input = new Scanner(System.in);
		int a = input.nextInt();

		if(a%3 == 0){System.out.println("3의 배수입니다.");
		}else {System.out.println("3의 배수가 아니에요.");
		}
		 */

		/* ******************* 연습2 ********************
		/문자하나를 입력받아서 그 문자가 대문자인지 소문자인지 */

		System.out.println("알파벳을 입력하세요");
		Scanner input1 = new Scanner(System.in);
		String b = input1.nextLine();

		int v = (int)b.charAt(0);

		//float aa = 'A';System.out.println(aa);


		if(65 <= v && v <= 90) {
			System.out.println("대문자입니다.");
		} else {
			System.out.println("소문자입니다.");
		}
		
		/**
		 -> if구절을 char을 이용해 단어구문으로도 표현가능
		 char ch = str.charAt(0);
		 ...입력하세요..
		 if('A'<=ch & ch<='z'){
		 
		 } 로도 가능하다.
		 
		 */

		//******************** 연습3 ************
		// 해당년도가 윤년인지 평년인지
		
		/**
		System.out.println("년도를 입력하세요");
		Scanner input2 = new Scanner(System.in);
		int c = input2.nextInt();
		int d = 0; // 일단 /4 윤년인 애들 집합
		if(c%4==0) {
			d = c;
		}else {
			System.out.println("평년");
		}
		if(d%100!=0) {
			System.out.println("윤년");
		}else if(d%400==0){
			System.out.println("윤년");
		}else {
			System.out.println("평년");
		}
		// 가능은 할 듯, 코드가 너무 길어진다
		*/
	
		System.out.println("연도를 입력하소");
		Scanner input3 = new Scanner(System.in);
		int e = input3.nextInt();
		
		if(e%4==0||(e%4==0 && e%400==0)) {
			System.out.println("윤년");
		}


/*
 
 16
 
 3,4
 
 3(x) -> 1 [해설]  4 && 7 = 일반논리는 T/F만 가능 // 뭐가 없음, 추가설정 필요 ex. if(4>3 && 4 >7){~~ or "4&&7"이면 출력가능
 
 4
 
 -5
 
 
 */





	}
}
