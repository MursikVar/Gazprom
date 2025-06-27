import Logo from '../../image/fullLogo.svg'
import Acc from '../../image/acc.svg'
import './header.css'

function Header() {
    return (
      <header className="header__wrappwe">
        <div className="container">
            <div className="header__items">
                <a href="/" className="header__logo">
                    <img src={Logo} alt="" />
                </a>
                <div className="header__btn">
                    <a href="/" className="header__listEvent">Мероприятия</a>
                    <a href="/mainTwo" className="header__listStaff">Каталог сотрудников</a>
                </div>
                <a href="/login" className="header__lk">
                    <img src={Acc} alt="" className="lk" />
                </a>
            </div>
        </div>
      </header>
    );
  }
  
  export {Header};