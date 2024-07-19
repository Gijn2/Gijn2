
package c_control;

import java.util.Scanner;

public class review2 {
	public static void main(String[] args) {	

		for(int i=0; i<5; i++) {
			for(int j=0; j<15; j++) {
				if(j<5) {
					System.out.print("**");
				}else if(j>=5) {
					System.out.print("--");	
				}
			}
			System.out.println();
		}

		for(int i=0; i<5; i++) {
			for(int j=0; j<15; j++) {
				System.out.print("--");
			}
			System.out.println();
		}

		// -------------------------------
		System.out.println();

		for(int i=0; i<5; i++) {
			for(int j=0; j<4-i; j++) {
				System.out.print(" ");
			}
			for(int j=0; j<i+1; j++) {
				System.out.print("*");
			}
			System.out.println();
		}
		// -----------------------------------	
		
			Scanner input = new Scanner(System.in); // 스캐너 객체 생성
			System.out.println("삼각형의 높이, 종류");
			int num1 = input.nextInt(); // 첫 번째 정수입력
			int num2 = input.nextInt(); // 두 번째 정수입력
			
			for(int a =0; a<=num1; a++ ) {
				System.out.println("*");
			}
		
		
	
		//------------------------------------------------
			
			
		
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
	}

}
