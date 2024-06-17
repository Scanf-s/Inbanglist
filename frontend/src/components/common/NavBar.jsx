const NavBar = ({ toggleDarkMode, darkMode }) => {
    return (
        <div
            className={`flex justify-between ${
                darkMode ? 'bg-slate-800' : 'bg-slate-200'
            } p-4 h-[68px]`}>
            <h1 className={`text-3xl ${darkMode ? 'text-white' : 'text-black'}`}>StreamView</h1>
            <div
                className={`w-12 h-7 p-2 bg-slate-400 ${
                    darkMode ? 'bg-slate-900' : ''
                } cursor-pointer rounded-full relative transition-all`}
                onClick={toggleDarkMode}>
                <div
                    className={`w-5 h-5 bg-white absolute top-1 left-1 rounded-full transition-all ${
                        darkMode ? 'translate-x-5' : ''
                    }`}>
                    <div
                        className={`w-full h-full bg-black ${
                            darkMode ? 'bg-white' : ''
                        } rounded-full`}
                    />
                </div>
            </div>
        </div>
    );
};

export default NavBar;
