package f_exception;
/* 자바는 예외 필수인 애들이 많아서 진짜 중요한 부분
 * try ~ catch ()
 */

public class Ex01_tryCatch {
	public static void main(String[] args) {

		String [] str = {"행복합시다","맛접","맑은정신"};
		try {
			for(int i =0; i < str.length; i++) {
				System.out.println(str[i]);
			}
			// 'for'문에서 이상이 생길 경우, catch문으로 이동
			//			이상이 없을 경우, 마무리하고 return 을 무시하는 finally 문으로
			System.out.println("예외가 발생할거같은 구문");
			return;
		}catch(Exception ex) {
			System.out.println("예외가 발생한 구문 :"+ ex.getMessage());
		}finally {
		//제어권을 가져오는 'return'이 있어도 무조건적으로 실행하는 구문.
			System.out.println("무적건 실행");
		}
		System.out.println("종료");
	}
}
