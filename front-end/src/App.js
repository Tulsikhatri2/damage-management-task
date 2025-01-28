import React from "react";
import { Route, Routes } from "react-router-dom";
import DamagePercentage from "./Components/DamagePercentage";

function App() {
    return (
        <div>
          <Routes>
            <Route path="/" element={<DamagePercentage/>}/>
          </Routes>
        </div>
    );
}

export default App;
