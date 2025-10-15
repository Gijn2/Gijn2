package c_array;

import java.util.Scanner;

public class Main {
	public static void main(String[] args) {
		// 3명의 학생의 점수를 입력받아서 총점과 평균 구하기
		
		Student [] s = new Student [3];
		// 학생의 이름을 배열로 저장하기 위해, new 배열로 가져와 학생 수 공간 잡기
		
		Scanner input = new Scanner(System.in);
		
		for(int i = 0; i <s.length; i++) {
			System.out.println("이름 입력: ");
			
			s[i] = new Student();
			/** **** 아주아주 중요합니다. *************
			 * 클래스의 배열인 경우, 배열과 클래스 둘 다 가져와야한다.
			 * 배열도 new 로 생성해줘야함. & class 도 new 로 생성해줘야한다.
			 */
			
			s[i].setName(input.next());
			
			System.out.println("영어점수입력: ");
			s[i].setEng(input.nextInt());
			System.out.println("국어점수입력: ");
			s[i].setKor(input.nextInt());
			System.out.println("수학점수입력: ");
			s[i].setMath(input.nextInt());
			
			System.out.println("총점"+s[i].calTotal());
		}
		
		
	}
}
