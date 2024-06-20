function MemberGreeting(props){
    return (<h1>오늘도 반가워요</h1>)
}

function GuestGreeting(){
    return(<h2>회원가입을 해주세요</h2>)
}

function Greeting(props){
    // const isLoggedIn = true;
    // const isLoggedIn = false;
    
    // const isLoggedIn = 'true';     // true
    // const isLoggedIn = '';         // false

    // const isLoggedIn = 1;          // true : 0 아닌 모든 수
    // const isLoggedIn = 0;          // false

    // const isLoggedIn = undefined;  // false
    // const isLoggedIn = null;       // false
    // const isLoggedIn = NaN;        // false

    // 여기서만 적용되는 조건들 - python 과는 다르다는 것을 항상 알고있도록하자.
    // const isLoggedIn = [];         // true
    // const isLoggedIn = {};         // true

    const isLoggedIn = [1];            // true

    if(isLoggedIn) return <MemberGreeting/>
    else return <GuestGreeting/>

}

function App(){
    return <Greeting/>
}

export default App;
