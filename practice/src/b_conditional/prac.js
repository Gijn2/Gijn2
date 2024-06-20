import "../App.css"
import { useState } from "react"

function MyCount (){
    let [cal,setCal] = useState(0);

    return(
    <tr style={{width:'100px', paddingLeft:'75px'}}>
            <button onClick={()=>{setCal(cal +=1)}} >▲</button>
            <td style={{textAlign:'right',width:'80%'}}>{cal}</td>
            <button onClick={()=>{setCal(cal -=1)}} >▼</button>
    </tr>);
}

function MyMenu (){
    let [fruit] = useState(['사과','배','귤'])
    return(
    <table >
            { fruit.map((item,idx)=>{
                return(
                    <table style={{border : '3px double black' , width:'200px'}}>
                        <tr >
                            <td key={item} style={{width:'100px'}}>{fruit[idx]}</td>
                            <MyCount/>
                        </tr>
                    </table>
                )
            })
        }
    </table>)
}

function App(){
    return(<MyMenu/>)
}

export default App;