import React from 'react'

export default ({ activePage, clickPagination, maxPage }) => {
    
    const getListItem = (num, act=false) => {
        
        const pageClass = (act) ? "page-item active" : "page-item";

        return (
            <li className={pageClass}>
                <a onClick={() => {
                    clickPagination(num);
                }} className="page-link" page={num}> { num } </a>
            </li>
        );
    };

    let prevPage = null;
    let midPage  = null;
    let postPage = null;

    let previousClass = "";
    let nextClass     = "";

    if(activePage==1 && maxPage==(activePage+1)){
        midPage  = getListItem(activePage, true);
        postPage = getListItem(activePage+1);
    } else if(activePage==maxPage && maxPage>1){
        prevPage = getListItem(activePage-1);
        midPage  = getListItem(activePage, true);
    } else if(activePage>1 && activePage<maxPage){
        prevPage = getListItem(activePage-1);
        midPage  = getListItem(activePage, true);
        postPage = getListItem(activePage+1);
        previousClass = "page-item";
    } else if(activePage==1 && maxPage>=(activePage+2)){
        prevPage = getListItem(activePage, true);
        midPage  = getListItem(activePage+1);
        postPage = getListItem(activePage+2);
        previousClass = "d-none";
    } else {
        midPage  = getListItem(activePage);
        previousClass = "d-none"
    }

    if(activePage==maxPage)
        nextClass = "d-none"
    else 
        nextClass = "page-item";

    return (
        <nav aria-label="Page navigation example">
            <ul className="pagination pagination-sm">
                <li className={previousClass}>
                    <a onClick={ 
                        () => {
                            clickPagination(activePage-1)
                        } 
                    } className="page-link" href="#">Previous</a>
                </li>
                {
                    prevPage
                }
                {
                    midPage
                }
                {
                    postPage
                }
                <li className={nextClass}>
                    <a onClick={ 
                        () => {
                            clickPagination(activePage+1)
                        } 
                    } className="page-link" href="#">Next</a>
                </li>
            </ul>
        </nav>
    );
}