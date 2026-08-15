// import { useState } from "react";
// import { useContext } from "react";
// import { createContext } from "react";

// export const ThemeContext = createContext({theme: 'lightblue'})

// function ThemeProvider(props){
//     const [theme,setTheme] = useState('lightblue');


//     return <ThemeProvider.Provider value={{theme,setTheme}}>
//         <div style={{backgroundColor: theme, padding: '10px'}}>
//             {props.children}
//         </div>
//     </ThemeProvider.Provider>
// }

// export default ThemeProvider

// export function useTheme() {
//     return useContext(ThemeContext)
// }

import { createContext, useContext, useState } from "react";

export const ThemeContext = createContext({ theme: "lightblue" });

function ThemeProvider(props) {
    const [theme, setTheme] = useState("lightblue");

    return (
        <ThemeContext.Provider value={{ theme, setTheme }}>
            <div style={{ backgroundColor: theme, padding: "10px" }}>
                {props.children}
            </div>
        </ThemeContext.Provider>
    );
}

export default ThemeProvider;

export function useTheme() {
    return useContext(ThemeContext);
}