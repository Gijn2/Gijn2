package i_inherit3;

public class Cd extends Item{
/**
	int 	num;
	String 	name;
	String 	singer;


	Cd(){

	}

	Cd(int num ,String name,String singer){
		this.num = num;
		this.name = name;
		this.singer = name;
	}
	public static void output() {

	}
*/
	
String singer;
	
	public void output() { 
		System.out.println("번호:" + num);
		System.out.println("제목:" + title);
		System.out.println("가수:" + singer);
	}
	
}
