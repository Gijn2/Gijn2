package c_control;
import java.util.Scanner;
public class Ex07_for_practice2 {

	public static void main(String[] args) {

		System.out.println("문자입력");
		Scanner input = new Scanner(System.in);

		String a = input.nextLine();
		char ch = a.charAt(0);
		
		if('a'<=ch&ch<='z') {
			for(char alpha='a';alpha<=ch;alpha++) {
				System.out.println(alpha);
			}
		}else if('A'<=ch&ch<='Z') {
			for(char alpha='A';alpha<=ch;alpha++) {
				System.out.println(alpha);
		}

			
	//----------------------------------------------------------		
			
			System.out.println("문자를 입력하세요");
			Scanner input1 = new Scanner(System.in);
			String a1 = input1.nextLine();
			// 문자입력받음
			int ch1 = a1.indexOf("");
			int c1 = 0;
			//입력받은문자의 수?
			
//			for(String b1 = a1;b1<=ch1;c1--) {
//				System.out.println(b1);
//					}
			
			
			
			
			
		}
			
			
			
		}
	}

		
