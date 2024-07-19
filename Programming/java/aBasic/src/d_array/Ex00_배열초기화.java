package d_array;

public class Ex00_배열초기화 {
public static void main(String[] args) {
	
	/*여러개의 값을 출력하고싶을 경우, 하나하나 저장하는 것보다 하나의 변수에 인덱스라는 공간에 넣어서 보관하는게 더 편리하다
	  이럴 경우, 반복문 반복변수를 통해서 저장
		
		String을 제외하고 대부분의 값에 반복변수를 넣을수 있다.
	*/
	
	// 배열변수 선언 +  배열객체 생성
			 //int [] kor = new int[5];
			 
			// 배열초기화
			// int [] kor = new int[] {99,88,77,66,55};
			int [] kor = {99,88,77,66,55}; 
			
			// 			값지정
			//			kor[0] = 99;
			//			kor[1] = 88;
			//			kor[2] = 77;
			//			kor[3] = 66;
			//			kor[4] = 55;
			 
			 int total = 0;
			 for( int i=0; i < 5 ; i++) {
				 total += kor[i];
			 }
			 
			 System.out.println("총점:" + total);
	
	
	
	// -----------
	
	int[][] data = new int[3][2];
	
	for(int i=0; i<3; i++) {
		for(int j=0; j<2; j++) {
			data[i][j] = (int)(Math.random()*10);
		}
	}
	
	for(int i = 0; i <data.length; i++) {
		for(int j =0; j <data[i].length; j++) {
			System.out.print(data[i][j]+" ");
		}
		System.out.println();
	}
	
	// ----------------------
	
	int [][] lotto = new int[5][6];

	// 로또번호 생성
	
	// 정렬
	
	// 출력
	
	
	
	
	
	
	
}
}
