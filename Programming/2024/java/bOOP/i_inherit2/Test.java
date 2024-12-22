package i_inherit2;
import java.util.Scanner;
public class Test {
	public static void main(String[] args) {
		
		Item i = null;
		
//		System.out.print("1.Book 2.Cd 3.Dvd / 번호입력: ");
//		Scanner input = new Scanner(System.in);
//		int a = input.nextInt();
//		
//		switch(a){
//		case 1:
//			i = new Book(); break;
//		case 2:
//			i = new Cd(); break;
//		case 3:
//			i = new Dvd(); break;
//		}
//		
//		i.output();
	
			
			Book b = new Book("001","자바책","김씨","서강대");
			b.output();


	}
}
