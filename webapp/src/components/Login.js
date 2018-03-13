import React from 'react'
import { Redirect } from 'react-router'

export default ({ logged, doLogin }) => {

    let username = "";
    let password = "";

    return (
        <div className="d-flex p-5">
            {
                logged ?
                    <Redirect from='/' to='/home' />
                : null
            }   

            <form className="form-signin" style={{width:'450px'}} onSubmit={ e => { e.preventDefault(); } }>
                <div className="form-label-group">
                    <input id="username" 
                        required="true" 
                        className="form-control" 
                        placeholder="Login" 
                        ref={ el => { username = el } }
                    />
                    <label htmlFor="username">Login</label>
                </div>
                <div className="form-label-group">
                    <input id="password" 
                        type="password" 
                        required="true" 
                        className="form-control" 
                        placeholder="Password" 
                        ref={ el => { password = el } }
                    />
                    <label htmlFor="password">Password</label>
                </div>
                <button 
                    className="btn btn-sm btn-primary btn-block" 
                    type="submit"
                    onClick={ e => { doLogin(username.value,  password.value); } }
                >
                    Login
                </button>
            </form>
        </div>
    );
}