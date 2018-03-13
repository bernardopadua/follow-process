import React, { Component } from 'react'
import processes from '../data/process_fake.json'

import Pagination from '../components/Pagination'

class Home extends Component {
    constructor(props){
        super(props);
        
        this.state = {
            logged: props.logged,
            processes: {
                active_page: 1,
                process_per_page: 2,
                maxPage: 0
            },
            db: {
                processes: []
            }
        };
    }

    getProcesses(){
    }

    render(){
        return (
            <div className="d-flex flex-column">
                <div id="login-check">
                    {
                        !this.state.logged ?
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
                        <tbody>
                        </tbody>
                    </table>
                    <Pagination 
                        activePage={this.state.processes.active_page}
                        clickPagination={null}
                        maxPage={this.state.processes.maxPage}
                    />
                </div>
            </div>
        );
    }
}

export default Home;