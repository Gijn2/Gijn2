package c_control;

import java.util.Scanner;

public class Ex08_for_중첩2 {
	public static void main(String[] args) {

		//		// 알파벳 A-Z
		//		for(int a1=1;a1<=26;a1++) {
		//			for(char a='A';a<='Z';a++) {
		//
		//				System.out.print(a);
		//			}	// A-Z 출력
		//			System.out.println(); // 줄 변경
		//		} //26번 반복


		// -----------------------------------


//		for(int a1=0;a1<26;a1++) {
//			for(char a='A';a<='A'+a1;a++) {
//
//				System.out.print(a);
//			}	// A-Z 출력
//			System.out.println(); // 줄 변경
//		} //26번 반복
//
//
//
//		for(int a1=0;a1<26;a1++) {
//			for(char a='A';a<='Z'-a1;a++) {
//
//				System.out.print(a);
//			}	// A-Z 출력
//			System.out.println(); // 줄 변경
//		} //26번 반복
//
//
//		//----------------------------------------
//
//		for(int a2=0;a2<26;a2++) {
//			for(char a3='Z';a3>='Z'-a2;a3--) {
//				System.out.print(a3);
//			}
//			System.out.println();
//		}
//
//
//		//----------------------------------------
//
//
//		char b = 'A';
//
//		for(int a4=0;a4<26;a4++) {
//			for(char a5= b;a5<='Z';a5++) {
//				System.out.print(a5);
//			}								// A-Z 출력
//			System.out.println(); 			// 줄 변경
//			b += 1; 						// 'A'자리 하나씩 뒤로
//
//		} //26번 반복
//
//
//		//---------------------------------------------------
//
//		System.out.println("높이");
//		Scanner input6 = new Scanner(System.in);
//		int a6 = input6.nextInt();
//
//		System.out.println("너비");
//		Scanner input7 = new Scanner(System.in);
//		int a7 = input7.nextInt();
//		int c6 = 0;
//
//		for(int b6 =1;b6<=a6; b6++) {
//			for(int b7=1;b7<=a7;b7++) {
//				System.out.print(b7+(a7*c6));
//			}System.out.println();
//			c6 +=1;
//		}
//
//
//		// ------------------------------------------------
//
//		System.out.println("정사각형 한 변의 길이 :");
//		Scanner input8 = new Scanner(System.in);
//		int a8 = input8.nextInt();
//
//		int c8 = 0;
//
//		for(int b8 =1;b8<=a8; b8++) {
//			for(int b9=1;b9<=a8;b9++) {
//				System.out.print(b9+(a8*c8));
//			}System.out.println();
//			c8 +=1;
//		}

		//---------------------------------------------------

		System.out.println("높이");
		Scanner input10 = new Scanner(System.in);
		int a10 = input10.nextInt();					// 높이

		System.out.println("너비");
		Scanner input11 = new Scanner(System.in);
		int a11 = input11.nextInt();					// 너비
		int c10 = 0;									// 행(높이)의 번호
		
		
		for(int b10 =1;b10<=a10; b10++) {				// 
			if(c10%2==0) {
				for(int b11=1;b11<=a11;b11++) {
					System.out.print(b11+(a11*c10));
				}System.out.println();
				c10 +=1;
			}
			if(c10%2!=0) {
				for(int b11=a11;a11>=b11&b11>0;b11--) {
					System.out.print(b11+(a11*c10));
				}System.out.println();
				c10 +=1;
			}
		} 
		
		// for 안의 변수는 i로, for문 안의 for문은 i다음 알파벳(j,k,l,m,...)으로 쭉쭉..
		
		//---------------------------------------------------------
		
		
		
		

	}
}
