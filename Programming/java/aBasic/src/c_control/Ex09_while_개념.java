package c_control;

public class Ex09_while_개념 {
/*
 for  : 주로 반복횟수가 정해진 경우,
 while: 주로 반복횟수가 정해지지 않은 경우,
 -- 'for'문을 빡세게 연습하고 'while'로 가는것을 추천
 */
	public static void main(String[] args) {
		
//		int sum = 0;
//		
//		int i =1; // 초기값 따로 빼기
//		for( ;i<=10;) {
//			sum+=i; //증감치 따로 빼기
//			i++;
//		}System.out.println(sum);
//		// 위의 경우도 가능하디, 이 경우 'while'문으로 바꿀 수 있따
//		
//		//초기값은 위에
//		while( i<=10 ) {
//			sum+=i; //증감치 따로 빼기
//			i++;
//		}System.out.println(sum);
		
		//------------------------------------------
		
		int dan = 3; // 구구단의 3단 출력 (입력받을 수 있음) 
		
		int a   = 1;
		while(a<=15) {
			System.out.print(dan*a+" ");
			a++;
			System.out.printf("%d * %d= %d \n");
		}
		
		
		//--------------------------------------
		
	}
	
}
