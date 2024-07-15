import React from 'react';
import { Route, Navigate } from 'react-router-dom';
import useAuthStore from '../store/authStore';

const PrivateRoute = ({ component: Component, ...rest }) => {
    const auth = useAuthStore(state => state.auth);

    return (
        <Route 
            {...rest} 
            render={(props) => 
                auth.token ? (
                    <Component {...props} />
                ) : (
                    <Navigate to="/login" />
                )
            } 
        />
    );
};

export default PrivateRoute;




// 로그인 하지 않은 사용자로부터 보호하고 싶은 컴포넌트를 감싸서 보호가 가능
// App.jsx 사용예시
// <Route path='bookmark' element={
//             <PrivateRoute>
//               <Bookmark darkMode={darkMode} />
//             </PrivateRoute>
// } />