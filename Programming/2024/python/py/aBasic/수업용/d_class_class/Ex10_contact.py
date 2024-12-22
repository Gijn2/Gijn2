
class Contact:
    def __init__(self, name, phone_number, email, addr):
        self.name=name
        self.phone_name=phone_number
        self.email=email
        self.addr=addr

    def print_info(self):
        print("이름:", self.name)
        print("전화번호:", self.phone_name)
        print("이메일:", self.email)
        print("주소;", self.addr)

def print_menu():
    print('1. 연락처 입력')
    print('2. 연락처 출력')
    print('3. 연락처 삭제')
    print('4. 종료')
    menu=input('메뉴선택:')
    return int(menu)

def set_contact():
    # 여기에 코드 작성
    name=input('name : ')
    phone_number=input('number : ')
    email=input('email : ')
    addr=input('address : ')

    contact = Contact(name,phone_number,email,addr)
    return contact
    # pass: 비어있는 코드에 임의로 작성해두는 기능도 한다.

def print_contact(contact_list):
    # 여기에 코드 작성
    for contact in contact_list:
        contact.print_info()

def delete_contact(contact_list, name):
    # 여기에 코드 작성
    for idx,contact in enumerate(contact_list):
        if contact.name == name:
            del contact_list[idx]
        else:
            print('오류')


def run():
    # Contact 인스턴스를 저장할 리스트 자료구조 생성
    contact_list = []
    while True:
        menu=print_menu()
        if menu==4:  # 종료를 선택하면
            break
        elif menu==1: # 입력을 선택하면
            contact = set_contact()
            contact_list.append(contact)
        elif menu==2: # 출력을 선택하면
            print_contact(contact_list)
        elif menu==3: # 삭제를 선택하면
            name = input('삭제할 이름은?')
            delete_contact(contact_list,name)


if __name__ == "__main__":      # 굳이 메인함수를 하나 더 만들어 돌리는 이유: 여기 외 다른데서 안 불러지게 하기 위해서
    run()