package d_info;

import java.sql.PreparedStatement;
import java.util.ArrayList;

public interface InfoModel {
	
	/* 함수명: insertData
	 * 인자값: null
	 * 리턴값: null
	 * 역할:  회원가입하는 입력값을 받아서 데이터베이스에 저장
	 */
	void insertData(InfoVO vo)throws Exception;
	
	/* 함수명: searchByTel
	 * 인자값: String tel
	 * 리턴값: InfoVO
	 * 역할:  전화번호를 입력받아 해당 고객의 정보를 찾아서 반환하는 함수
	 */
	InfoVO searchByTel(String tel) throws Exception;
	
	/* 함수명: 
	 * 인자값: null
	 * 리턴값 인포VO 의 어레이타입(가변성 배열)
	 * 역할: 전체검색
	 */
	ArrayList <InfoVO> searchAll() throws Exception;
	
	/* 함수명: 
	 * 인자값: null
	 * 리턴값 인포VO 의 어레이타입(가변성 배열)
	 * 역할: 전체검색
	 */
	public void deleteData(String tel) throws Exception;
	
	void modifyData(InfoVO vo )throws Exception;

	
	
	
}
