package c_control;

public class Ex05_switch_성적 {
public static void main(String[] args) {
	
	int kor =90, eng =60, math =90;
	int total = kor + eng + math;
	int avg = total/3;
	
	System.out.println("평균값: "+avg);
	char a = '0';
	switch(avg/10) {
		case 10:					// 결과, break 안쓰면 10은 A에 걸림
		case 9: a='A'; 		break;
		case 8: a='B'; 		break;
		case 7: a='C'; 		break;
		default: a='F';
	}
	System.out.println(a);
	
	//---------------------------------------------------------
	
	
	
}
}
