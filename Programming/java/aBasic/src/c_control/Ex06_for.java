package c_control;

public class Ex06_for {

	public static void main(String[] args) {

		/**
		for(char ch='A';ch<='C';ch++) {
			//for(초기값 ; 조건문 ;증감식) 
			System.out.println(ch);
			// 초기값 -> 조건문 -> T일 경우, {}진행-> 증감식 -> 조건문(반복) -> F일 경우, for문 이탈 
		}
		 */


		// A ~ S
		//		for(char r='A';r<='S';r+=2) {
		//			System.out.println(r);
		//		}


		//1 ~ 10
		int hap = 0;
		for(int i=1;i<=10;i++) {
			//hap = hap++; or hap = hap+1;
			hap += 1;
		}
		System.out.println("합: "+hap);


		// 1부터 100까지 홀수 짝수 합 구하기
		//				int b=0,c=0; // b=짝. c=홀
		//				
		//				for(int a=0;a<=100;a++) {
		//					if(a%2 == 0) {
		//						b += a;
		//					}else if(a%2 != 0) {
		//						c += a ;
		//					}
		//					
		//				}System.out.println(b+","+c);


		//1 ~ 30, 3칸씩 넘기
		//		for(int b=1;b<31;b+=3) {
		//			System.out.println(b);
		//		}







	}

}
