import React from 'react'

import ButtonGroup from './subcomponent/TableRows-Button-Group'

export default ({ processes }) => {

    let rows = null;

    if(processes.length==0 || processes===undefined){
        rows = (
            <tr>
                <td colSpan="4"> LOADING </td>
            </tr>
        );
    } else {
        rows = processes.map(
            (el, i) => {
                return (
                    <tr key={el.pk}>
                        <th scope="row">{i+1}</th>
                        <td>{el.numero_processo}</td>
                        <td>{el.dados_processo}</td>
                        <td>
                            <ButtonGroup />
                        </td>
                    </tr> 
                );
            }
        )
        
    }

    return (
        <tbody>
            {rows}
        </tbody>
    );
}