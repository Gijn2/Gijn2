package e_method;

public class Ex03_인자와반환 {
	public static void main(String[] args) {

		int a =10,b = 20;
		int sum = add(a,b);

		System.out.println(sum);	
	}
	static int add(int a, int b) {
		int sum = a + b;
		return sum;
	}

}
