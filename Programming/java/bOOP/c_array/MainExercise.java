package c_array;

import java.util.Scanner;

public class MainExercise {

	public static void main(String[] args) {


	
		System.out.println("입력할 학생의 수: ");
		Scanner input = new Scanner(System.in);
		int head = input.nextInt();
		Student [] s = new Student [head];
		
		for(int i = 0; i <s.length; i++) {

			s[i] = new Student();
			
			System.out.println("이름 입력: ");
			s[i].setName(input.next());
			System.out.println("영어점수입력: ");
			s[i].setEng(input.nextInt());
			System.out.println("국어점수입력: ");
			s[i].setKor(input.nextInt());
			System.out.println("수학점수입력: ");
			s[i].setMath(input.nextInt());
		}
		for(int i = 0;i < s.length; i++){
		System.out.println("이름: "+s[i].getName()+", 총점: "+s[i].calTotal()+", 평균: "+s[i].calAvg());
		}
	}
}