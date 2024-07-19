package d_array;

public class Ex09_practice {
	public static void main(String[] args) {

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
			int total = 0;
			for(int j =0;j<a[i].length; j++) {

				total += a[i][j];		
			}
			for(int j=1; j< a.length ; j++) {
				 if( max < total) {
					 max = total;
				 }
			 }
		}
		System.out.println("가장 큰 값: " + max);

		// 1. 안에 있는 애들을 더해서 저장 - 4개 필요  2. 안에 있는 값들을 비교 하면서 최대값 거르기
		// 3. 최대값 출력
	}

}






