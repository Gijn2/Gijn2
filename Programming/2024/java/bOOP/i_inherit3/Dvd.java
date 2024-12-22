package i_inherit3;

public class Dvd extends Item{
/**
		int 	num = 8;
		String 	name = "이름";
		String 	actor = "배우";
		String 	Direct = "감독";
	Dvd(){
		
	}
	Dvd(int num,String name, String actor, String Direct){
		this.num = num;
		this.name = name;
		this.actor = actor;
		this.Direct = Direct;
	}
	public static void output() {

	}
	*/
	
	String actor;
	String director;
	
	public void output() { 
		System.out.println("번호:" + num);
		System.out.println("제목:" + title);
		System.out.println("배우:" + actor);
		System.out.println("감독:" + director);
	}
	
}
