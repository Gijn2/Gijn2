package b_conclusion;

import java.util.Scanner;

public class Z_recursive {
	public static void main(String[] args) {
		// Review: ASumtest
		// 1~5까지 합 구하기 : 1+2+3+4+5
		
		int sum =0;
		for(int i=1; i<=5; i++) {
			 int exsum = sum;
			 sum = exsum + i;
			 System.out.println(sum+","+exsum+","+i);
		}
		System.out.println(sum);

		// Chapter 1. 재귀호출
		int summ = 0;
		summ = sumFunc(5);
		System.out.println(summ);

		// 1-1. 재귀함수 활용한 Factorial code
		// 5! = 5*4*3*2*1;
		System.out.println("숫자입력 :");
		Scanner input = new Scanner(System.in);
		int fac = 0;
		fac = Fac(10);
		System.out.println(fac);

	}

	// 재기호출: 함수 자신을 계속 불러도 된다.
	static int sumFunc(int i) {
		if( i ==1) {
			return 1;
		}
		return i+ sumFunc(i-1); 
	}

	// Factorial
	static int Fac(int i) {
		if( i ==1) {
			return 1;
		}
		return i* Fac(i-1); // 재기호출: 함수 자신을 계속 불러도 된다.
	}
}
