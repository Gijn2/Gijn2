package 연습문제;
import java.util.Scanner;

public class test {
	int  i;
	public static void main(String[] args) {


		//        char[][] a1 = input(); //이차배열 a1은 input임
		//	        output(a1);
		//	    } 
		//	    
		//
		//	    static char[][] input() { //반환 값이 이차배열이니 이차배열로 생성 ~ 
		//	        
		//	        Scanner s = new Scanner(System.in);
		//	        System.out.println("두 정수와 알파벳 문자 하나를 입력해 주세요. = >");
		//	        int a = s.nextInt();
		//	        int b = s.nextInt();
		//	        String c = s.next();
		//	        
		//	        return makesquare(a, b, c.charAt(0)); //반환값은 makesquare에서 계산된 값임. a,b,c도 동시에 전달해줍니다.
		//	     
		//	    }
		//
		//	    static char[][] makesquare(int a, int b, char c) {
		//
		//	        char[][] ch = new char[a][b];
		//
		//	        for (int i = 0; i < a; i++) {
		//	            for (int j = 0; j < b; j++) {
		//	                ch[i][j] = c++;
		//	            }
		//	        }
		//
		//	        return ch; // 완성된 이차배열 ch 반환
		//	    }
		//
		//	    static void output(char[][] ch) { //출력을 위해서 반환된 ch 가져옴
		//	        for (int i = 0; i < ch.length; i++) {
		//	            for (int j = 0; j < ch[i].length; j++) {
		//	                System.out.print(ch[i][j] + " ");
		//	            }
		//	            System.out.println();
		//	        }
		//	    }
		//	 //input의 반환 값이 makesquare 이니 makesquare에서 만들어진 ch는 ai이 됩니다. (ai = input() 이니)
		//	    
		//	} 
			    
		//	1---------------------------------------
		//		void subtract{int x, int y}{		
		//		
				
		//	2----------------------------------------
		//			System.out.println("숫자입력");
		//			Scanner input = new Scanner(System.in);
		//			int a = input.nextInt();
		//			
		//			greeting(a);
		//			
		//	}
		//
		//		
		//	
		//	//2
		//	static String greeting(int a) {
		//		switch(a) {
		//		case 1: return "안녕하세요";
		//		case 2: return "hello" ;
		//		case 3: return "hola";
		//		case 4: return "곤니치와";
		//		default: return "";
		//		}
		//		
		//	}
		//	
		//	//3
		//	
		//	
		//	//4
		//	static double circle(int a) {
		//		double square = a*a*3.14;
		//		return square;
		//	
		//	}
		//	
		//	//5
		//	static void square(int a, int b){
		//	



		// 추가연습 - 별삼각형

		//		System.out.println("높이, 종류(1~3)");
		//		Scanner input = new Scanner(System.in);
		//		int num1 = input.nextInt();
		//		int num2 = input.nextInt();
		//
		//		switch(num2) {
		//		case 1 :
		//			for(int i=0; i<num1; i++) {
		//				for(int j=num1; j-i<=num1 ;j++) {
		//			System.out.println();
		//					System.out.print("*");
		//				}
		//				} break;
		//		case 2 :
		//			for(int i=0; i<num1; i++) {
		//				for(int j=1; j+i<=num1 ;j++) {
		//					System.out.print("*");
		//				}
		//				System.out.println();
		//			} break;
		//		case 3 :
		//			for(int i=0; i<num1; i++) {
		//				for(int j=1;j+i<num1;j++) {
		//					System.out.print(" ");
		//				}
		//				for(int j=1; j<=2*i+1 ;j++) {
		//					System.out.print("*");
		//				}
		//				System.out.println();
		//			} break;
		//		default: System.out.println("잘못된 숫자입니다.");
		//		}


		//[방탈출]	 0 ~ 10000까지 수에 포함된 숫자8의 개수 세는 법.

		//		int count = 0;				// 숫자셀변수
		//		for(int i =0;i<=10000; i++) {
		//			int su = i;
		//									//'su'는 반복횟수
		//			while(su!=0) {
		//				int na = su%10;
		//				if(na==8) {
		//					count += 1;
		//				}	
		//				su/=10;
		//			}
		//
		//		}System.out.println(count);


		// 자연수 n을 입력받아 출력 예시와 같이 공백으로 구분하여 출력
		// #1

		//		System.out.println("자연수 입력 :");
		//		Scanner input = new Scanner(System.in);
		//		int num = input.nextInt();
		//
		//		for(int i=0; i<num; i++) {
		//			for(int j=0; j<num-i; j++) {
		//				System.out.print(" ");
		//			}
		//			for(int j=1; j<=i+1; j++) {
		//				System.out.print(j);
		//			}
		//			System.out.println();
		//		}


		// #2

		//		System.out.println("자연수 입력 :");
		//		Scanner input = new Scanner(System.in);
		//		int num = input.nextInt();
		//		int store = 0;
		//				
		//		for(int i=0; i<=num; i++) {
		//			for(int j=num-i; j<num; j++) {
		//				System.out.print(" ");
		//			}
		//			for(int j=1+i; j<=num; j++) {
		//				store += 1;
		//				System.out.print(store);
		//			}
		//			System.out.println();
		//		}


		// #3
		//		
		//		System.out.println("자연수 입력 :");
		//		Scanner input = new Scanner(System.in);
		//		int num = input.nextInt();
		//		int store = 0;
		//		char alpha = 'A';
		//				
		//		for(int i=0; i<num; i++) {
		//			for(int j=0; j<num-i; j++) {
		//				System.out.print(alpha);
		//				alpha += 1;
		//			}
		//			for(int j=0; j<i; j++) {
		//				System.out.print(store);
		//				store += 1;
		//			}
		//			System.out.println();
		//		}


		// #4
		
		
		
		
		// 3/11 ------------------------------------------------------------
		
		
		
	
	

	}
}
