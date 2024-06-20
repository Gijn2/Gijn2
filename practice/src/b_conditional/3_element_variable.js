// 3_element_variable.js

import { useState } from "react"

function LoginBtn(){
    return(<button onClick={this.props.onClick}>로그인</button>)
}

function LogoutBtn(){
    return(<button onClick={this.props.onClick}>로그아웃</button>)
}

function LoginControl(){
    const [isLogged, setIsLogged] = useState(false);
    
    let button;
    if(isLogged) button = <LogoutBtn onClick={()=>{setIsLogged(false)}}/>
    else button = <LoginBtn onClick={()=>{setIsLogged(true);}}/>
    return button
}

function App(){
    return(<>
    <LoginControl/>
    </>)
}
export default App