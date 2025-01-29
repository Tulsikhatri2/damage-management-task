import React from "react";
import { Route, Routes } from "react-router-dom";
import DamagePercentage from "./Pages/DamagePercentage";
import Authentication from "./Pages/Authentication";

function App() {
    return (
        
          <Routes>
            <Route path="/" element={<DamagePercentage/>}/>
            <Route path="/login" element={<Authentication/>}/>
          </Routes>
    );
}

export default App;
