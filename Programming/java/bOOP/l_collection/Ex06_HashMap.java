package l_collection;

import java.util.HashMap;
import java.util.Scanner;

public class Ex06_HashMap {
	public static void main(String[] args) {
		HashMap<String,String> map = new HashMap<String,String>();
		map.put("javassem", "1");
		map.put("kimssem", "9999");
		map.put("kimbabo", "1234");
		map.put("kimbab", "23");
		map.put("javassem", "567");
		// 키가 중복되면 덮어져버려버림.. = 키값은 중복되지않는다

		Scanner input = new Scanner(System.in);

		boolean stop = false;
		while(!stop) {
			System.out.println("아이디 비번 입력");
			System.out.println("아이디입력: ");
			String ID = input.next();
			System.out.println("비밀번호입력: ");
			String PW = input.next();

			// 입력받은 아이디가 저장부분 key 값에 있는지
			if(map.containsKey(ID)) {
				//2-1 입력한 해당 key 값의 value 값과 입력한 비밀번호가 같다면
				if( (map.get(ID)).equals(PW) ) {
					System.out.println("로그인 성공");
					break;
				}else {
					System.out.println("비밀번호 틀림");
					continue;
				}
				
			}else {
				//입력받은 아이디가 저장 아이디에 없음
				System.out.println("없는 아이디");
				continue;
				
			}
		}
	}
}
