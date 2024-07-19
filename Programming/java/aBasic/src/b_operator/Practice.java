package b_operator;

import java.util.Scanner;		// 스캐너 사용할 때, 이거 꼭 선언해주기

public class Practice {

	public static void main(String[] args) {

		/*
		학생점수를 입력받아 100만점 중 80~90사이라면 '평균', 
		1. 학생점수 변수 선언
		2. scanner
		3. 점수입력 문장출력
		4. 입력값을 학생점수 변수에 저장
		5. 입력값이 80보다 크고 90보다 작다면 '평균 출력'
		

		 */
		
		
		System.out.println("점수입력");

		Scanner input = new Scanner(System.in);
		int score = input.nextInt();
		
		if(score>100 || score <0) {
			System.out.println("잘못입력된 점수");
		}else if(score>80 & score<90) {
			System.out.println("평균");
		}else {
			System.out.println("평균아님");
		}
		
		/*
		String a = "점수";
		score>=80 & score<=90 ? a=="평균":a=="비평균" ;  
		*** 에러코드 = if else 문으로 바꿔라
		
		왜 이렇게는 안되는 걸까?
		
		-----------------------------------------------------------------
		[참고]
		파일을 읽기위해 컴파일이 필요
		java 버츄얼 머신
		
		코딩 실행시, f11만 누르면 디버깅모드가된다(오류잡는 용도)
		
		*/
		
		
		
		
		
		
	}

}
