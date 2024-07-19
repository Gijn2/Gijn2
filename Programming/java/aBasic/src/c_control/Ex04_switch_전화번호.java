package c_control;

public class Ex04_switch_전화번호 {
public static void main(String[] args) {
	
			String a = "";
			String tel = "0323232-123-1234";
			int idx = tel.indexOf('-');
			
			String locNum = tel.substring(0, idx);
			System.out.println(locNum);
			
			switch(locNum) {
			case"02":a="서울"; 	 break;
			case"031":a="경기북부"; break;
			case"032":a="경인";	 break;
			default: a="한국";
			}
			System.out.println("전화번호 지역은 "+a);

			// ------------------------------------
			
			
			
			
			
}
}
