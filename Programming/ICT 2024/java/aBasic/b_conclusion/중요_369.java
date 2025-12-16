package b_conclusion;

public class 중요_369 {
	public static void main(String[] args) {

		// 1~50 숫자쭝 3.6.9를 포함하면 '짝' 출력

		//	System.out.println("숫자입력");
		//	Scanner input = new Scanner(System.in);
		//	String num = input.nextLine();
		//	StringTokenizer st = new StringTokenizer(num);

		for(int i =0;i<=50;i++) {
			//'for'문 반복 
			int su = i;
			//'su'는 반복횟수
			boolean su369 = false;

			while(su!=0) {
				//'su'가 0이 아니면
				int na = su%10;
				if(na==3||na==6||na==9) {
					System.out.print("짝");
					su369 = true;
				}	
				su/=10;
				// 반복횟수/10의 나머지'n'이 3,6,9면 "짝" 출력하고 논리는 True
				// 10이되면 나머지는 0이니까 탈출한다. -> /10을 해서 반복횟수를 0으로 
			}
			if(!su369) {
				System.out.println(i);
			}else {
				System.out.println();
			}
		}
		/*
		 * for   문: 1~50까지 반복
		 * while 문: 반복횟수가 0이 아니면 T, 10으로 나눈 나머지가 369이면 출력,True
		 * 
		 * ex)  su ==1 -> T(진입) -> 1(su)%10 = 1(na) -> (na)if에 안걸림
		 * 		 -> 1/10 = 0 -> while 조건문 탈출
		 * 		if 문: 나머지/10이 0이되어 탈출 후, 'su369'가 false 상태에서
		 *            !su369는 이중부정으로 True가 되어 숫자 출력
		 *            		ㄴ (System.out.println(i);)
		 *            
		 * 		su ==3 -> 3 != 0, T(진입) -> 3(su)%10=3(na)
		 * 		-> na = 3, if문에 걸림(T) -> "짝" 출력, su369 = T
		 * 		-> 3(su)/10 = 0 -> while 조건문 탈출
		 * 		if 문: su369가 T가 된 상태에서 부정명령어로 인해 F로 되어 한줄 넘김
		 * 					ㄴ (System.out.println();)
		 */

		



	}
}
