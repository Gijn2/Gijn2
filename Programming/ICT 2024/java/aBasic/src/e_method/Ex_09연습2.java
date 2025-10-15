package e_method;

import java.util.Scanner;

public class Ex_09연습2 {
	public static void main(String[] args) {

		System.out.println("알파벳 입력");
		Scanner input = new Scanner(System.in); 
		String str = input.next();
		char alpha = str.charAt(0);

	// 논리변수 선언, 결과 출력
		boolean answer = method(alpha);
		System.out.println(answer);
	}
	// 함수
	static boolean method(char alpha) {

		if('A'<=alpha&alpha<='Z') {
			return false;
		}else {
			return true;
		}
	}
}
