import React, { Component } from 'react'
import ReactDOM from 'react-dom'
import { browserHistory, Switch, Redirect } from 'react-router';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import FollowProcessAPI from './components/api'
import Logger from './components/Logger'

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

        this.debugging = true;

        this.api = new FollowProcessAPI();
        this.l   = new Logger(this.debugging);

        this.debuggingState();

    }

    debuggingState(){
        //Make testing faster when debugging
        if(this.debugging){
            this.state = {
                auth: {
                    token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1MjEyMjUwOTMsInVzZXJuYW1lIjoiYWRtaW4iLCJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsInVzZXJfaWQiOjF9.Ucdc2q5csJDppXQsZksvGGIDgbMAPVP9JKSd3pGXLUY",
                    logged: true
                }
            };
        }
    }

    doLogin(login, pass){
        this.l.log(["Login:: " + login, "Pass:: " + pass]);

        this.api.getToken(login, pass)
        .then(
            response => {
                this.l.log(["thenDoLOGIN", response]);

                const data = response.data;
                if(data.token){
                    this.setState(
                        {
                            auth: {
                                logged: true,
                                token: data.token
                            }
                        }
                    );
                }
            }
        )
        .catch(
            response => {
                this.l.log(["Error:: ", response]);
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
                            <div className="col text-center">
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
                                        component={
                                            () => ( 
                                                <Home 
                                                    logger={this.debugging}
                                                    auth={this.state.auth}
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