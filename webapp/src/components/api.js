import axios from 'axios'
import Config from '../config/Config'

export default class FollowProcessAPI {
    constructor(){
        this.request = axios.create({
            baseURL: Config.baseURL
        });
    }

    objToData(objData){
        let httpData = new FormData();
        for(const field in objData){
            if(field!==undefined)
                httpData.append(field, objData[field]);
        }
        httpData.append('token', this.token);
        return httpData;
    }

    getToken(login, pass){
        return new Promise(
            (res, err) => {
                const loginData = this.objToData({
                    username: login,
                    password: pass
                })
                this.request.post('get-token/', loginData)
                .then(
                    r => {
                        res(r);
                    }
                )
            }
        )
    }
    
    getProcesses(){

        return new Promise(
            (res, err) => {
                this.request.get('v1/process/')
            }
        );
    }
}