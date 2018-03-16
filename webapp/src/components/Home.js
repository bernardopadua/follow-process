import React, { Component } from 'react'
import { Redirect } from 'react-router';

import FollowProcessAPI from './api';
import Logger from './Logger';

import TableRows from './TableRows'
import Pagination from '../components/Pagination'

class Home extends Component {
    constructor(props){
        super(props);
        
        this.state = {
            auth: props.auth,
            processes: {
                active_page: 1,
                process_per_page: 2,
                maxPage: 1
            },
            db: {
                processes: [],
                show_processes: []
            }
        };
        this.api = new FollowProcessAPI(props.auth.token);
        this.l   = new Logger(props.logger);
    }

    componentDidMount(){
        //Getting all processes for logged user
        this.getProcesses();
    }

    clickPagination(pageClick){

        const prRows = this.state.db.processes.filter(
            (el, i) => {
                const pr  = this.state.processes;
                const max = (pr.process_per_page * pageClick) - 1;

                if(i<=max && i>=max-1)
                    return true;
            }
        );

        this.l.log(["clickPagination::", prRows, "PageClick::", pageClick]);

        this.setState(
            prev => ({
                ...prev,
                processes: {
                    ...prev.processes,
                    active_page: pageClick
                },
                db: {
                    ...prev.db,
                    show_processes: prRows
                }
            })
        )
    }

    getProcesses(){
        this.api.getProcesses()
        .then(
            response => {
                this.l.log(["Home::getProcesses", response]);
                const jdata = response.data;

                if(jdata){
                    this.setState(
                        prev => ({
                            ...prev,
                            processes: {
                                ...prev.processes,
                                maxPage: Math.floor(jdata.length/prev.processes.process_per_page)
                            },
                            db: {
                                ...prev.db,
                                processes: jdata
                            }
                        })
                        , //Callback 
                        () => {
                            this.clickPagination(1);
                        }
                    );
                }
            }
        );
    }

    render(){
        return (
            <div className="d-flex flex-column">
                <div id="login-check">
                    {
                        !this.state.auth.logged ?
                            <Redirect from='/home' to='/' />
                        : null
                    }
                </div>
                <div className="d-flex flex-row">
                    <div className="p-2">
                        <button className="btn btn-sm btn-outline-primary">
                            Cadastrar Processo
                        </button>
                    </div>
                </div>

                <div className="p-1">
                    <table className="table">
                        <thead>
                            <tr>
                                <th scope="col">#</th>
                                <th scope="col">Numero Processo</th>
                                <th scope="col">Dados Processo</th>
                                <th scope="col">Ação</th>
                            </tr>
                        </thead>
                        <TableRows 
                            processes={this.state.db.show_processes}
                        />
                    </table>
                    <Pagination 
                        activePage={this.state.processes.active_page}
                        clickPagination={this.clickPagination.bind(this)}
                        maxPage={this.state.processes.maxPage}
                    />
                </div>
            </div>
        );
    }
}

export default Home;