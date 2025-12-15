package a_datatype;

import java.util.Scanner;

public class test {

	public static void main(String[] args) {

		// 2/27일자 메모

		/* 카페 시험 답
		1,5 -> 한글 사용가능 - 아스키코드 와 유니코드 비교, 결론 - 자바는 유니코드라 영어 제외한 문자도 가능
		3,4,5 -> 명명규칙 생각해보기
		3 -> 5번 소문자 this는 키워드이므로 사용불가
		2 -> main은 키워드가 아닌 함수이다.
		2 -> new는 키워드 이므로 불가

		- 썜추천 - 깃블로그 or 다른 블로그들을 사용해봐라... */

		byte aa = 64;
		byte bb = 64;
		int result = aa+bb;

		// 3 몰루.., 2
		// 3번 문제 4번 -> 마지막 byte 키워드 대신 int로 수정해야댐
		//4번 36 36

		byte cc = 36;
		int dd = (int)cc;


		//5 360,104 -> ()를 써줌으로써 2^7으로 바뀜 **360은 2진법으로 9칸 -> 7칸으로 바뀌며 두칸에 해당되는 숫자 인식 x
		int ii = 360;
		byte bbb = (byte)ii;

		//6 5번 아니면 1번?인데 5번같음
		byte ee = 127;
		int var = (int)ee;

		String s = "안녕하세요";

		/*
		3 
		2
		4 		 -> 해설 byte int로 수정해야댐
		36 , 36 byte 에 byte를 씌우면 자리수 변동없다
		360, 104 -> 해설 360은 이진법으로 9자리수, int는 4bit로 360보다 공간이 크지만
		 			1byte는 127까지 이므로 자리수가 2의 7승으로 7자리만 나온다 
		 			따라서 두 공간이 사라짐/ 9자리수 ->7자리수까지의 숫자만 처리되어 104
		 			ㄴ360 101101000
		 			ㄴ104   1101000
		2, 3, 5
		 */


		// 2/28일자 메모

		/*
		- 위의 답안 풀이
		1. 해설
		ㅁㅁㅁㅁㅁㅁㅁ -> 1byte = 1bit
		ㅁ의 공간에 0, 1 저장 고로 2가지를 7개의 공간에 저장가능 (2^7)

		양수,음수 -> - 2^7 ~ + 2^7-1 (3)번
		[2진수]

		[16진수]: 2진법 표기가 너무 길어서 4개씩 묶음
		0~9/ A(10) B(11) C D E F(15)

		2. 해설
			1. int 1 = 12345678
			2. float f = 3.5; -> double로 or 3.5F; or float = (float)3.5
			3. 문제 x
			4. string s = ""; -> 문제 x, 문자열을 처리하는 친구
				ㄴ char = 'z'; 문자는 작은따옴, string = "z"; 문자열은 큰따옴


		3. 해설
		애초에 64 + 64 = 128이라 byte로 처리가 안됨(byte: -128 ~ 127)
		int를 사용하여 처리해준다
		byte result = (byte)(a+b);로도 처리가능

		 **음수를 1의 보수식 이란걸로 음수로 인식해서 -128이 나온다

		 */

		/**
		String b = ""; //문.이과
		String c = ""; //학과

		System.out.println("학번 10자리를 입력하세요");
		Scanner input = new Scanner(System.in);
		String Num = input.nextLine();
		int a = Num.length();

		String year = Num.substring(0, 4);
		String loot = Num.substring(4,5); // char, charAt으로 쓸 수 있다.
		String major = Num.substring(5, 7);

		if(loot.equals("1")) {
			b="공학계";
			if(major.equals("11")) {
				c="컴퓨터학과";
			}else if(major.equals("12")){
				c="소프트워어학과";
			}else if(major.equals("13")){
				c="모바일학과";
			}else if(major.equals("22")){
				c="자바학과";
			}else if(major.equals("33")){
				c="서버학과";
			}
		}else {
			b="인문계";
			if(major.equals("11")) {
				c="사회학과";
			}else if(major.equals("12")){
				c="경영학과";
			}else if(major.equals("13")){
				c="경제학과";
			}
		}

		System.out.println(Num+"은"+year+"년도에 입학한"+b+c+"학생입니다");
		// 굳이 년도를 따로 넣을 필요는 없었다. 숫자하나만 볼 때는 char 사용.

		*/
		
		//*************************************************
		
		/**
		
		System.out.println("숫자1을 입력하세요");
		Scanner input1 = new Scanner(System.in);
		int n1 = input1.nextInt();
		
		System.out.println("숫자2를 입력하세요");
		Scanner input2 = new Scanner(System.in);
		int n2 = input2.nextInt();
		
		System.out.println("숫자3을 입력하세요");
		Scanner input3 = new Scanner(System.in);
		int n3 = input3.nextInt();
		
		int result1 = 0;
		
		if(n1==n2&&n2==n3) {
			System.out.println("두번째로 큰 수는 없습니다.");
		}else if(n1>=n2 & n1>=n3) {
			result1 = (n2>=n3)? n2: n3;
			if(n1==n2) {result1 = n3;}
			if(n1==n3) {result1 = n2;}
			
		}else if(n2>=n1 & n2>=n3){
			result1 = (n1>=n3)? n1: n3;
			if(n1==n2) {result1 = n3;}
			if(n2==n3) {result1 = n1;}

		}else if(n3>=n1 & n3>=n2){
			result1 = (n1>=n2)? n1: n2;
			if(n1==n3) {result1 = n2;}
			if(n2==n3) {result1 = n1;}
				
		}System.out.println(result1);
		
		*/
		
		
		
		}
			
		

	}
