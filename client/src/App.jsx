import { BrowserRouter, Route, Routes ,  } from 'react-router-dom';
import { useState } from 'react';


import CheckedEvent from './popUpForm/checkedEvent/checkedEvent'

import { Login } from './pages/login/Login';
import { Registration } from './element/regisrtation/Resistration';

import { Header } from './element/header/Header';
import { LoginAdmin } from './pages/admin/loginAdmin/LoginAdmin';
import { AdminPanel } from './pages/admin/AdminMain/AdminPanel';


import Main from './pages/main/Main';
import ListStaffAdmin from './pages/admin/AdminMain/adminElement/ListStaffAdmin/ListStaffAdmin';
import { EventRouteWrapper } from './pages/admin/AdminMain/adminElement/createEvent/createEventAdmin';
import { CheckedStaff } from './popUpForm/checkedStaff/CheckedStaff';
import MainTwo from './pages/main/mainTwo';


function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  console.log(token);

  return (
    
    <div className="App">
        <Header />
      
        <BrowserRouter>
          <Routes>

            <Route path='/listStaffAdmin' element={<ListStaffAdmin />} />

            <Route path='/' element={<Main token={token} />} />
           
            <Route path="/login" element={<Login setToken={setToken} />} />
            <Route path="/checkedEvent" element={<CheckedEvent />}/>
            <Route path="/checkedStaff" element={<CheckedStaff />}/>
            
            <Route path='/registration' element={<Registration />} />

            <Route path="/createEvent" element={<EventRouteWrapper />} />

            <Route path="/mainTwo" element={<MainTwo />} />


            <Route path='/admin' element={<LoginAdmin/>} />
            <Route path='/adminPanel' element={<AdminPanel/>}/>
          </Routes> 
        </BrowserRouter> 
    </div>
  );
}

export default App;
