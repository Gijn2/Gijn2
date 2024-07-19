package e_method;
import java.util.Scanner;
import java.util.StringTokenizer;
public class Ex_09연습3 {
public static void main(String[] args) {
	
	
	int scr[] = input();
	int say[] = getCalc(scr);
	output(say);
	
	
}
// 함수
// 역할: 국영수 점수 입력받기
static int[] input() {
	Scanner input = new Scanner(System.in);
	System.out.println("국영수 점수 입력 ex.100/100/100");
	String score = input.nextLine();
	StringTokenizer st = new StringTokenizer(score,"/");
	int kor = Integer.parseInt(st.nextToken());
	int eng = Integer.parseInt(st.nextToken());
	int math = Integer.parseInt(st.nextToken());
	
	int[]scr = {kor,eng,math}; 
	
	return scr;
}

//역할: 입력값은 국영수 점수로 총점과 평균을 구해서 출력
static int[] getCalc(int[] scr) {
	int total = 0;
	for(int t =0; t <scr.length; t++) {
		total += scr[t];	
	}
	int avg = total/scr.length;
	int say[] = {total,avg};
	return say;
}

//평균값 받아서 학점 구하기
static void output(int[] say) {
	
	if(say[1] >= 90) {
	System.out.println("평균값: "+say[1]+", A");
	}else if(say[1]>=70) {
		System.out.println("평균값: "+say[1]+", B");
	}else {
		System.out.println("평균값: "+say[1]+", F");
	}
}
}
