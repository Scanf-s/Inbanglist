import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import useAuthStore from '../store/authStore';
import Modal from '../components/common/GlobalModal';

const liStyle = 'flex flex-col gap-1 items-center';
const inputStyle = 'h-12 p-2 w-full border border-solid border-slate-300 rounded-md text-sm';

const SignUpPage = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const navigate = useNavigate();

  
  // 회원가입 클릭 버튼 이벤트 함수
  const { signUp, error, setError, showModal, modalMessage, clearError } = useAuthStore();
  const handleSignUp = async (e) => {
    e.preventDefault();

    // 이메일 형식 검증
    let regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!regex.test(email)) {  
      setError('이메일 형식이 올바르지 않습니다.');
      return;
    }
    

    // 비밀번호 일치 여부 확인
    if (password !== confirmPassword) {
      setError('비밀번호가 일치하지 않습니다.');
      return;
  }

    signUp(name, email, password,
      () => navigate('/login'), // 성공 시 리디렉트
      (error) => {
        // 에러가 발생하면 전역 상태에 에러를 설정
        console.error('Sign up error:', error);
      }
    );
  };
  
  useEffect(() => {
    if (showModal) {
      setTimeout(() => {
        clearError();
      }, 3000);
    }
  }, [showModal, clearError]);

  // if (!showModal || !error) return null;

  return (
    <div className='h-screen w-screen bg-gradient-to-br from-[#f5f7fa] to-[#c3cfe2]'>
      <div className='fixed h-full w-full'>
        <div className='flex h-full justify-center items-center'>
          <form className='w-[calc(100%-40px)] max-w-[440px] p-[50px] bg-white border rounded-xl shadow-md' onSubmit={handleSignUp}>
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
            <button className='my-7 w-full h-12 text-lg bg-[#929EAD] text-white rounded-md hover:bg-[#BCC5CE]' type='submit' name='submit'>
              회원가입
            </button>
            <div className='flex justify-center gap-1 text-sm'>
              <p>이미 회원이신가요?</p>
              <Link to='/login' className='text-[#929EAD] font-bold'>
                로그인
              </Link>
            </div>
          </form>
          {showModal && error && <Modal message={error} onClose={clearError} />}
        </div>
      </div>
    </div>
  );
};

export default SignUpPage;
