package f_exception;

import java.io.FileInputStream;
import java.io.IOException;

public class Ex03_throws {
	public static void main(String[] args) {
		try {
			readFile();
		}catch(Exception ex) {
			System.out.println("예외발생: "+ex.getMessage());
		}
	}
	static void readFile() throws Exception {
		FileInputStream file = new FileInputStream("abc");
		
//------------------------------------------------------------------------
		
		
		try{
			method();
			System.out.println("TRY");
		} catch( Exception ex ) {
			System.out.println("EXCEPTION");
		} finally {
			System.out.println("FINALLY");
		}
		System.out.println("END");
	}
	
	static void method() throws IOException {
		  throw new IOException();
		}
	
}


