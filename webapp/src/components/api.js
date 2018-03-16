import axios from 'axios'
import Config from '../config/Config'

export default class FollowProcessAPI {
    constructor(token=null){
        this.request = axios.create({
            baseURL: Config.baseURL
        });
        
        if(token)
            this.token = token;
    }

    objToData(objData=null){
        let httpData = new FormData();
        for(const field in objData){
            if(field!==undefined)
                httpData.append(field, objData[field]);
        }
        httpData.append('token', this.token);
        return httpData;
    }

    objToParams(objParams=null){
        return {
            ...objParams,
            token: this.token
        };
    }

    getToken(login, pass){
        const loginData = this.objToData({
            username: login,
            password: pass
        });
        return this.request.post('get-token/', loginData);
    }
    
    getProcesses(){
        return this.request.get('v1/process/', this.objToParams());
    }
}