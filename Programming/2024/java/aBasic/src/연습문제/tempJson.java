package 연습문제;

import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;

import org.json.simple.*;
import org.json.simple.parser.JSONParser;

public class tempJson {
	private static final int port = 50000;
		
		public static void main(String[] args) {
			ServerSocket serversocket;
			try { serversocket = new ServerSocket(port);
				  System.out.println("<server> listening port:5000");
				
				  while(true) {
					  Socket sock = serversocket.accept();
					  System.out.println("connect!("+sock.getInetAddress()+")");
					  
					  new user(sock).start();
				  }
			}catch(Exception e) {
				System.out.println(e);
			}
			
		}
}


class user extends Thread{
	public final Socket sock;
	private int num;
	
	user(Socket soc){
		this.sock = soc;
	}
	
	@Override
	public void run() {
        JSONParser parser = new JSONParser();
        JSONObject obj;

        try (BufferedReader in = new BufferedReader(new InputStreamReader(sock.getInputStream(), StandardCharsets.UTF_8));
             PrintWriter out = new PrintWriter(new OutputStreamWriter(sock.getOutputStream(), StandardCharsets.UTF_8), true)) {

            while (true) {
                String recvmsg = in.readLine();
                if (recvmsg == null) {
                    break;
                }

                System.out.println("receive: " + recvmsg);

                obj = (JSONObject) parser.parse(recvmsg);
                int num = ((Long) obj.get("num")).intValue() + 1;

                JSONObject responseObj = new JSONObject();
                responseObj.put("name", "server");
                responseObj.put("contents", "hello client");
                responseObj.put("num", num);

                String message = responseObj.toJSONString();
                System.out.println("send: " + message);

                out.println(message);
                out.flush();
            }
        } catch (Exception e) {
            System.out.println("[server] 클라이언트가 퇴장하였습니다.: " + e);
        } finally {
            try {
                if (sock != null && !sock.isClosed()) {
                    sock.close();
                }
            } catch (IOException e) {
                System.out.println("소켓 닫기 오류: " + e.getMessage());
            }
        }
    }
	
	
}