package 연습문제;
import java.util.Scanner;
public class 입사문제 {
	
	// 2 ------------------------------------------------------
//	public static void main(String[] args) {
//
//		System.out.println("mod1/mod2/max_range: ");
//
//		Scanner input = new Scanner(System.in);
//		int mod1 = input.nextInt();
//		int mod2 = input.nextInt();
//		int max = input.nextInt();
//		
//		int result = solution(mod1, mod2, max);
//		//변수 설정
//		
//		System.out.println("mod1: "+mod1);
//		System.out.println("mod2: "+mod2);
//		System.out.println("max_range: "+max);
//		System.out.println("result: "+result);
//		//출력
//	}
//	//함수 시작
//
//	static int solution(int mod1, int mod2, int max) {
//		int count = 0;
//		for(int i =1;i <= max; i++) {
//			if(i%mod1 == 0 & i%mod2 != 0) {count += 1;
//			}
//		}
//		return count;
//	}

	// 1 ------------------------------------------
	public static void main(String[] args) {

		System.out.println("mod1/mod2/max_range: ");

		Scanner input = new Scanner(System.in);
		int mod1 = input.nextInt();
		int mod2 = input.nextInt();
		int max = input.nextInt();
		
		int result = solution(mod1, mod2, max);
		//변수 설정
		
		System.out.println("mod1: "+mod1);
		System.out.println("mod2: "+mod2);
		System.out.println("max_range: "+max);
		System.out.println("result: "+result);
		//출력
	}
	//함수 시작

	static int solution(int mod1, int mod2, int max) {
		int count = 0;
		for(int i =1;i <= max; i++) {
			if(i%mod1 == 0 & i%mod2 != 0) {count += 1;
			}
		}
		return count;
	}
// 3 --------------------------------------------
}