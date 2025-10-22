package z_recursive;

public class ASumtest {
	public static void main(String[] args) {
		// 1~5까지 합 구하기
		// 1+2+3+4+5
		
		int sum =0;
		for(int i=1; i<=5; i++) {
//			sum += i;
			 int exsum = sum;
			 sum = exsum + i;
			 System.out.println(sum+","+exsum+","+i);
		}
		System.out.println(sum);
	}
}
