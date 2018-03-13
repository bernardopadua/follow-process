import React, { Component } from 'react'
import ReactDOM from 'react-dom'
import { browserHistory, Switch, Redirect } from 'react-router';
import { BrowserRouter as Router, NavLink, Route, IndexRoute } from 'react-router-dom';

import FollowProcessAPI from './components/api'

import Header from './components/Header'
import Login from './components/Login'
import Home from './components/Home'

class App extends React.Component {
    constructor(props){
        super(props);

        this.state = {
            auth: {
                token: null,
                logged: false
            }
        };

        this.api = new FollowProcessAPI();
    }

    doLogin(login, pass){
        console.log("LOGIN:: " + login);
        console.log("PASSS:: " + pass);
        this.api.getToken(login, pass)
        .then(
            response => {
                console.log("response doLogin");
                console.log(response);
            }
        );
    }

    render(){
        return(
            <Router baseName="/" history={browserHistory}>
                <div id="container-follow-process-app">
                    <Header logged={this.state.auth.logged} />
                    <div className="container">
                        <div className="row">
                            <div className="col- text-center">
                                <Switch>
                                    <Route path='/' exact
                                        component={ 
                                            () => (
                                                <Login 
                                                    logged={this.state.auth.logged}
                                                    doLogin={this.doLogin.bind(this)}
                                                />
                                            )
                                        }
                                    />
                                    
                                    <Route path='/home' exact
                                        render={
                                            () => ( 
                                                <Home 
                                                    logged={this.state.auth.logged}
                                                /> 
                                            )
                                        } 
                                    />
                                </Switch>
                            </div>
                        </div>
                    </div>
                </div>
            </Router>
        );
    }
}

ReactDOM.render(
    <App />,
    document.getElementById('app')
);