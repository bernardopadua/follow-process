class Logger {
    constructor(isSet=false){
        this.isSet = isSet;
    }

    log(arMsgs){
        if(this.isSet)
            for(const msg of arMsgs)
                console.log(msg);
    }
}

export default Logger;