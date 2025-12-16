package e_method;
import java.util.Scanner;
public class Ex_09연습 {
	public static void main(String[] args) {

		String result = func();
		System.out.println(result);
		method(result);
	} 
	//함수의 역할: 콘솔 창을 통해서 점수를 입력받을 거야.
	// 입력받은 점수가 80이성이면 합격, 아니면 반환
	
	// func 함수
	static String func() {

		Scanner input = new Scanner(System.in);
		System.out.println("점수입력");
		int score = input.nextInt() ;

		if(score>=80) {
			return "합격";
		}else {
			return "불합";
		}
	}
	
	// method 함수
	static void method(String result) {
	// 	리턴변수의 자료형		입력변수의 자료형
	
		
	
	}
	
	
	
	// 함수 끝
}