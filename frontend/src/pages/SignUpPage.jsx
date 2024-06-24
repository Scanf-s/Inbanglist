import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const liStyle = 'flex flex-col gap-1 items-center';
const inputStyle = 'h-12 p-2 w-full border border-solid border-slate-300 rounded-md text-sm';

const SignUpPage = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    return (
        <div className='h-screen w-screen bg-gradient-to-br from-[#f5f7fa] to-[#c3cfe2]'>
            <div className='fixed h-full w-full'>
                <div className='flex h-full justify-center items-center'>
                    <form className='w-[calc(100%-40px)] max-w-[440px] p-[50px] bg-white border rounded-xl shadow-md'>
                        <ul className='flex flex-col gap-4'>
                            <li className={liStyle}>
                                <input
                                    className={inputStyle}
                                    type='text'
                                    name='name'
                                    id='name'
                                    required
                                    autoComplete='off'
                                    placeholder='이름 혹은 닉네임'
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                />
                            </li>
                            <li className={liStyle}>
                                <input
                                    className={inputStyle}
                                    type='email'
                                    name='email'
                                    id='email'
                                    required
                                    placeholder='이메일'
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                />
                            </li>
                            <li className={liStyle}>
                                <input
                                    className={inputStyle}
                                    type='password'
                                    name='password'
                                    id='password'
                                    required
                                    placeholder='비밀번호'
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                />
                            </li>
                            <li className={liStyle}>
                                <input
                                    className={inputStyle}
                                    type='password'
                                    name='confirmPassword'
                                    id='confirmPassword'
                                    required
                                    placeholder='비밀번호 확인'
                                    value={confirmPassword}
                                    onChange={(e) => setConfirmPassword(e.target.value)}
                                />
                            </li>
                        </ul>
                        <button
                            className='my-7 w-full h-12 text-lg bg-[#929EAD] text-white rounded-md hover:bg-[#BCC5CE]'
                            type='submit'
                            name='submit'>
                            회원가입
                        </button>
                        <div className='flex justify-center gap-1 text-sm'>
                            <p>이미 회원이신가요?</p>
                            <Link to='/login' className='text-[#929EAD] font-bold'>
                                로그인
                            </Link>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default SignUpPage;
