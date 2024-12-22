package c_control;

public class Ex03_Switch_주민번호 {
	public static void main(String[] args) {

		String id = "980620-3334567";

		char ch = id.charAt(8); // 주민번호 뒷자리 2설정, charAt.()
		System.out.println(ch);

		/* 출신지
		 0이면 서울
		 1이면 인천/부산
		 2이면 경기
		 */

		switch(ch) {
		case '0':System.out.println("서울");
			break;
		case '1':System.out.println("인천");
			break;
		case '2':System.out.println("경기");
			break;
		default:System.out.println("한국인"); // 제일 마지막 문장에는 브레이크를 안 걸어줘도댐	
		}
		
		
		String area="";		// 변수 안잡아주면 오류남
		
		switch(area) {
		case "0":area="서울";System.out.println(area+"출신"); break;
		// 문장변수를 잡아주고 그 값에 넣어 줄 수 도 있 따
		case "1":System.out.println("인천"); break;
		case "2":System.out.println("경기");break;
		default:System.out.println("한국인"); }
		
		/* 성별출력
		 Switch 문장으로 성별 출력
		 */
		
		char num = id.charAt(7);
		
		switch(num) {
		case '9':
		case '3':
		case '1':System.out.println("남");	break;
		// 만약 9 1 3 모두 남자이므로 9 1 3 case문 만들어주고 마지막에만 break 넣어도댐
		case'2':System.out.println("여");	break;
		case'0':System.out.println("여");	break;
		case'4':System.out.println("여");	break;
		// 위 두 코딩 비교 예시
		default:System.out.println("한국인");
		}
		

	}
}
