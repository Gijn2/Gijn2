package c_control;
import java.util.Scanner;

public class Ex11_dowhile연습 {
	public static void main(String[] args) {
		
	

		// 구구단 단수를 입력받아 구구단 출력

//		System.out.println("반복 횟수");
		Scanner input = new Scanner(System.in);

		//	int a = input.nextInt();
		//	int a1 = input.nextInt();
		//	
		//	
		//	for(int i =1; i<=9; i++) {
		//		System.out.println("구구단 단수");
		//	}


		//2 반복이 끊나거나 반복횟수를 모를 경우,
		//		while(true) {
		//			System.out.println("구구단 몇 번 반복할까요?");
		//			int num = input.nextInt();
		//
		//			for( int j=0; j<num; j++) {			
		//				System.out.println("구구단의 단수->");
		//				int dan = input.nextInt();
		//				for(int i=1; i<=9; i++) {
		//					System.out.println(dan +"*" + i + "=" + dan*i );
		//				}	
		//			}
		//			System.out.println("반복?");
		//			String answer = input.nextLine();
		//			if(answer.equals("y")|answer.equals("Y")) {
		//				break;
		//			}
		//		}
		
		String answer = "";
		do {
			System.out.println("구구단의 단수->");
			int dan = input.nextInt();
			
			for(int i=1; i<=9; i++) {
				System.out.println(dan*i);
			}
			System.out.println("반복?(Y/N)");
			answer = input.next();
		}while(answer.equals("y")|answer.equals("Y"));
		
		
		
		
		
		
		
		
		
		
		
		
	}
}
