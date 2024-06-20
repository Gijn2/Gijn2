// 4_stop_rendering

import { useState } from "react";

/*
    stop component rendering - return null
*/

function Banner(props){
    if(!props.showbanner) return null;

    return (<div>광고</div>)
}

function MainPage(props){

    let [show,setShow] = useState(false);

    const toggleHandler = ()=>{setShow(!show)}

    return(
        <div>
            <Banner showbanner={show}/>
            <hr/>
            <button onClick={()=>{
                if(show === true) setShow(false)
                else setShow(true)
            }}>{show ? '감추기':'보이기'}</button><hr/>
            <button onClick={()=>{setShow(!show)}}>{show ? '감추기2':'보이기2'}</button><hr/>
            <button onClick={()=>{toggleHandler()}}>{show ? '감추기3':'보이기3'}</button><br/>
        </div>
    )
}

function App(){
    return <MainPage/>
}

export default App;