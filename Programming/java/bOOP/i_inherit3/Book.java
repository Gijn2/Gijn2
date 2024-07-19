package i_inherit3;
public class Book extends Item{
/*
 * this: 현재 객체의 레퍼헌스
 * super: 부모객체의 레퍼런스
 * 
 * this(): 다른 생성자함수를 호출할 떄
 * super(): 부모의 다른 생성자함수를 호출할 때
 * 
 */
	
/**
	String 	write;
	String 	com ;
	
	Book(){			
		num = 1000;
		name = "제목없음";
		write = "ㅇㅇ";
		com = "출판사";
		
		System.out.println("자식의 기본생성자");
	}
	
	Book(int num, String name, String write, String com){
//		super.num = num;
//		super.name = name;
		super(num,title);
		
		this.write = write;
		this.com = com; 
		
		System.out.println("자식 인자생성자");
	}
	
	public static void output() {
		System.out.println("num: " );
		System.out.println("name: " );
		System.out.println("Write: ");
		System.out.println("Com: ");
	}
*/
	String writer;
	String publisher;
	
	Book(){
		num = "1000";
		title = "제목없음";
		writer = "ㅇㅇ";
		publisher = "출판사";
		
		System.out.println("자식의 기본생성자");
		
	}
	
	Book(String num, String title, String writer, String publisher){
//		super.num = num;
//		super.title = title;
		
		super(num,title);
		//super도 this 처럼 제일 위에 올려줘야한다.
		
		this.writer = writer;
		this.publisher = publisher;
		
		System.out.println("자식 인자생성자");
	}
	
	public void output() { 
		System.out.println("번호:" + num);
		System.out.println("제목:" + title);
		System.out.println("작가:" + writer);
		System.out.println("출판사:" + publisher);
	}
	
}
