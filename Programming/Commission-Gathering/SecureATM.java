import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HashMap;
import java.util.InputMismatchException;
import java.util.Map;
import java.util.Scanner;

// Account 클래스를 캡슐화하고 해시된 비밀번호를 사용
class Account {
    // 필드를 private로 선언하여 외부 접근을 제한 (캡슐화)
    private final String accountNumber;
    private final String hashedPassword; // 비밀번호를 해시하여 저장
    private int balance;

    // 생성자: 비밀번호를 SHA-256으로 해시하여 저장
    public Account(String accountNumber, String password, int balance) {
        this.accountNumber = accountNumber;
        this.hashedPassword = hashPassword(password);
        this.balance = balance;
    }
    
    // 비밀번호 해싱 메서드 (보안 강화)
    private String hashPassword(String password) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] hash = md.digest(password.getBytes());
            StringBuilder sb = new StringBuilder();
            for (byte b : hash) {
                sb.append(String.format("%02x", b));
            }
            return sb.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-256 알고리즘을 찾을 수 없습니다.", e);
        }
    }
    
    // 비밀번호 검증 메서드
    public boolean verifyPassword(String inputPassword) {
        String hashedInputPassword = hashPassword(inputPassword);
        return this.hashedPassword.equals(hashedInputPassword);
    }

    // 외부에서 계좌번호를 안전하게 조회할 수 있도록 getter 제공
    public String getAccountNumber() {
        return accountNumber;
    }
    
    // 잔액 조회 메서드
    public int getBalance() {
        return balance;
    }
    
    // 입금 메서드 (내부에서 잔액을 수정하도록 캡슐화)
    public void deposit(int amount) {
        if (amount > 0) {
            this.balance += amount;
            System.out.println("✅ 입금 완료! 잔액: " + this.balance + "원");
        } else {
            System.out.println("❌ 잘못된 금액입니다.");
        }
    }
    
    // 출금 메서드 (내부에서 잔액을 수정하도록 캡슐화)
    public void withdraw(int amount) {
        if (amount <= 0) {
            System.out.println("❌ 0원 이하 금액은 출금할 수 없습니다.");
        } else if (amount > this.balance) {
            System.out.println("❌ 잔액이 부족합니다. 현재 잔액: " + this.balance + "원");
        } else {
            this.balance -= amount;
            System.out.println("✅ 출금 완료! 잔액: " + this.balance + "원");
        }
    }
}

public class SecureATM {
    private static final Scanner scanner = new Scanner(System.in);
    
    // 계좌 데이터를 Map으로 관리하여 빠른 검색 가능
    private static final Map<String, Account> accounts = new HashMap<>();
    
    static {
        // 샘플 계좌 데이터 초기화
        accounts.put("1111-2222", new Account("1111-2222", "1234", 10000));
        accounts.put("2222-3333", new Account("2222-3333", "5678", 5000));
    }

    public static void main(String[] args) {
        Account currentAccount = null;

        System.out.println("=== ATM 로그인 ===");
        System.out.print("계좌번호를 입력하세요: ");
        String inputAccount = scanner.nextLine();

        System.out.print("비밀번호를 입력하세요: ");
        String inputPassword = scanner.nextLine();

        // 로그인 처리
        // Map을 사용하여 O(1) 시간 복잡도로 계좌 검색
        Account foundAccount = accounts.get(inputAccount);
        if (foundAccount != null && foundAccount.verifyPassword(inputPassword)) {
            currentAccount = foundAccount;
            System.out.println("\n✅ 로그인 성공! 환영합니다.");
        } else {
            System.out.println("로그인 실패! 계좌번호 또는 비밀번호가 틀립니다.");
            return;
        }

        int choice;
        do {
            System.out.println("\n=== 메뉴 ===");
            System.out.println("1. 잔액 조회");
            System.out.println("2. 입금");
            System.out.println("3. 출금");
            System.out.println("4. 종료");
            System.out.print("메뉴 선택: ");
            
            // 입력 유효성 검사 및 버퍼 문제 해결
            try {
                choice = scanner.nextInt();
                scanner.nextLine(); // 버퍼 비우기
            } catch (InputMismatchException e) {
                System.out.println("❌ 잘못된 입력입니다. 숫자를 입력해주세요.");
                scanner.nextLine(); // 버퍼 비우기
                choice = 0; // 잘못된 입력이므로 다시 루프를 돌게 함
            }

            switch (choice) {
                case 1:
                    System.out.println("💰 현재 잔액: " + currentAccount.getBalance() + "원");
                    break;
                case 2:
                    System.out.print("입금할 금액: ");
                    try {
                        int depositAmount = scanner.nextInt();
                        scanner.nextLine(); // 버퍼 비우기
                        currentAccount.deposit(depositAmount);
                    } catch (InputMismatchException e) {
                        System.out.println("❌ 잘못된 금액입니다. 숫자를 입력해주세요.");
                        scanner.nextLine(); // 버퍼 비우기
                    }
                    break;
                case 3:
                    System.out.print("출금할 금액: ");
                    try {
                        int withdrawAmount = scanner.nextInt();
                        scanner.nextLine(); // 버퍼 비우기
                        currentAccount.withdraw(withdrawAmount);
                    } catch (InputMismatchException e) {
                        System.out.println("❌ 잘못된 금액입니다. 숫자를 입력해주세요.");
                        scanner.nextLine(); // 버퍼 비우기
                    }
                    break;
                case 4:
                    System.out.println("👋 이용해 주셔서 감사합니다.");
                    break;
                default:
                    System.out.println("❌ 잘못된 메뉴입니다.");
            }
        } while (choice != 4);

        scanner.close();
    }
}