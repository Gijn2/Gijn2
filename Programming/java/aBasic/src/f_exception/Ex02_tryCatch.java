package f_exception;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;

public class Ex02_tryCatch {
	public static void main(String[] args) {
		FileInputStream file = null;
		try {
			file = new FileInputStream("abc.txt");
			System.out.println("파일 연결");

			file.read();
			//file.close();
			//열고 닫기 세트

			return;
		}catch(FileNotFoundException ex) {
			System.out.println("예외 발생");
			// 첫 예외
		}catch(IOException ex) {
			System.out.println("파일 읽을때 ㅇㅖ외");
			// 그 다음 예외
		}catch(Exception ex) {
			// 나머지 처리
			System.out.println("그 외 예외발생");
		}finally {
			// 진짜 무조건 수행해야할때만 사용해야한다.
			// 파일을 열고 조건을 수행하고 나서 무조건 닫아야하기에 사용
			try{
				file.close();
			}catch(Exception ex) {}
		}
		
		// 4 3 2 1 0 / 0 1 2 3 4 /  4 2 0 2 4 /  1 2 3 4 /  * * * * * * 1.0 2.0 4.1 9.0 18.1 39.0
		// 4, 1, 4, 3, 2번, 3, 1, acdbc
	}
}
