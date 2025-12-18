package b_conclusion;

import java.util.Scanner;

public class C_control {
	// 제어문 관련 class
	public static void main(String[] args) {
		
		// Chapter 1. if~ #1

		String id =  "111111-1234567";				//String id = new String(""); 대신가능
		id.charAt(7);						// 자바스크립 = 프로그램언어는 0부터 카운트/ 데이터베이스쪽은 1부터 카운트
		char num = id.charAt(7);

		if(num=='1' || num=='3'|| num=='9') {		// 실수형이랑 문자형 구분 안하면 다르게 인식한다.
			System.out.println("남자");
		}else if(num=='0' || num=='2'|| num=='4'){
			System.out.println("여자");
		}else if(num=='5'||num=='7') {
			System.out.println("남 외국인");
		}else if(num=='6'||num=='8') {
			System.out.println("여 외국인");
		}
		
		char num1 = id.charAt(1);
		char num2 = id.charAt(2);
		System.out.println("당신이 태어난 년도는"+num1+num2);
		
		
		System.out.println("문자입력");
		Scanner input = new Scanner(System.in);
		String str = input.next();
		char ch = str.charAt(0);					//String -> char 형변환 안됨. 둘이 자료형이 다름
		
		
		// if~ #2
		System.out.println("전화번호를 입력하세요");		
		Scanner inputing = new Scanner(System.in);		// input이라는 변수에 system.in에 적인 값 저장 
		String Num = inputing.nextLine();				// Num이라는 문장 변수에 input값 문자로 저장
		String b = "";
		
		int a = Num.indexOf("-");					// a라는 숫자변수에 Num변수에 첫"-"의 자리수를 숫자로 저장
		String a1 = Num.substring(0,a);		// a1이라는 문장변수에 Num변수에 0번째~a-1번째 까지를 글로 저장
		
		if(a1.equals("02")) {					//if문 안에서 생기는 변수는 if문 안에서만 쓸 수 있는 변수. 밖에서는 소멸
		Num = "인천";									//if()문의 결과가 T/F에 따라
		}
		
		// ************************************************************
		String tel = "02-123-4567";
		String gu = "";

		char cha = tel.charAt(5);
		System.out.println(cha);
		
		// 서울인 경우 5번째 문자의 값이 3이면 마포구 아니면 강남구
		if(tel.equals("03")) {
			System.out.println("마포구");
			if(cha=='3') {
				gu="마포구";
			}else {
				gu="강남구";
			}
		}else {
			
		}
		


		// Chapter 2. Switch
		String idc = "980620-3334567";

		char chaR = idc.charAt(8); 								// 주민번호 뒷자리 2설정, charAt.()
		System.out.println(chaR);

		switch(chaR) {
		case '0':System.out.println("서울");							
			break;
		case '1':System.out.println("인천");
			break;
		case '2':System.out.println("경기");
			break;
		default:System.out.println("한국인"); 	  					 // 제일 마지막 문장에는 브레이크를 안 걸어줘도댐	
		}
		
		String area="";													// 변수 안잡아주면 오류남
		
		switch(area) {
		case "0":area="서울";System.out.println(area+"출신"); break;	 // 문장변수를 잡아주고 그 값에 넣어 줄 수 도 있 따
		case "1":System.out.println("인천"); break;
		case "2":System.out.println("경기");break;
		default:System.out.println("한국인"); }
		
		char numb = idc.charAt(7);

		// Switch 문장으로 성별 출력
		switch(numb) {
		case '9':
		case '3':
		case '1':System.out.println("남");	break;			// 만약 9 1 3 모두 남자이므로 9 1 3 case문 만들어주고 마지막에만 break 넣어도댐
		case '2':System.out.println("여");	break;			
		case '0':System.out.println("여");	break;
		case '4':System.out.println("여");	break;			// 위 두 코딩 비교 예시
		default:System.out.println("한국인");
		}
		
		// Swtich #2
		String aA = "";
		String tele = "0323232-123-1234";
		int idx = tele.indexOf('-');
		
		String locNum = tele.substring(0, idx);
		System.out.println(locNum);
		
		switch(locNum) {
		case"02":aA="서울"; 	 break;
		case"031":aA="경기북부"; break;
		case"032":aA="경인";	 break;
		default: aA="한국";
		}
		System.out.println("전화번호 지역은 "+aA);

		// Swtich #3
		int kor =90, eng =60, math =90;
		int total = kor + eng + math;
		int avg = total/3;
		
		System.out.println("평균값: "+avg);
		char ac = '0';
		switch(avg/10) {
			case 10:						
			case 9: ac='A'; 		break;	// 결과, break 안쓰면 10은 A에 걸림
			case 8: ac='B'; 		break;
			case 7: ac='C'; 		break;
			default: ac='F';
		}
		System.out.println(ac);



		// Chapter 3. for~
		
		/**		for(char ch='A';ch<='C';ch++) {
					//for(초기값 ; 조건문 ;증감식) 
					System.out.println(ch);
					// 초기값 -> 조건문 -> T일 경우, {}진행-> 증감식 -> 조건문(반복) -> F일 경우, for문 이탈 
				}
		*/

		// A ~ S
		for(char r='A';r<='S';r+=2) {
			System.out.println(r);
		}


		//1 ~ 10
		int hap = 0;
		for(int i=1;i<=10;i++) {
			//hap = hap++; or hap = hap+1;
			hap += 1;
		}
		System.out.println("합: "+hap);

		//1~15까지 출력
		System.out.println("계산 최댓값 :");
		Scanner inputS = new Scanner(System.in);
		int number = inputS.nextInt();
		
		System.out.println("나눌 자릿수 :");
		Scanner inputS1 = new Scanner(System.in);
		int number1 = inputS1.nextInt();
		
		for(int al =1; al <=number; al++) {
			System.out.print("i= "+a+", ");
			// 5개씩 끊어서 출력하고싶을때, (5의 배수인 경우, 개행하는 법 )
			if(al%number1==0) {
				System.out.println("");  //syso(), 괄호 안을 채우지 않고도 가능 
			}
		}

		// -----------------------
		System.out.println("문자입력");
		Scanner inputScan = new Scanner(System.in);

		String an = inputScan.nextLine();
		char chab = an.charAt(0);
		
		if('a'<=chab&chab<='z') {
			for(char alpha='a';alpha<=chab;alpha++) {
				System.out.println(alpha);
			}
		}else if('A'<=chab&chab<='Z') {
			for(char alpha='A';alpha<=ch;alpha++) {
				System.out.println(alpha);
			}
		}



		// Chapter 3-1. 중첩 for~
		System.out.print("*");

		for(int al1 = 1; al1 <=4; al1++) {
			System.out.println("");
			for(int al = 1;a<=5;a++) {
				System.out.print("*");
			}
		}
		
		// Ex-1

		for(int a2 = 0; a2 <=4; a2++) {
			System.out.println("");
			for(int a3 = 1;a3<=a2+1;a3++) {
				System.out.print("*");
			}
		}
		
		// Ex-2
		for(int a2 = 0; a2 <=4; a2++) {
			System.out.println("");
			for(int a3 = 1;a3<=5-a2;a3++) {
				System.out.print("*");
			}
		}

		// Ex-3
		System.out.println("높이");
		Scanner input10 = new Scanner(System.in);
		int a10 = input10.nextInt();					// 높이

		System.out.println("너비");
		Scanner input11 = new Scanner(System.in);
		int a11 = input11.nextInt();					// 너비
		int c10 = 0;									// 행(높이)의 번호
		
		
		for(int b10 =1;b10<=a10; b10++) {				// 
			if(c10%2==0) {
				for(int b11=1;b11<=a11;b11++) {
					System.out.print(b11+(a11*c10));
				}System.out.println();
				c10 +=1;
			}
			if(c10%2!=0) {
				for(int b11=a11;a11>=b11&b11>0;b11--) {
					System.out.print(b11+(a11*c10));
				}System.out.println();
				c10 +=1;
			}
		}



		//Chapter 4.  while~
		
		/*	for  : 주로 반복횟수가 정해진 경우,
			while: 주로 반복횟수가 정해지지 않은 경우,
			-- 'for'문을 빡세게 연습하고 'while'로 가는것을 추천
		*/

		int dan = 3; 	// 구구단의 3단 출력 (입력받을 수 있음)
		int ai  = 1;
		while(ai<=15) {
			System.out.print(dan*ai+" ");
			ai++;
			System.out.printf("%d * %d= %d \n");
		}

		// Chapter 4-1. do~ While
		int sum = 0;
		int i =1;
		do {
			sum += i;
			i++;
		}while(i<=10);
		System.out.println(sum);

		// #2
		String answer = "";
		do {
			System.out.println("구구단의 단수->");
			int dans = input.nextInt();
			
			for(int in=1; in<=9; in++) {
				System.out.println(dans*in);
			}
			System.out.println("반복?(Y/N)");
			answer = input.next();
		}while(answer.equals("y")|answer.equals("Y"));
		


		// Chapter 5. Break_Countinue
		// break   : 블럭을 벗어나는 문장. (switch)
		// continue: 블럭의 끝으로 가라.

		Jump:										//만약 전부 스킵하고싶을 경우, 구간을 설정 **눈에 잘 띄게 설정해놓기
		for(int in =0; in<2; in++) {
			
			for(int j =0; j<3; j++) {
				if(j ==3) {
					break Jump;						// 3일때, } ...("데이터");}로 	-> for 문 탈출
													// 구간을 탈출하고 싶으면 break 뒤에 Jump(구간명) 붙혀주기/ 구간 제일 끝으로 가려면 continue 뒤에~
				}
				if(j ==1) {
					continue;						// 1일때, (i+", "+j);의 뒤로 	-> for 문 내부
				}
				System.out.println(i+", "+j);
			}
			System.out.println("데이터");
		}




		// Review
		/**
		
		String sn = "980620-1234567";
		char g = sn.charAt(0);

		if(g =='9'||g =='0') {
			System.out.println("MZ");
		} else {
			System.out.println("-틀-");
		}

		switch(g) {
		case'8':	System.out.println("젊은이"); break;
		case'9':
		case'0':	System.out.println("청년"); break;
		default: 	System.out.println("정상인");
		}

		// -------------------------------

		Scanner sc = new Scanner(System.in); // 스캐너 객체 생성
		System.out.println("정수 2개 입력");
		int firstNum = sc.nextInt(); // 첫 번째 정수입력
		int secondNum = sc.nextInt(); // 두 번째 정수입력

		for (int i = 0; i < firstNum; i++) { // 0부터 N까지 높이
			if(i % 2 == 0) { // 나머지가 0이면 ---> 방향
				for (int j = (i*secondNum) + 1; j <= (i + 1) * secondNum; j++) {
					System.out.print(j + " ");
				}
				System.out.println(""); // 줄 바꿈
			}
			else { // 나머지가 0이 아니면 <--- 방향
				for (int j = (i + 1) * secondNum; j > (i*secondNum); j--) {
					System.out.print(j + " ");
				}
				System.out.println(""); // 줄 바꿈
			}
		}
		//--------------------------------------------------
		for(int i=0; i<5; i++) {
			for(int j=0; j<15; j++) {
				if(j<5) {
					System.out.print("**");
				}else if(j>=5) {
					System.out.print("--");	
				}
			}
			System.out.println();
		}

		for(int i=0; i<5; i++) {
			for(int j=0; j<15; j++) {
				System.out.print("--");
			}
			System.out.println();
		}

		// -------------------------------
		System.out.println();

		for(int i=0; i<5; i++) {
			for(int j=0; j<4-i; j++) {
				System.out.print(" ");
			}
			for(int j=0; j<i+1; j++) {
				System.out.print("*");
			}
			System.out.println();
		}
		// -----------------------------------	
		
			Scanner input = new Scanner(System.in); // 스캐너 객체 생성
			System.out.println("삼각형의 높이, 종류");
			int num1 = input.nextInt(); // 첫 번째 정수입력
			int num2 = input.nextInt(); // 두 번째 정수입력
			
			for(int a =0; a<=num1; a++ ) {
				System.out.println("*");
			}

	 	*/
	}
}