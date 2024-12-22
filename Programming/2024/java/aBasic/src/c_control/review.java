package c_control;
import java.util.Scanner;
public class review {
	public static void main(String[] args) {

		//

		String sn = "980620-1234567";
		char g = sn.charAt(0);

		if(g =='9'||g =='0') {
			System.out.println("MZ");
		} else {
			System.out.println("-틀-");
		}

		switch(g) {
		case'8':	System.out.println("젊은이"); break;
		case'9':
		case'0':	System.out.println("청년"); break;
		default: 	System.out.println("정상인");
		}

		// -------------------------------

		Scanner sc = new Scanner(System.in); // 스캐너 객체 생성
		System.out.println("정수 2개 입력");
		int firstNum = sc.nextInt(); // 첫 번째 정수입력
		int secondNum = sc.nextInt(); // 두 번째 정수입력

		for (int i = 0; i < firstNum; i++) { // 0부터 N까지 높이
			if(i % 2 == 0) { // 나머지가 0이면 ---> 방향
				for (int j = (i*secondNum) + 1; j <= (i + 1) * secondNum; j++) {
					System.out.print(j + " ");
				}
				System.out.println(""); // 줄 바꿈
			}
			else { // 나머지가 0이 아니면 <--- 방향
				for (int j = (i + 1) * secondNum; j > (i*secondNum); j--) {
					System.out.print(j + " ");
				}
				System.out.println(""); // 줄 바꿈
			}
		}
		
		
		
	}
}
