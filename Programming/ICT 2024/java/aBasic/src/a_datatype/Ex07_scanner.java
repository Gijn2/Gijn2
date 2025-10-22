package a_datatype;

// 패키지 import 자동 단축기: Scanner에 ctrl + shift + o
import java.util.Scanner;

public class Ex07_scanner {

	public static void main(String[] args) {
		/*
		 콘솔에 출력
		 	system.out
		 		' print()
		 		' println()
		 		' printf()
		 		
		 콘솔에 입력
		 	system.in
		 	
		 -> Scanner 이용	
		 
		 */
		
		//import java.utill            import java.lang.*;
//		
//		System.out.println("이름을 입력해:");
//		Scanner input = new Scanner(System.in);
//		String name = input.nextLine();
//		
//		System.out.println("당신의 이름은 " + name);
//		
		/*
		 문자열 입력시: next()/ nextLine()
		 ㄴ 두 명령어 차이점 ==> 과제
		 정수형 입력시: nextInt
		 실수형 입력시: nextDouble()
		 */
		
		
		System.out.println("첫번쨰 수를 입력하세요");
		Scanner input = new Scanner(System.in);
		int first = input.nextInt();
		
		System.out.println("두번쨰 수를 입력하세요");
		Scanner input1 = new Scanner(System.in);
		int second = input1.nextInt();
		
		int add = first + second;
		System.out.println("두 수의 합은 " + add);
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	}

	}
