package d_exercise;

public class Main1 {

	public static void main(String[] args) {
	
	
		Customer cus = new Customer();
		
//		cus.tel = "010-1234-1234";
//		cus.name = "홍길순";
//		cus.m = 10000;
		
		cus.output();
		
		String tel = cus.getTel();
		String name = cus.getName();
		int m = cus.getM(); 
		
	}

}
