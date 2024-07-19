package l_collection;

public class Student{	// object default
	
	private String name;
	private int age;
	
	public Student(String name, int age) {
		this.name = name;
		this.age = age;
	}
	
	public String toString() {
		return name + "학생은 "+ age + " 살 입니다.";
	}
}
