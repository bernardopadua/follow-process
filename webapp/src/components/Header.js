import React from 'react'
import {NavLink} from 'react-router-dom'

export default ({ logged }) => {
    
    let login  = 'Login';
    let clogin = 'nav-item';

    if(logged){
        login   = 'Logout';
        clogin += ' active';
    }

    return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <a className="navbar-brand" href="#">Follow-Process</a>
        <button className="navbar-toggler"
            type="button"
            data-toggle="collapse"
            data-target="#navFollowProcessCollapse"
            aria-controls="navFollowProcessCollapse"
            aria-expanded="false">
          <span className="navbar-toggler-icon" />
        </button>
        <div className="collapse navbar-collapse" id="navFollowProcessCollapse">
            <ul className="navbar-nav mr-auto">
                {
                    logged ?
                    <li className="nav-item active">
                        <NavLink className="nav-link" to="/home">
                            Home
                        </NavLink>
                    </li>
                    : null
                }
                <li className={ clogin }>
                    <a className="nav-link" href="#">
                        { login }
                    </a>
                </li>
            </ul>
        </div>
      </nav>
    );
};