package b_operator;

import java.util.Scanner;

public class Ex05_비교연산자 {
	public static void main(String[] args) {

		/* ****************************
	 		>  >=  ==  <=  <  !=(같지않다)
		 */

		System.out.println("국어점수");					//print(내부는 문장은 무조건 따옴표)
		Scanner input = new Scanner(System.in);		// 스캐너 오류? 대소문자 구문 철저히
		int a = input.nextInt();					// int -> nextInt / Spring -> nextLine / float -> nextDouble

		System.out.println("수학점수");
		Scanner input1 = new Scanner(System.in);	// input 변수가 중복되지 않도록
		int b = input1.nextInt();					// input1로 실수했을시, 잊지않고 변환

		System.out.println("영어점수");
		Scanner input2 = new Scanner(System.in);
		int c = input2.nextInt();

		System.out.println("총점 = "+ (a+b+c)); 		// 괄호 잊지 말기. 아니면 숫자 연속으로 표현함
		System.out.println("평균 = "+((a+b+c)/3 ) );	

		// 정수가 아닌 소수점을 원한다면 double형 으로 바꾸고(double)

		int ave = ((a + b + c)/3);

		if(ave >= 90) {
			System.out.println("A");			
		}else if(ave >= 70){
			System.out.println("B");
		}else if(ave >= 50) {
			System.out.println("C");
		}else {
			System.out.println("F");
		}

		
		/** #2
		int ave = ((a + b + c)/3);

		if(ave >= 70) {					// 첫번째가 우선순위, 70보다 높은 모든 점수가 첫 조건에 맞춰지므로 주의
			System.out.println("F");				
		}else if(ave >= 80){
			System.out.println("C");
		}else if(ave >= 90) {
			System.out.println("B");
		}else {
			System.out.println("A");
		}
		*/

		
		



}
}

