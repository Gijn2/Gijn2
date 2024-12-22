package y_useful;

import java.util.Scanner;
import java.util.StringTokenizer;

public class StringTokenizer샘플 {

	public static void main(String[] args) {
		
		System.out.println("문장 입력");
		Scanner input = new Scanner(System.in);
		//문장 입력
		
		String sent = input.nextLine();
		//.next는 입력문자 중 " " 앞에서 끊음, .nextLine은 String 안의 모든 문자 들음
		StringTokenizer st = new StringTokenizer(sent);
		//'sent'라는 변수를 토크나이저에 설정
		
		while(st.hasMoreTokens()) {
			System.out.println(st.nextToken());
		}
		/* st.hasMoreTokens()= 안에 내용물이 있다면
		 * System.out.println(st.nextToken()
		 * " "마다 끊어서 출력
		 */
		
		StringTokenizer st1 = new StringTokenizer(sent,"/");
		// "/" 마다 문장을 끊어준다.
		
		/* 
		 * st.hasMoreTokens()를 사용할 경우, 'while'문 사용
		 * st.countTokens  ()를 사용할 경우, 'for'문 사용
		 */

		
	}

}
