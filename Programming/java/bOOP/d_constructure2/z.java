package d_constructure2;

public class z {
	 
 int var;
String name;
public static void main(String[] args) {
	
	String s = ""; //로 바꿔
	 System.out.println("s=" + s );
	  
	z  my = null;
    my.var = 1000;
    System.out.println( my. var );
}
    
    public int  method ( int i , int j ) {
        return i + j;
    }
    
    public double method ( double i, int j ) {
        return ( i + j ) / 3;
    }
}


// 1, 2, (2번도 된다고 한다. 2&)4 , my = null; (or my = new MyClass()),
// method(double i, int j);: 오버로드해줘, 순서