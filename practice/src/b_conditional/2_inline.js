// 논리연산자 + 삼항연산자

import { useState } from "react";

function Counter(props){
    const [count, setCount] = useState(0);
    return(
        <div>            
            {count && <h4> 현재 카운트 : {count}</h4>} &nbsp;<br/>
            <hr/>
            {count > 0 && <h4> 현재 카운트 : {count}</h4>} &nbsp;<br/>
            <button onClick={()=>{setCount(count+1)}}>누름</button>
        </div>
    )
}

function MailBox(props){
    const unreadMessage = props.data;
    return(
        <div>
            <h1> 나의 메일함 </h1>
            {unreadMessage.length > 0 && <h3>{unreadMessage.length}개의 읽지않은 메세지가 존재합니다.</h3>}
        </div>
    );
}

function App(){
    var msg = []
    var msg2 = ['광고메일','회의메일','기타메일']
    return(
        <div>
            <Counter/>
            <hr/>
            <MailBox data={msg}/>
            <MailBox data={msg2} />
        </div>
    );
}

export default App;

