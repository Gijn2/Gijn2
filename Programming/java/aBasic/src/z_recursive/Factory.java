package z_recursive;
import java.util.Scanner;
public class Factory {
public static void main(String[] args) {
	
	// 5! = 5*4*3*2*1;
	System.out.println("숫자입력 :");
	Scanner input = new Scanner(System.in);
	int fac = 0;
	fac = Fac(10);
	System.out.println(fac);
	}
	static int Fac(int i) {
		if( i ==1) {
			return 1;
		}
		return i* Fac(i-1); // 재기호출: 함수 자신을 계속 불러도 된다.
}

}
