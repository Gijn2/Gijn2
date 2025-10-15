package k_rapper;
/*
 * 기본형 							   int		 boolean    char       double
 * wrapper class(자료형을 처리하는 클래)   integer   Boolean    Character  Double	
 */

public class Test {
	public static void main(String[] args) {
		Object[] obj = method();
		for(int i =0;i <obj.length;i++) {
			System.out.println(obj[i]);
		}
	}
	static Object[] method() {
		String name	  = "홀길동";
		int    age	  = 30;
		double height = 180.99;
		
		Object [] obj = new Object[3];
		obj [0] = name;
		obj [1] = age; 		// int -> integer 변환이 자동으로 이루어진다.
		obj [2] = height;
		return obj;
	}
}
