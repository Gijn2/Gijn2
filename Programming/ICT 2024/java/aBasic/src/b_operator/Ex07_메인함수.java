package b_operator;

public class Ex07_메인함수 {
public static void main(String[] args) {
	
	
	int a = 15;
	int b = 10;
	
	int and = a & b;			
		/* 00001111
		   00001010
		   ---------
		   00001010
		   
		   ㄴ and 이므로 두 수가 1인 것들만 걸러짐 다르면 0처리
		 */
	System.out.println(and);
	
	int or = a | b;
	
	/* 
	 
	 00001111
	 00001010
	 ---------
	 00001111
	 
	 답은 15  */
	System.out.println(or);
	
	int xor = a^b;
	System.out.println(xor); // xor : 두 신호가 다른경우에만 결과 발생
	
	/* 
	 
	 00001111
	 00001010
	 ---------
	 00000101
	 
	 답은 5  */
	
	
	
	
}
}
