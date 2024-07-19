package b_review;
import java.util.Scanner;
public class Main {
	public static void main(String[] args) {

		Product p = new Product();
		Scanner input = new Scanner(System.in);
		
		System.out.println("품번: ");
		p.setProductNo(input.nextInt());
		
		System.out.println("품명: ");
		p.setProductName(input.next());
		
		System.out.println("초기재고량: ");
		p.setStock(input.nextInt());
		
		System.out.println("판매량: ");
		p.sale(input.nextInt());
		p.output();
		
		System.out.println("입고량: ");
		p.income(input.nextInt());
		p.output();
		
	}
	// 함수

}
