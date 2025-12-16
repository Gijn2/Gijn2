package b_conclusion;

import java.util.Calendar;

public class Y_useful_Calender샘플 {
public static void main(String[] args) {
	
	/* 날짜관련 클래스 소속:java.util 패키지안에 있다
	 * Date
	 * 
	 * Calendar**
	 * 
	 * LocalDate**
	 * 
	 * LocalDateTime
	*/
	
	// Calendar c = new Calendar(); 이미 컴퓨터 안에 달력이 있으므로 new 사용 불가
	
	Calendar c 	= Calendar.getInstance();			// 이미 있는 데이터를 불러오기.
	int year 	= c.get(Calendar.YEAR);
	int month 	= c.get(Calendar.MONTH)+ 1; 		// 숫자는 0부터 세기에 +1
	int day 	= c.get(Calendar.DATE);
	
	System.out.println(year+"/"+ month +"/"+day);
	
	int hour = c.get(Calendar.HOUR);
	int min  = c.get(Calendar.MINUTE);
	int sec  = c.get(Calendar.SECOND);
	
	System.out.println(hour +":"+ min+":"+sec );
	
	//---------올해 연도 구하기------------------------------------------
	
	String id = "980620-1234567";
	String old_str = id.substring(0,2);
	// System.out.println(old_str); 		//"98"
	
	// String -> int 형으로 변환: "98" -> 98
	//int old = (int)old_str;				//Str은 참조형이라 자료형이다름: 캐스팅 힘듬
	int old = Integer.parseInt(old_str);
	
	char gend = id.charAt(7);
	int  cent = 0;
	int  age  = 0;
	
	switch(gend) {
	case'9':
	case'0':
	case'1': 
	case'2': cent = 1900;break;
	case'3': 
	case'4': cent = 2000;break;
	}
	
	age = year-(cent+old)+1;
	
	System.out.println("현재 나이"+age);
	
	
		
	
	
	
}
}
