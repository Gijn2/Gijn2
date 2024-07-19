
package f_exception;

public class Ex04_throw {
	public static void main(String[] args) {
		try {
			readArray();
		}catch(Exception ex) {
			System.out.println("예외처리: "+ex.getMessage());
		}
	}
	//함수 시작
	static void readArray() throws Exception{
		String []msg = {"안녕","잘가","또 보자"};
		try{
			for(int i =0; i <=msg.length; i++) {
				System.out.println(msg[i]);
			}
		}catch(Exception ex){
			throw new Exception();
			// 일부러 오류를 내는 이유: 문제가 발생하면 생기는 위치를 빠르게 알기위해서(개발자가 편하기 위해)
			// 예외를 직접 발생시킬때는 throw,
			// 일부러 발생시킨 경우가 아미녀 throws


		}
	}
}