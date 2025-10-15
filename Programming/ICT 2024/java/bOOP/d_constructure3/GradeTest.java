package d_constructure3;
import java.util.Scanner;
public class GradeTest {
	public static void main(String[] args) {


		System.out.println("처리할 데이터의 수");
		Scanner input = new Scanner(System.in);
		int length = input.nextInt();

		int [] jumsu = new int [length];
		GradeExpr expr = new GradeExpr(jumsu);

		//추후에 입력받기
		//	int [] jumsu = new int[3];
		//	jumsu[0] = 100;
		//	jumsu[1] = 100;
		//	jumsu[2] = 100;
		//	

		//	System.out.println("총점: "+expr.getTotal());
		//	System.out.println("평균: "+expr.getAverage());

		System.out.println("처리할 데이터만큼의 값을 입력하세요. ex.70,80,90,100");
		for(int i =0;i <jumsu.length; i++) {
			jumsu [i] = input.nextInt();
		}

		System.out.print("점수들: ");
		for(int i =0;i <jumsu.length; i++) {
			System.out.print(jumsu[i]+", ");
		}
		System.out.println();
		System.out.println("총점: "+expr.getTotal());
		System.out.printf("평균: %.2f",expr.getAverage());
		System.out.println();
		System.out.println("최고점: "+expr.getGoodScore());
		System.out.println("최저점: "+expr.getBadScore());


	}
}
