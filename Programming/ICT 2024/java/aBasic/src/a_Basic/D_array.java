package a_Basic;

public class D_array {
public static void main(String[] args) {
	
	// Chapter 1. 배열초기화

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
	
	// Practice
			//		char[][]star = new char [4][4]; // 4행 4열만큼의 공간 확보
		//
		//		/* ex.
		//		 * 스택 영역과 힙 영역
		//		 * - 스택 영역
		//		 * 		ㄴ star라는 공간 확보 
		//		 * 
		//		 * -힙 영역
		//		 *  ㄴ 메모리의 4개의 공간 생김
		//		 *  star가 찾아갈 수 있음. 공간의 번호는 순서대로 [0] [1] [2] [3]의 번호가 매겨짐
		//		 *  						 // 해당 칸의 길이는 3
		//		 *  ㄴ 각 번호 안에 4개의 공간이 생김. // [4] [4]
		//		 */
		//
		//		// 각각의 캐릭터 공간에 '*' 넣기
		//		
		//		for(int i =0; i <star.length; i++) {				// 'star'의 행 길이
		//			for(int j =0; j <i+1; j++) {	
		//				star[i][j] = '*';
		//			}		
		//		}
		//		
		//		// 출력 **2차원이면 for문 2개, n차원이면 for문이 n개 만들어야함
		//
		//		for(int i =0; i <star.length; i++) {				// 'star'의 행 길이
		//
		//			for(int j =0; j <star[i].length; j++) {			// 'star'의 열 길이
		//				System.out.print(star[i][j]+" ");
		//
		//
		//			}System.out.println();
		//		}

		// --------------------------------------------------

		char[][]star = new char [4][]; // 일단 4행만 줘

		/* ex.
		 * 스택 영역과 힙 영역
		 * - 스택 영역
		 * 		ㄴ star라는 공간 확보 
		 * 
		 * -힙 영역
		 *  ㄴ 메모리의 4개의 공간 생김
		 *  star가 찾아갈 수 있음. 공간의 번호는 순서대로 [0] [1] [2] [3]의 번호가 매겨짐
		 *  						 // 해당 칸의 길이는 3
		 *  ㄴ 각 번호 안에 4개의 공간이 생김. // [4] [4]
		 */

		// 각각의 캐릭터 공간에 '*' 넣기


		for(int i =0; i <star.length; i++) {				// 'star'의 행 길이

			star [i] = new char[i+2];						// 열은 내가 추가할게
			// star [i]행에 [i+1]만큼의 열 추가

			for(int j =0; j <i+1; j++) {	
				star[i][j] = '*';
				star[i][j+1] = 'a';
			}		
		}

		// 출력 **2차원이면 for문 2개, n차원이면 for문이 n개 만들어야함

		for(int i =0; i <star.length; i++) {				// 'star'의 행 길이

			for(int j =0; j <star[i].length; j++) {			// 'star'의 열 길이
				System.out.print(star[i][j]+" ");


			}System.out.println();
		}

		// 4 4 1
		//-----------수정 중------------------------------------------

		int a[][]=new  int[][]{{3,-5, 12 }, {-2, 11, 2, -7}, {21, -21, -35, -93, -11}, {9, 14, 39, -98}};
		int max = 0;
		
		for(int i =0; i <a.length; i++) {
			int totaL = 0;
			for(int j =0;j<a[i].length; j++) {

				totaL += a[i][j];		
			}
			for(int j=1; j< a.length ; j++) {
				 if( max < totaL) {
					 max = totaL;
				 }
			 }
		}
		System.out.println("가장 큰 값: " + max);

		// 1. 안에 있는 애들을 더해서 저장 - 4개 필요  2. 안에 있는 값들을 비교 하면서 최대값 거르기
		// 3. 최대값 출력
	
	
	
	
	
}
}
