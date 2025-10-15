package c_control;

public class Ex12_Break_Continue {
	public static void main(String[] args) {

		Jump:										//만약 전부 스킵하고싶을 경우, 구간을 설정 **눈에 잘 띄게 설정해놓기
		for(int i =0; i<2; i++) {
			
			for(int j =0; j<3; j++) {
				if(j ==3) {
					break Jump;						// 3일때, } ...("데이터");}로 	-> for 문 탈출
													// 구간을 탈출하고 싶으면 break 뒤에 Jump(구간명) 붙혀주기/ 구간 제일 끝으로 가려면 continue 뒤에~
				}
				if(j ==1) {
					continue;						// 1일때, (i+", "+j);의 뒤로 	-> for 문 내부
				}
				System.out.println(i+", "+j);
			}
			System.out.println("데이터");
		}

		// break   : 블럭을 벗어나는 문장. (switch)
		// continue: 블럭의 끝으로 가라.
		
		
		
		
		
		
		

	}
}
