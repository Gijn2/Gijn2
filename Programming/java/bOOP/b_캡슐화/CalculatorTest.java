package b_캡슐화;

import java.util.Scanner;

public class CalculatorTest {

	public static void main(String[] args) {

		CalculatorExpr cal = new CalculatorExpr();

		String answer = "";
		do{
			System.out.println("num1, num2 입력: ");
			Scanner input = new Scanner(System.in);
			int num1 = input.nextInt();
			int num2 = input.nextInt();
			
			//cal.num1 = num1이 안되므로
			cal.setNum1(num1);
			cal.setNum2(num2);

			System.out.println("덧셈: "+ cal.getGetAddition());
			System.out.println("뺄셈: "+ cal.getGetSubtraction());
			System.out.println("곱: "+cal.getGetMultiplication());
			System.out.println("나눔: "+ cal.getGetDivision());

			System.out.println("반복?");
			answer = input.nextLine();
			
			if(answer.equals("n")|answer.equals("N")) {
				break;
			}
			
		}while(answer.equals("y")|answer.equals("Y"));


	}

}
