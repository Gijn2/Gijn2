package e_method;
import java.util.Scanner;
public class Ex_09복습2 {
	private static final String String = null;
	public static void main(String[] args) {

		input();
		System.out.println("- 끝 -");
	}

	static void input() {
		System.out.println("두 정수와 알파벳 입력");
		Scanner input = new Scanner(System.in);

		int num1 = input.nextInt();
		int num2 = input.nextInt();
		String alpha = input.next();		

		makeSquare(num1, num2, alpha);
	}
	//역할: 두 정수와 알파벳 문자 하나를 입력받음
	// ex. 3 4 f

	//	static void output(char change) {
	//		System.out.print(change);
	//	}
	//	//역할: 'make square'안에 생성만 문자배열에 저장된문자를 화면출력
	//
	//
	//
	//	static void makeSquare(int num1, int num2, String alpha) {
	//		int[][]ch = new int[num1][num2];
	//		char change = alpha.charAt(0);
	//
	//		for(int i=0; i <num1; i++) {					// 행 반복
	//			for(int j=0;j <num2; j++) {				// 열 반복
	//				//				if(change == 'z'+1|change =='Z'+1)
	//				//				{break;}							// 알파벳 이후의 다른 문자 제외
	//				switch(change) {
	//				case '{': change = 'A'; break;
	//				case '[': change = 'a'; break;
	//				}
	//				ch[i][j] = change;					// 문자 저장
	//				output(change);						// 출력담당 함수
	//				change += 1;						// abcdefg...
	//			}
	//			System.out.println();					// 1행 진행 후 끊어주기
	//		}


	// #1-2 -----------------------------------------------------------------

	static void output(char[][] ch) {

		for(int i=0; i <ch.length; i++) {						// 행 반복
			for(int j=0;j <ch[i].length; j++) {					// 열 반복
				System.out.println(ch[i][j]);
			}
		}

	}
	//역할: 'make square'안에 생성만 문자배열에 저장된문자를 화면출력		

	static char[][] makeSquare(int num1, int num2, String alpha) {
		//	역할: input에서 입력받은 첫번째 정수만큼의 행과 두번쨰만큼의 열의 배열생성, 입력받은 문자로 시작하는 배열을 저장합니다.
		char[][]ch = new char[num1][num2];
		char change = alpha.charAt(0);

		for(int i=0; i <num1; i++) {					// 행 반복
			for(int j=0;j <num2; j++) {					// 열 반복
				switch(change) {						// 알파벳 이후의 다른 문자 제외
				case '{': change = 'A'; break;
				case '[': change = 'a'; break;
				}
				ch[i][j] = change++;						// 문자 저장
			}
		}
		return ch;
	}


}
